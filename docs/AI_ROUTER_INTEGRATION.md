# تكامل AI Provider Router

## الغرض من التكامل

لا يستدعي مصنع المحتوى أي مزود ذكاء اصطناعي مباشرة. عند استخراج النص من الفيديو، يمر طلب إنشاء العنوان والأوصاف والوسوم ووسم المحتوى الاصطناعي عبر **[AI Provider Router](https://github.com/ysrg2003/ai-provider-router)** فقط. يطبّق الموجّه ترتيب النماذج والمفاتيح وسياسات إعادة المحاولة من إعداداته المستقلة، ويسجل محاولات النجاح أو الفشل في قاعدة SQLite.[1]

> **ما يفعله هذا التكامل:** ينتج كائن JSON منظم لبيانات الفيديو الوصفية. **ما لا يفعله:** لا يختار أو ينشئ مفاتيح للمستخدم، ولا ينشر المحتوى عند فشل جميع المزودات، ولا يتجاوز سياسات أو حدود مزودي الذكاء الاصطناعي.

## مكان التكامل داخل المشروع

| العنصر | المسار | المسؤولية |
| --- | --- | --- |
| استدعاء الموجّه | `scripts/pipeline.py` | إنشاء `AIRouter` واستدعاء `complete_json()` للتحويل من النص إلى metadata منظمة |
| نسخة الموجّه في CI | `.github/workflows/publish.yml` | استنساخ نسخة مثبّتة من الموجّه وتثبيتها قبل تشغيل المعالجة |
| إعداد الموجّه | `.ai-provider-router/config/` أثناء التشغيل | تعريف المزودات، سلاسل النماذج، مجموعات المفاتيح، وسياسات التبريد |
| حالة التشغيل | `temp/ai_router.db` | سجل SQLite لمحاولات AI في تشغيل الفيديو الحالي؛ يُرفق في Artifact لمدة يوم واحد |

## المتطلبات

| المتطلب | مطلوب؟ | السبب |
| --- | --- | --- |
| Python 3.11 أو أحدث | نعم | يطابق متطلبات مصنع المحتوى والموجّه |
| مفتاح Gemini مرتب في JSON | اختياري | المسار الأول في السلاسل الافتراضية |
| `HF_TOKEN` أو مفاتيح Hugging Face مرتبة | اختياري | مسار احتياطي لنماذج Hugging Face |
| مفتاح واحد صالح على الأقل | نعم للنشر | من دونه يتوقف توليد البيانات الوصفية قبل النشر |
| حسابات منصات النشر | مستقل | يلزم فقط بعد نجاح مرحلة البيانات الوصفية |

## إعداد GitHub Actions

### الخطوة 1: أضف أسرار الموجّه

نفّذ ذلك من المستودع **`ysrg2003/content-factory-gha`** في المسار **Settings → Secrets and variables → Actions**. لا تضف المفاتيح إلى ملفات Git أو الـ README أو رسالة تشغيل.

| الاسم | مطلوب؟ | الصيغة الآمنة | النتيجة المتوقعة |
| --- | --- | --- | --- |
| `AI_ROUTER_GEMINI_KEYS_JSON` | اختياري | مصفوفة JSON مرتبة من كائنات تحمل `id` و`key` و`project` | يجرّب الموجّه كل مفتاح Gemini بالتتابع |
| `AI_ROUTER_HF_KEYS_JSON` | اختياري | مصفوفة JSON مرتبة من مفاتيح Hugging Face | يدوّر الموجّه بين مفاتيح Hugging Face |
| `HF_TOKEN` | اختياري | Token واحد من Hugging Face | بديل أبسط عن مصفوفة مفاتيح Hugging Face |

مثال هيكل فقط، وليس قيمة سرية حقيقية:

```json
[
  {"id":"gemini-primary","key":"ضع_المفتاح_هنا","project":"content-factory"},
  {"id":"gemini-secondary","key":"ضع_المفتاح_الثاني_هنا","project":"content-factory"}
]
```

> لا تحفظ هذا المثال بعد وضع مفاتيح حقيقية في أي ملف. ألصق القيمة في GitHub Secret فقط.

### الخطوة 2: اختر سلسلة النماذج

أضف متغير Repository variable اختياري اسمه `AI_ROUTER_CHAIN`. القيمة الافتراضية في مصنع المحتوى هي `creative`.

| السلسلة | ترتيب الموديلات المثبّت في الموجّه | متى تستخدمها |
| --- | --- | --- |
| `creative` | Gemini Flash، ثم GPT-OSS 120B، ثم DeepSeek V4 Flash، ثم GLM 5.2، ثم DeepSeek R1 | الافتراضي المقترح للعناوين والأوصاف الإبداعية |
| `cheap` | Gemini Flash-Lite، ثم GPT-OSS 20B، ثم Qwen Thinking 4B، ثم Qwen 2.5 7B، ثم Llama 3.1 8B | عندما تكون الأولوية للاقتصاد والسرعة |
| `default` | Gemini Flash وFlash-Lite ثم عشرة بدائل Hugging Face | عندما تريد أطول مسار احتياطي |

لكل نموذج، يجرب الموجّه المفاتيح المتاحة بالترتيب قبل الانتقال إلى النموذج التالي. مثال: إذا وُجد مفتاحا Gemini، فإن سلسلة `creative` تبدأ بـFlash بالمفتاح الأول ثم Flash بالمفتاح الثاني، ثم تنتقل إلى البديل التالي إذا فشلا أو دخلا فترة تبريد.[1]

### الخطوة 3: نفّذ أول تشغيل

افتح **Actions**، اختر **Process and Publish Short Video**، أدخل رابط MP4 مباشر، وفَعِّل منصة نشر واحدة في التجربة الأولى. لا يظهر للمستخدم المفتاح في السجل؛ الموجّه يسجل معرف المفتاح الداخلي وحالة المحاولة بدلاً من قيمته.[1]

النتيجة الناجحة هي إنشاء `temp/metadata.json` قبل خطوات YouTube أو Meta أو TikTok. بعد التنفيذ، نزّل Artifact المسمى `processed-video-and-metadata-<run-id>` إن احتجت إلى فحص `temp/ai_router.db` أو الترجمة أو البيانات الناتجة.

إذا اختلفت النتيجة وظهر `All AI Provider Router attempts failed`، راجع قسم [استكشاف الأخطاء](#استكشاف-الأخطاء) ولا تحاول لصق مفتاح في سجل التشغيل.

## التشغيل المحلي للتحقق

### الخطوة 1: نزّل المشروعين

نفّذ الأوامر من Terminal على Linux أو macOS. يجب أن يكون المجلدان بجانب بعضهما لتعمل المسارات التالية كما هي.

```bash
git clone https://github.com/ysrg2003/content-factory-gha.git
git clone https://github.com/ysrg2003/ai-provider-router.git
cd content-factory-gha
```

النتيجة المتوقعة:

```text
content-factory-gha/
ai-provider-router/
```

إذا ظهر `git: command not found`، ثبّت Git أو حمّل المشروعين بصيغة ZIP وانتقل إلى مجلد `content-factory-gha` يدوياً.

### الخطوة 2: أنشئ البيئة وثبّت الحزم

نفّذ الأوامر من داخل `content-factory-gha`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e ../ai-provider-router
```

النتيجة المتوقعة هي ظهور `Successfully installed ai-provider-router...`. إذا ظهر `No module named ai_router` لاحقاً، تأكد من تفعيل البيئة؛ يجب أن يبدأ سطر الأوامر غالباً بـ`(.venv)`، ثم أعد تنفيذ آخر أمر تثبيت.

### الخطوة 3: جهّز البيئة المحلية

انسخ نموذج الموجّه إلى ملف لا يرفع إلى Git:

```bash
cp ../ai-provider-router/.env.example .env
```

أضف المفاتيح إلى `.env` في **مجلد مصنع المحتوى**، ثم نفّذ:

```bash
export AI_ROUTER_CONFIG_DIR=../ai-provider-router/config
export AI_ROUTER_STATE_DB=temp/ai_router.db
export AI_ROUTER_CHAIN=creative
ai-router --config-dir "$AI_ROUTER_CONFIG_DIR" --state-db "$AI_ROUTER_STATE_DB" summary
```

مثال لنتيجة سليمة قبل إضافة مفاتيح:

```json
{
  "config": {
    "secrets_loaded": {
      "google_gemini": 0,
      "huggingface": 0
    }
  },
  "state": {
    "calls": 0
  }
}
```

هذه النتيجة تعني أن التثبيت نجح، لا أن توليد البيانات سيعمل. بعد إضافة مفتاح واحد صالح على الأقل، يجب أن يتحول عداد المزود المقابل إلى `1` أو أكثر. إذا بقي `0`، تحقق من أن اسم المتغير يطابق الجدول أعلاه وأن JSON مصفوفة سليمة.

## عقد البيانات الناتجة

يطالب `scripts/pipeline.py` الموجّه بإرجاع كائن JSON يحتوي المفاتيح التالية. إذا أعاد نموذج كائناً ناقصاً أو قيمة غير منطقية في `contains_synthetic_media`، يفشل التشغيل **قبل النشر** حتى لا يرسل بيانات غير دقيقة للمنصات.

| المفتاح | النوع | الغرض |
| --- | --- | --- |
| `title` | string | عنوان YouTube قصير |
| `youtube_description` | string | وصف فيديو YouTube |
| `instagram_caption` | string | وصف Instagram Reel |
| `facebook_caption` | string | وصف Facebook Page Reel |
| `tiktok_caption` | string | وصف TikTok |
| `tags` | array | وسوم YouTube بلا `#` |
| `contains_synthetic_media` | boolean | إفصاح عن المحتوى الاصطناعي عند انطباقه |

## كيف يعمل المسار الاحتياطي

| الحالة | سلوك الموجّه | ما يفعله مصنع المحتوى |
| --- | --- | --- |
| نجح أول مزود | يعيد JSON فوراً ويسجل نجاحاً | يكمل المعالجة والنشر |
| 429 أو مشكلة شبكة | يطبق التبريد أو التراجع ثم ينتقل إلى المحاولة التالية وفق السياسة | ينتظر نتيجة الموجّه فقط |
| 401 أو 403 | يسجل فشل مصادقة ويبرد المفتاح | لا يعرض المفتاح في السجل؛ يتابع البدائل المتاحة |
| أرجع النموذج JSON غير صالح | يعتبرها استجابة غير صالحة وينتقل إلى البديل | لا ينشر محتوى ببيانات ناقصة |
| فشلت كل المحاولات | يرمي `AllProvidersFailed` | تتوقف المعالجة ولا تبدأ أي خطوة نشر |

## استكشاف الأخطاء

| العَرَض | السبب المرجح | التحقق | الإصلاح |
| --- | --- | --- | --- |
| `AI Provider Router is not installed` | لم يُثبت الموجّه في البيئة | نفّذ `python -m pip show ai-provider-router` | شغّل `python -m pip install -e ../ai-provider-router` محلياً؛ في GitHub تحقق من خطوة التثبيت |
| `All AI Provider Router attempts failed` | لا توجد مفاتيح صالحة، أو نفدت الحصة، أو أخفقت كل النماذج | افحص `ai-router ... summary` وملف SQLite دون عرض أسرار | أضف مفتاحاً صالحاً، انتظر التبريد، أو بدّل `AI_ROUTER_CHAIN` |
| `AI_ROUTER_GEMINI_KEYS_JSON must contain a JSON array` | صيغة Secret غير صحيحة | تأكد أنها تبدأ بـ`[` وتنتهي بـ`]` | ألصق JSON صالحاً بلا اقتباس خارجي إضافي |
| لم يظهر `HF_TOKEN` في الملخص | الاسم غير موجود أو token بلا صلاحية inference | راجع `secrets_loaded.huggingface` | أنشئ token بصلاحية Inference Providers وأضفه بالاسم نفسه |
| metadata ناقصة أو غير صالحة | نموذج لم يلتزم بالعقد | راجع رسالة الخطأ و`temp/ai_router.db` | جرّب `creative` أو `default` ولا تخفف التحقق في `pipeline.py` |

## الأمن والتنظيف

لا تضع مفاتيح حقيقية في `README.md` أو `config/*.json` أو `scripts/` أو Issue أو لقطة شاشة. استخدم `.env` محلياً وGitHub Secrets في سير العمل. إذا ظهر مفتاح في commit أو سجل، ألغِه فوراً من المزود، أنشئ بديلاً، ثم احذف القيمة من التاريخ والسجل حيث أمكن.

ملف `temp/ai_router.db` يحتوي بيانات تشخيصية عن المحاولات ومعرفات المفاتيح الداخلية، لا قيم المفاتيح. يُحتفظ به يوماً واحداً مع Artifact للتشخيص؛ نزّله فقط عند الحاجة ثم احذفه محلياً بعد إغلاق البلاغ.

## مراجع

[1]: https://github.com/ysrg2003/ai-provider-router "AI Provider Router — README and source"
