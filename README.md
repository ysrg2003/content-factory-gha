# مصنع المحتوى المباشر

## ما الذي يفعله هذا المشروع؟

هذا المشروع يحوّل رابط فيديو MP4 إلى فيديو عمودي **1080×1920** مع ترجمة عربية مدمجة، ثم ينشئ بيانات وصفية منظمة وينشر النتيجة مباشرة إلى المنصات التي تختارها: **YouTube Shorts** و**Instagram Reels** و**Facebook Page Reels** و**TikTok**.

لا توجد في المشروع أي خطوة تليجرام، أو رسالة معاينة، أو زر موافقة بين المعالجة والنشر. عند اختيار منصة في نموذج التشغيل، وبعد نجاح المعالجة، يبدأ نشرها مباشرة.

> **ما لا يفعله المشروع:** لا ينشئ حسابات منصات النشر أو مفاتيحها، ولا ينشر إذا فشلت مرحلة الذكاء الاصطناعي أو كان الفيديو غير صالح، ولا يتجاوز سياسات أي منصة.

## ما النتيجة التي ستحصل عليها؟

بعد الإعداد وتشغيل سير العمل من GitHub، ستحصل على فيديو عمودي مع ترجمة وبيانات وصفية، ثم ستظهر نتيجة كل منصة في **ملخص التشغيل**. يحتفظ المشروع بالفيديو المعالج، والترجمة، و`metadata.json`، وسجل الموجّه `ai_router.db` في Artifact لمدة يوم واحد فقط.

## كيف يعمل المشروع؟

```text
رابط MP4 مباشر
   │
   ▼
FFmpeg + Whisper
   │  فيديو عمودي + ترجمة عربية
   ▼
AI Provider Router
   │  JSON منظم مع تبديل مفاتيح/نماذج احتياطي
   ▼
YouTube / Instagram / Facebook / TikTok
```

يستخدم المشروع **[AI Provider Router](https://github.com/ysrg2003/ai-provider-router)** لكل تفاعل مع الذكاء الاصطناعي. هذا المكوّن يجرّب سلاسل مزودين ونماذج ومفاتيح بالترتيب الذي تضبطه، ويسجل المحاولات وينتقل إلى البديل عند فشل المفتاح أو الحصة أو الخدمة.[1]

## المتطلبات

| المتطلب | مطلوب؟ | لماذا؟ |
| --- | --- | --- |
| حساب GitHub | نعم | تشغيل سير العمل وإضافة الأسرار |
| رابط HTTPS مباشر لملف MP4 | نعم لكل تشغيل | تنزيل الفيديو الخام داخل سير العمل |
| مفتاح واحد على الأقل للموجّه | نعم للنشر | إنشاء العنوان والأوصاف والوسوم قبل النشر |
| إعداد OAuth أو API للمنصة المختارة | نعم لكل منصة مفعلة | تفويض النشر المباشر |
| كمبيوتر محلي وPython 3.11 | اختياري | فقط إن أردت اختبار المشروع محلياً |

تشغيل الـ runners القياسية في GitHub مجاني للمستودعات العامة، لكن يجب مراقبة سياسات التخزين واستخدام Artifacts؛ لذلك يحدد المشروع الاحتفاظ بالملفات الناتجة ليوم واحد. [2]

## خريطة المشروع

| المسار | الغرض |
| --- | --- |
| `.github/workflows/publish.yml` | سير العمل اليدوي للمعالجة والنشر المباشر |
| `scripts/pipeline.py` | التحويل العمودي، تفريغ Whisper، واستدعاء AI Provider Router |
| `scripts/publish_youtube.py` | النشر الرسمي إلى YouTube |
| `scripts/publish_meta.py` | النشر الرسمي إلى Instagram وFacebook |
| `scripts/publish_tiktok_api.py` | النشر الرسمي إلى TikTok Direct Post |
| `scripts/publish_tiktok_browser_fallback.py` | بديل متصفح معزول عند فشل TikTok API فقط |
| `docs/SETUP.md` | إعداد أسرار منصات النشر |
| `docs/AI_ROUTER_INTEGRATION.md` | إعداد الموجّه، مساراته الاحتياطية، وتشخيص فشله |
| `tests/validate_project.py` | فحص ساكن لمسارات المشروع وغياب تكامل تليجرام |

## الخطوة 1: أضف أسرار النشر والذكاء الاصطناعي

افتح مستودع GitHub ثم انتقل إلى **Settings → Secrets and variables → Actions**. أضف أولاً مفاتيح AI Provider Router، ثم مفاتيح المنصات التي ستفعلها فقط.

| الفئة | السر أو المتغير | مكان الشرح |
| --- | --- | --- |
| AI Provider Router | `AI_ROUTER_GEMINI_KEYS_JSON` أو `AI_ROUTER_HF_KEYS_JSON` أو `HF_TOKEN` | [دليل تكامل الموجّه](docs/AI_ROUTER_INTEGRATION.md) |
| YouTube | `YOUTUBE_CLIENT_SECRET_JSON` و`YOUTUBE_REFRESH_TOKEN` | [دليل الإعداد](docs/SETUP.md) |
| Meta | `META_PAGE_ACCESS_TOKEN` و`META_INSTAGRAM_ACCOUNT_ID` و/أو `META_FACEBOOK_PAGE_ID` | [دليل الإعداد](docs/SETUP.md) |
| TikTok الرسمي | `TIKTOK_ACCESS_TOKEN` | [دليل الإعداد](docs/SETUP.md) |
| TikTok الاحتياطي | `TIKTOK_BROWSER_COOKIES_BASE64` | [دليل الإعداد](docs/SETUP.md) |

**النتيجة المتوقعة:** تظهر أسماء الأسرار في صفحة GitHub من دون إظهار قيمها. إذا لصقت مفتاحاً في ملف أو سجل أو commit عن طريق الخطأ، ألغِه من مزوّده فوراً واستبدله؛ لا تكتفِ بحذف النص من Git.

## الخطوة 2: اختر سلسلة الذكاء الاصطناعي

أضف متغيراً اختيارياً باسم `AI_ROUTER_CHAIN` من قسم **Variables** في صفحة Actions. إن لم تضفه، يستعمل المشروع `creative`، وهي سلسلة مناسبة للعناوين والأوصاف. اختر `cheap` عندما تكون السرعة/الكلفة أولوية، أو `default` عندما تحتاج سلسلة احتياطية أطول. يشرح [دليل الموجّه](docs/AI_ROUTER_INTEGRATION.md) ترتيب كل سلسلة وكيف يدور بين المفاتيح.

## الخطوة 3: نفّذ أول تشغيل

من تبويب **Actions**، اختر سير العمل **Process and Publish Short Video** ثم اضغط **Run workflow**. املأ الحقول كما يلي في أول تجربة:

| الحقل | قيمة التجربة الأولى | السبب |
| --- | --- | --- |
| `video_url` | رابط HTTPS مباشر لفيديو MP4 قصير | التأكد من التنزيل والتحويل |
| منصة واحدة فقط | `true` | عزل مشكلة المنصة إن ظهرت |
| المنصات الأخرى | `false` | منع نشرات اختبار غير ضرورية |
| `allow_tiktok_browser_fallback` | `false` | لا تستخدم الكوكيز قبل اختبار TikTok API الرسمي |
| `language` | `ar` | تفريغ وتعليق عربيان |

**النتيجة المتوقعة:** تمر خطوة **Process video, transcribe, and write metadata** بنجاح، ثم تعرض صفحة Summary حالة كل منصة. إذا فشلت هذه الخطوة برسالة `All AI Provider Router attempts failed`، لا تبدأ أي منصة بالنشر؛ اتبع جدول الأخطاء في [دليل تكامل الموجّه](docs/AI_ROUTER_INTEGRATION.md#استكشاف-الأخطاء).

## وضع TikTok الاحتياطي

المسار الأساسي هو **TikTok Content Posting API**. أما البديل المتصفحي فيُشغَّل فقط عندما تتحقق الشروط الثلاثة التالية: اخترت TikTok، وفشل المسار الرسمي، وفعلت `allow_tiktok_browser_fallback`. لا يستخدم هذا البديل لأي منصة أخرى، ولا يحل محل تدقيق تطبيق TikTok أو سياساته. تطبيق TikTok غير المدقق مقيد بالنشر الخاص عبر Direct Post. [3]

## تجربة محلية اختيارية

إذا أردت اختبار الصياغة وبنية المشروع قبل استخدام GitHub، نفّذ من جذر المستودع:

```bash
python3 tests/validate_project.py
python3 -m py_compile scripts/*.py tests/validate_project.py
git diff --check
```

النتيجة المتوقعة:

```text
Static project validation passed.
```

إذا ظهر خطأ Python، تأكد أنك تعمل من مجلد يحتوي `scripts/` و`tests/`. وإذا ظهر أن `ai_router` غير مثبت في اختبار كامل، اتبع خطوة التثبيت المحلي في [دليل تكامل الموجّه](docs/AI_ROUTER_INTEGRATION.md#التشغيل-المحلي-للتحقق).

## الأمان والتنظيف

احفظ المفاتيح في **GitHub Secrets**، ولا تضعها في `requirements.txt` أو `config/*.json` أو `.env` المتعقب أو issue أو لقطة شاشة. يتجنب `.gitignore` رفع الفيديوهات المعالجة، والملفات المؤقتة، وملفات الجلسات، وملفات OAuth.

يُحفظ `temp/ai_router.db` كجزء من Artifact التشخيصي لمدة يوم واحد. يحتوي السجل على محاولات وحالات ومعرفات مفاتيح داخلية، وليس قيمة المفتاح نفسها. نزّله عند التحقيق في فشل، ثم احذفه محلياً بعد الانتهاء.

## مراجع

[1]: https://github.com/ysrg2003/ai-provider-router "AI Provider Router"
[2]: https://docs.github.com/en/billing/concepts/product-billing/github-actions "GitHub Actions billing"
[3]: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post "TikTok Content Posting API — Direct Post"
