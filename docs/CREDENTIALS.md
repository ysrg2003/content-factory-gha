# دليل الاعتمادات والمتغيرات والتكاملات

## الغرض وحدود هذا الدليل

يوضح هذا الدليل، خطوةً بخطوة، **كل قيمة خارجية** يقرأها مصنع المحتوى: الأسرار، مفاتيح واجهات البرمجة، رموز الوصول، OAuth، المعرفات العامة، والمتغيرات غير السرية. وهو مخصص لمن يبدأ من الصفر ويريد معرفة مكان الحصول على كل قيمة، أين يحفظها، وكيف يتحقق من إعدادها من دون كشفها.

> **قاعدة أمنية:** لا تنسخ قيمة حقيقية إلى ملف داخل المستودع أو إلى Issue أو صورة شاشة أو سجل تشغيل. استبدل كل الأمثلة التالية بقيمك داخل GitHub Secrets فقط. إذا كُشف اعتماد، ألغِه من مزوده وأنشئ بديلاً؛ حذف النص من Git وحده لا يلغي الصلاحية.

## 1. المسار المشترك لإضافة القيم إلى GitHub

نفّذ هذا المسار مرة واحدة لكل اعتماد. يلزم أن تكون مالك المستودع أو متعاوناً لديه صلاحية كتابة.

1. افتح صفحة أسرار هذا المستودع مباشرة: [GitHub Actions Secrets](https://github.com/ysrg2003/content-factory-gha/settings/secrets/actions).
2. إذا كانت القيمة **سرية**، ابق في تبويب **Secrets** واضغط **New repository secret**. اكتب الاسم مطابقاً تماماً للجدول ثم ألصق القيمة واضغط **Add secret**.
3. إذا كانت القيمة **غير سرية**، افتح تبويب **Variables** أو استخدم [صفحة Variables المباشرة](https://github.com/ysrg2003/content-factory-gha/settings/variables/actions)، ثم اضغط **New repository variable** واحفظها بالاسم المطابق.
4. النتيجة الصحيحة هي ظهور **اسم** القيمة في القائمة من دون ظهور محتواها. شغّل workflow التجريبي لاحقاً وراجع Summary؛ لا تطبع القيمة من داخل أي خطوة.

إذا لم تجد زر **Settings** أو ظهر منع صلاحية، تأكد أنك مالك المستودع أو أن لك صلاحية كتابة. لا تنشئ secret باسم `GITHUB_TOKEN`: GitHub ينشئ هذا الرمز تلقائياً لكل تشغيل، والمشروع الحالي لا يحتاج Personal Access Token مخصصاً. [1]

## 2. خريطة جميع القيم

| الاسم الدقيق | الفئة | سرية؟ | مطلوب متى؟ | يقرأه أين؟ |
| --- | --- | ---:| --- | --- |
| `AI_ROUTER_GEMINI_KEYS_JSON` | مجموعة مفاتيح Gemini مرتبة | نعم | عند استخدام Gemini في توليد metadata | خطوة AI Provider Router و`pipeline.py` |
| `AI_ROUTER_HF_KEYS_JSON` | مجموعة Tokens Hugging Face مرتبة | نعم | عند استخدام أكثر من Token من Hugging Face | خطوة AI Provider Router و`pipeline.py` |
| `HF_TOKEN` | Token Hugging Face منفرد | نعم | بديل أبسط عن المجموعة المرتبة | خطوة AI Provider Router و`pipeline.py` |
| `YOUTUBE_CLIENT_SECRET_JSON` | OAuth client configuration | نعم | عند تفعيل YouTube | `publish_youtube.py` |
| `YOUTUBE_REFRESH_TOKEN` | OAuth refresh token للقناة | نعم | عند تفعيل YouTube | `publish_youtube.py` |
| `META_PAGE_ACCESS_TOKEN` | Page Access Token من Meta | نعم | عند تفعيل Instagram أو Facebook | `publish_meta.py` |
| `META_INSTAGRAM_ACCOUNT_ID` | معرف حساب Instagram احترافي | ليس سراً، لكنه مخزن كسِر لتوافق workflow | عند تفعيل Instagram | `publish_meta.py` |
| `META_FACEBOOK_PAGE_ID` | معرف صفحة Facebook | ليس سراً، لكنه مخزن كسِر لتوافق workflow | عند تفعيل Facebook | `publish_meta.py` |
| `TIKTOK_ACCESS_TOKEN` | User Access Token لـTikTok | نعم | عند تفعيل TikTok الرسمي | `publish_tiktok_api.py` |
| `TIKTOK_BROWSER_COOKIES_BASE64` | جلسة متصفح TikTok مشفرة Base64 | نعم، عالية الخطورة | بديل TikTok فقط | `publish_tiktok_browser_fallback.py` |
| `AI_ROUTER_CHAIN` | اسم سلسلة نماذج | لا | اختياري دائماً | workflow، افتراضياً `creative` |
| `WHISPER_MODEL` | اسم نموذج تفريغ Whisper | لا | اختياري دائماً | `pipeline.py`، افتراضياً `base` |
| `YOUTUBE_PRIVACY_STATUS` | خصوصية فيديو YouTube | لا | اختياري عند YouTube | `publish_youtube.py` |
| `YOUTUBE_CATEGORY_ID` | فئة YouTube الرقمية | لا | اختياري عند YouTube | `publish_youtube.py` |
| `YOUTUBE_MADE_FOR_KIDS` | وسم محتوى للأطفال | لا | اختياري عند YouTube | `publish_youtube.py` |
| `META_GRAPH_VERSION` | إصدار Meta Graph API | لا | اختياري عند Meta | `publish_meta.py` |
| `TIKTOK_PRIVACY_LEVEL` | خصوصية TikTok | لا | اختياري عند TikTok | `publish_tiktok_api.py` |
| `TIKTOK_DISABLE_DUET` | منع Duet | لا | اختياري عند TikTok | `publish_tiktok_api.py` |
| `TIKTOK_DISABLE_STITCH` | منع Stitch | لا | اختياري عند TikTok | `publish_tiktok_api.py` |
| `TIKTOK_DISABLE_COMMENT` | منع التعليقات | لا | اختياري عند TikTok | `publish_tiktok_api.py` |
| `TIKTOK_BRAND_CONTENT` | إفصاح شراكة مدفوعة | لا | اختياري عند TikTok | `publish_tiktok_api.py` |
| `TIKTOK_BRAND_ORGANIC` | إفصاح عن ترويج نشاط المنشئ | لا | اختياري عند TikTok | `publish_tiktok_api.py` |

القيم الداخلية `AI_ROUTER_CONFIG_DIR` و`AI_ROUTER_STATE_DB` و`VIDEO_PATH` و`METADATA_PATH` يضبطها workflow بنفسه داخل الـ runner. لا تنشئ لها Secrets أو Variables من الواجهة.

---

# 3. الذكاء الاصطناعي: AI Provider Router

## 3.1 `AI_ROUTER_GEMINI_KEYS_JSON` — مفاتيح Gemini المرتبة

**الغرض.** يمكّن AI Provider Router من إنشاء عنوان الفيديو والأوصاف والوسوم ووسم المحتوى الاصطناعي. يجرب الموجّه المفاتيح بالترتيب داخل سلسلة النموذج المختارة، ثم ينتقل إلى نماذج أو مزودين بديلين عند فشل مصادقة أو حصة أو شبكة.[2]

**قبل البدء.** تحتاج إلى حساب Google يملك أو يستطيع استيراد مشروع Google Cloud. إذا كان الزر إنشاء مفتاح غير متاح، اطلب من مشرف المشروع أذونات إنشاء المفتاح وتفعيل خدمة Gemini، أو أنشئ مشروعاً شخصياً جديداً.[3]

### خطوة 1: أنشئ أو اختر مشروع Gemini

1. افتح [Google AI Studio — API Keys](https://aistudio.google.com/app/apikey) وسجل الدخول بالحساب الذي سيدفع الفوترة أو يدير الحصة.
2. افتح **Dashboard** ثم **Projects**. إذا كان مشروعك موجوداً في Google Cloud لكنه غير ظاهر، اختر **Import projects**، ثم ابحث عنه واستورده.
3. افتح صفحة **API Keys**، واختر المشروع الصحيح، ثم اضغط **Create API key**.
4. انسخ المفتاح فور ظهوره، واحفظه مؤقتاً في مدير كلمات مرور وليس في المستودع.

**النتيجة المتوقعة:** يظهر مفتاح جديد مرتبط بمشروع Google Cloud. المفاتيح الجديدة التي ينشئها AI Studio هي مفاتيح تفويض تلقائياً وفق وثائق Google الحالية. [3]

إذا ظهر تنبيه صلاحية، تحقق من امتلاكك لأذونات المشروع أو اطلب من المالك منح دور ملائم. إذا كنت تستخدم مفتاحاً عادياً قديماً غير مقيد، أنشئ مفتاحاً أحدث أو قيد المفتاح حسب تعليمات Google قبل اعتماده.

### خطوة 2: جهز صيغة مجموعة المفاتيح

انسخ **الهيكل الآتي فقط** إلى محرر نصي محلي، واستبدل النص بين علامات الاقتباس بقيمك الحقيقية محلياً. لا تضع مثالاً يحتوي قيمة حقيقية في أي commit.

```json
[
  {
    "id": "gemini-primary",
    "key": "REPLACE_WITH_GEMINI_KEY",
    "project": "my-google-cloud-project"
  },
  {
    "id": "gemini-backup",
    "key": "REPLACE_WITH_SECOND_GEMINI_KEY",
    "project": "my-google-cloud-project"
  }
]
```

حقل `id` تسمية تشخيصية آمنة تظهر في سجل حالة الموجّه. حقل `key` هو السر الحقيقي. حقل `project` وصف للتشخيص فقط. ترتيب العناصر مهم: يبدأ الموجّه بالعنصر الأول. إذا لديك مفتاح واحد، احذف الكائن الثاني والفاصلة قبله.

### خطوة 3: خزّن واختبر

1. اتبع [المسار المشترك](#1-المسار-المشترك-لإضافة-القيم-إلى-github) واختر **Secret**.
2. اجعل الاسم `AI_ROUTER_GEMINI_KEYS_JSON` والصق مصفوفة JSON كاملة في حقل Secret.
3. شغّل workflow ثم راقب خطوة **Check AI Provider Router configuration**. ستعرض عداد المفاتيح المحملة فقط، وليس القيم.

إذا كان العداد صفراً، فالسبب المعتاد هو JSON غير صالح أو اسم secret غير مطابق. تأكد من أن القيمة تبدأ بـ`[` وتنتهي بـ`]` ولا تضع علامات اقتباس إضافية حول المصفوفة كاملة.

**التدوير والإلغاء.** عند الاشتباه في كشف المفتاح، أنشئ مفتاحاً بديلاً في AI Studio، حدّث Secret واختبر workflow، ثم عطّل أو احذف المفتاح القديم من AI Studio وراجع استخدام المشروع. لا تحذف المفتاح القديم قبل نجاح البديل، لتجنب توقف الخدمة. [3]

## 3.2 `AI_ROUTER_HF_KEYS_JSON` و`HF_TOKEN` — Hugging Face

**الغرض.** يوفران مساراً احتياطياً لنماذج Hugging Face داخل AI Provider Router. استخدم `HF_TOKEN` عندما يوجد Token واحد؛ استخدم `AI_ROUTER_HF_KEYS_JSON` عندما تريد عدة Tokens مرتبة. لا تحتاج إلى وضع القيمتين معاً؛ المجموعة المرتبة أوضح عندما تريد تدويراً مقصوداً.

**قبل البدء.** تحتاج حساب Hugging Face وصلاحية استعمال Inference Providers. افتح [Hugging Face Access Tokens](https://huggingface.co/settings/tokens) بعد تسجيل الدخول. [4]

### خطوة 1: أنشئ Token

1. افتح **Settings** في Hugging Face ثم **Access Tokens**، أو استخدم الرابط المباشر أعلاه.
2. اضغط **New token**، واكتب اسماً واضحاً مثل `content-factory-router`.
3. اختر أقل صلاحية تحقق الغرض. لتشغيل نماذج الموجّه، أنشئ fine-grained token وأضف صلاحية **Make calls to Inference Providers** إذا ظهرت في الواجهة.
4. أنشئ Token وانسخه مرة واحدة إلى مدير كلمات مرور. لا تعتمد على إمكانية رؤيته لاحقاً.

**النتيجة المتوقعة:** يظهر token جديد باسمك في قائمة Access Tokens، ويمكن إدارته أو تحديثه أو حذفه من زر **Manage**. [4]

### خطوة 2: اختر أحد شكلَي التخزين

**خيار Token واحد:** أنشئ GitHub Secret اسمه `HF_TOKEN` والصق الـ Token فقط. هذه أبسط تجربة أولى.

**خيار عدة Tokens:** أنشئ GitHub Secret اسمه `AI_ROUTER_HF_KEYS_JSON` بالصيغة التالية:

```json
[
  {
    "id": "hf-primary",
    "key": "REPLACE_WITH_HF_TOKEN",
    "project": "content-factory"
  },
  {
    "id": "hf-backup",
    "key": "REPLACE_WITH_SECOND_HF_TOKEN",
    "project": "content-factory"
  }
]
```

**التحقق.** في خطوة فحص الموجّه، ابحث عن `huggingface` وعدد أكبر من صفر. إذا ظهر 401 أو 403 في السجل، افتح Access Tokens وتحقق من أن الصلاحية المطلوبة ما زالت مفعلة وأن الـ Token يخص الحساب الصحيح. إذا ظهر 429، انتظر فترة التبريد أو اعتمد المسار البديل.

**التدوير والإلغاء.** إذا تسرب Token، احذفه أو حدثه من **Access Tokens** فوراً ثم استبدل GitHub Secret. تنبه Hugging Face صراحة إلى تجنب وضع Token الخام في سجل الأوامر أو shell history. [4]

## 3.3 `AI_ROUTER_CHAIN` — اختيار سلسلة النماذج

هذه **Variable** وليست Secret. أضفها من تبويب Variables عند الحاجة.

| القيمة | الافتراضي؟ | الأثر | متى تختارها؟ |
| --- | ---:| --- | --- |
| `creative` | نعم | Gemini Flash ثم عدة بدائل إبداعية/عامة | العنوان والأوصاف الإبداعية، وهو الاختيار المقترح |
| `cheap` | لا | يبدأ بنماذج أخف وأقل كلفة | عند تفضيل السرعة أو الاقتصاد |
| `default` | لا | سلسلة أطول من نماذج Gemini وHugging Face | عند تفضيل أكبر عدد من البدائل |

اكتب القيمة بحروف صغيرة تماماً. إذا أدخلت اسماً غير موجود، تفشل مرحلة metadata قبل النشر؛ صححه إلى إحدى القيم الثلاث أعلاه ثم أعد التشغيل.

---

# 4. YouTube Shorts

## 4.1 `YOUTUBE_CLIENT_SECRET_JSON` — إعداد عميل OAuth

**الغرض.** يحتوي JSON لعميل OAuth 2.0 على `client_id` و`client_secret` وتعريفات OAuth اللازمة لتفويض قناة YouTube. هو سر، حتى لو كانت بعض المعرفات داخله عامة.

**قبل البدء.** تحتاج حساب Google يملك القناة أو يملك إذن رفع الفيديوهات إليها. لا يكفي API key للنشر؛ رفع الفيديو يتطلب OAuth 2.0 ونطاق الرفع `https://www.googleapis.com/auth/youtube.upload`. [5] [6]

### خطوة 1: فعّل YouTube Data API

1. افتح [Google Cloud API Library — YouTube Data API](https://console.cloud.google.com/apis/library/youtube.googleapis.com).
2. اختر مشروع Google Cloud موجوداً أو أنشئ مشروعاً جديداً من أداة اختيار المشروع أعلى الصفحة.
3. اضغط **Enable**. إذا ظهر أن API مفعلة بالفعل، انتقل إلى الخطوة التالية.

**النتيجة المتوقعة:** تظهر صفحة YouTube Data API كـ**Enabled** داخل مشروعك. إذا رفضت Google التفعيل، تحقق من امتلاكك صلاحية تفعيل الخدمات أو اطلبها من مالك المشروع. [6]

### خطوة 2: اضبط شاشة الموافقة وأنشئ OAuth Client

1. افتح [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials) واختر المشروع نفسه.
2. إذا طلبت الواجهة إعداد موافقة OAuth، أنشئ شاشة الموافقة، وحدد معلومات التطبيق، ثم أضف حساب Google الذي يملك القناة ضمن حسابات الاختبار إن كان التطبيق في وضع الاختبار.
3. اضغط **Create Credentials → OAuth client ID**.
4. لاستخدام طريقة الحصول على refresh token المبينة أدناه من OAuth Playground، اختر **Web application** وأضف Redirect URI التالي حرفياً:

```text
https://developers.google.com/oauthplayground
```

5. أنشئ العميل، ثم اختر **Download JSON**. احتفظ بالملف محلياً فقط.

الـ script يقبل JSON من قسم `web` أو `installed`. اختر نوع العميل الذي يطابق طريقة تفويضك، لكن لا تخلط إعداد Redirect URI الخاص بالويب مع عميل Desktop. [5] [7]

### خطوة 3: ضع JSON في GitHub Secret

1. افتح ملف JSON الذي نزلته في محرر محلي.
2. انسخ **كل المحتوى** من أول `{` إلى آخر `}`، من دون تعديله.
3. أنشئ GitHub Secret باسم `YOUTUBE_CLIENT_SECRET_JSON` والصق المحتوى كاملاً.

لا ترفع ملف JSON إلى المستودع ولا تلصقه في تعليق أو لقطة شاشة. إذا حملته بطريق الخطأ، احذف OAuth client من Cloud Console، أنشئ عميلاً جديداً، ثم استبدل Secret.

## 4.2 `YOUTUBE_REFRESH_TOKEN` — تفويض القناة

**الغرض.** يسمح للنظام بتجديد وصوله إلى القناة من دون تسجيل دخول كل تشغيل. لا تضع access token القصير في هذا الحقل؛ المشروع يحتاج refresh token.

### خطوة 1: استخدم OAuth Playground بحذر

1. افتح [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground/).
2. اضغط رمز الإعدادات، فعّل **Use your own OAuth credentials**، ثم أدخل `client_id` و`client_secret` من JSON الذي أنشأته محلياً. لا تحفظهما في متصفح مشترك.
3. في **Step 1**، ابحث عن **YouTube Data API v3** واختر النطاق:

```text
https://www.googleapis.com/auth/youtube.upload
```

4. اضغط **Authorize APIs**، وسجل الدخول بالحساب الذي يملك القناة المقصودة، ثم وافق على النطاق.
5. في **Step 2** اضغط **Exchange authorization code for tokens**.
6. انسخ قيمة `refresh_token` فقط، وأنشئ GitHub Secret باسم `YOUTUBE_REFRESH_TOKEN`.

**النتيجة المتوقعة:** تظهر قيمة `refresh_token` في استجابة Playground. إذا لم تظهر، أعد عملية التفويض واسمح بوصول offline حسب واجهة Google. إذا ظهر `redirect_uri_mismatch`، راجع OAuth Client وتأكد من إضافة URI Playground في الخطوة السابقة. [7]

**التحقق.** شغّل workflow مع `publish_youtube=true` فقط وفيديو تجريبي تملك حق نشره. يكتب الناشر ملف `publish-result-youtube.json` ويحوي معرف الفيديو عند النجاح. إذا ظهر `401` أو `invalid_grant`، أنشئ تفويضاً جديداً واحذف/استبدل refresh token القديم.

## 4.3 متغيرات YouTube غير السرية

| الاسم | النوع والقيمة الافتراضية | القيم الصحيحة | الأثر |
| --- | --- | --- | --- |
| `YOUTUBE_PRIVACY_STATUS` | string؛ `public` | `public`، `unlisted`، `private` | خصوصية الفيديو بعد الرفع |
| `YOUTUBE_CATEGORY_ID` | string؛ `22` | معرف فئة YouTube رقمي | فئة الفيديو في metadata |
| `YOUTUBE_MADE_FOR_KIDS` | boolean نصي؛ `false` | `true` أو `false` بأحرف صغيرة | إفصاح المحتوى الموجه للأطفال |

أضف هذه القيم من صفحة Variables. ابدأ بـ`unlisted` للاختبار إذا أردت منع ظهور فيديو الاختبار للعامة، ثم بدّل إلى `public` بعد التحقق.

---

# 5. Meta: Instagram Reels وFacebook Page Reels

## 5.1 قبل إنشاء القيم

يحتاج المشروع حساب Instagram احترافياً عند النشر إلى Instagram، وصفحة Facebook عند النشر إلى Facebook. اختر مسار التفويض الذي يناسب حسابك: **Instagram Login** للحسابات الاحترافية ذات الحضور على Instagram فقط، أو **Facebook Login for Business** للحسابات الاحترافية المرتبطة بصفحة Facebook. [8]

للنشر خارج حسابات أدوار التطبيق، قد تحتاج إلى Access Level/App Review من Meta. لا تتوقع أن يعمل رمز تجريبي مع جميع الحسابات لمجرد أن الاستدعاء يعمل على حساب المدير. [8] [9]

## 5.2 `META_PAGE_ACCESS_TOKEN` — Page Access Token

**الغرض.** يصرح للناشر بإنشاء ونشر Instagram Reels وFacebook Page Reels. هو السر الأهم لتكامل Meta.

### خطوة 1: أنشئ تطبيق Meta وأضف المنتج المناسب

1. افتح [Meta for Developers — My Apps](https://developers.facebook.com/apps/) وسجل الدخول بالحساب الذي يدير الصفحة والحساب الاحترافي.
2. اختر **Create App** واتبع معالج Meta لاختيار نوع التطبيق الملائم للأعمال والنشر.
3. أضف **Facebook Login for Business** إذا كان حساب Instagram مرتبطاً بصفحة Facebook، أو مسار Instagram Login المناسب لتكوينك.
4. أضف كل حساب اختبار أو مدير في أدوار التطبيق أثناء الاختبار. أكمل متطلبات Meta للانتقال إلى الإنتاج أو طلب الصلاحيات المتقدمة عند الحاجة.

### خطوة 2: اطلب الصلاحيات وأنشئ User Token مؤقتاً

1. افتح [Graph API Explorer](https://developers.facebook.com/tools/explorer/) واختر التطبيق الذي أنشأته.
2. اختر **Get Token → Get User Access Token**.
3. اطلب أقل مجموعة صلاحيات لازمة لهذا المشروع. لمسار Page Reels، يوضح دليل Meta الحاجة إلى `pages_show_list` و`pages_read_engagement` و`pages_manage_posts`، وإلى مهمة `CREATE_CONTENT` على الصفحة. لنشر Instagram، أضف صلاحيات نشر Instagram التي يحددها مسار تسجيل الدخول المختار، مثل `instagram_business_content_publish`. [9] [10]
4. سجل الدخول بالحساب الذي يدير الصفحة، ووافق فقط على الصلاحيات التي تحتاجها.

### خطوة 3: استخرج Page Access Token والمعرفات

1. في Graph API Explorer، نفذ طلب GET التالي باستخدام User Token الذي أنشأته:

```text
/me/accounts?fields=id,name,access_token
```

2. حدد كائن الصفحة الصحيح في الاستجابة بحسب `name`. انسخ `access_token` إلى GitHub Secret باسم `META_PAGE_ACCESS_TOKEN`.
3. انسخ `id` للصفحة ذاتها إلى GitHub Secret باسم `META_FACEBOOK_PAGE_ID`. على الرغم من أنه معرف عام، يقرأه workflow من secrets حالياً لتوافق التشغيل.
4. للحصول على معرف Instagram، نفذ:

```text
/PAGE_ID?fields=instagram_business_account
```

استبدل `PAGE_ID` بمعرف الصفحة. انسخ `instagram_business_account.id` إلى GitHub Secret باسم `META_INSTAGRAM_ACCOUNT_ID`.

**النتيجة المتوقعة:** تحصل على Page ID، وPage Access Token، وInstagram professional account ID عند وجود الربط الصحيح. إذا لم يظهر `instagram_business_account`، تحقق من أن حساب Instagram احترافي ومربوط بالصفحة الصحيحة، ثم راجع إعدادات الربط في Meta. [8] [10]

**العمر والتجديد.** تستبدل Meta رموز الوصول القصيرة برموز طويلة الأجل وفق تدفق OAuth؛ الصفحة الرسمية تذكر أن الرمز الطويل الأجل صالح 60 يوماً ويمكن تحديثه قبل انتهائه. راقب حالة الرمز من Meta ولا تفترض أنه دائم. [8]

**التحقق.** شغّل workflow مع منصة Meta واحدة فقط. عند النجاح، ينشئ الناشر ملف `publish-result-instagram.json` أو `publish-result-facebook.json`. عند 401/403، تحقق من انتهاء الرمز، التطبيق الصحيح، الصفحة الصحيحة، ودور المستخدم/الصلاحيات قبل إنشاء رمز جديد.

## 5.3 `META_GRAPH_VERSION` — إصدار API

هذه Variable غير سرية. قيمتها الافتراضية في المشروع `v26.0`. لا تغيرها إلا بعد مراجعة [Meta API Changelog](https://developers.facebook.com/docs/graph-api/changelog/) والتأكد أن نقاط النهاية المستخدمة ما زالت متوافقة. إذا أخفق نشر Meta بعد تغيير الإصدار، أعد القيمة إلى `v26.0` ثم راجع الاستجابة.

---

# 6. TikTok

## 6.1 `TIKTOK_ACCESS_TOKEN` — المسار الرسمي الكامل من الصفر

**الهدف من هذا القسم.** عند نهايته سيكون لديك User Access Token لحساب TikTok واحد، وستضعه في GitHub Secret باسم `TIKTOK_ACCESS_TOKEN`. هذا هو الرمز الذي يقرأه `scripts/publish_tiktok_api.py`؛ لا يقرأ السكربت `client_key` ولا `client_secret` من GitHub.

> **مهم جداً قبل البدء:** لا يمكن إنشاء `TIKTOK_ACCESS_TOKEN` بمجرد نسخ `client_key` أو `client_secret`. الأول يعرّف تطبيقك، والثاني يثبت هوية تطبيقك، أما `access_token` فهو إذن صادر لحساب TikTok بعد أن يسجل مالك الحساب الدخول ويضغط الموافقة. TikTok تنص على أن User Access Token وRefresh Token يجب حفظهما في جهة الخادم.[12]

### ما ستحتاجه قبل فتح TikTok

| العنصر | هل هو سري؟ | أين تحصل عليه؟ | أين يستخدم؟ |
|---|---:|---|---|
| حساب TikTok الذي سينشر المحتوى | لا، لكنه حساب مستهدف | حسابك العادي في TikTok | سيظهر في موافقة OAuth |
| حساب TikTok for Developers | لا | [developers.tiktok.com](https://developers.tiktok.com/) | إدارة التطبيق |
| `client_key` | لا، معرف تطبيق | صفحة التطبيق في **Manage apps** | تشغيل رابط التفويض |
| `client_secret` | نعم | صفحة التطبيق في **Manage apps** | استبدال code بـ tokens؛ لا تضعه في GitHub لهذا المشروع |
| Redirect URI | لا | القيمة التي تسجلها أنت في التطبيق | يجب أن تطابق الطلب حرفياً |
| `video.publish` | نطاق صلاحية | إعداد Content Posting API وموافقة TikTok | يسمح بالنشر المباشر |
| `TIKTOK_ACCESS_TOKEN` | نعم | ناتج OAuth بعد موافقة الحساب | GitHub Secret الذي يقرأه الناشر |

### الخطوة 1: أنشئ تطبيق TikTok وسجّل الدخول بالحساب الصحيح

1. افتح [TikTok for Developers](https://developers.tiktok.com/) في متصفحك.
2. اضغط **Log in**، ثم سجل الدخول بحساب TikTok الذي سيملك التطبيق. إذا كان لديك أكثر من حساب، توقف وتأكد من صورة الحساب أو اسم المستخدم الظاهر في أعلى الصفحة قبل إنشاء التطبيق.
3. اضغط صورة الحساب أو اسمك في أعلى الصفحة، ثم اختر **Manage apps**. يمكنك أيضاً فتح [صفحة Manage apps مباشرة](https://developers.tiktok.com/apps/).
4. إذا لم يكن لديك تطبيق، اضغط **Create an app**. إذا كان لديك تطبيق مخصص لمصنع المحتوى، اضغط اسمه بدلاً من إنشاء تطبيق ثانٍ.
5. عند ظهور نموذج التطبيق، اكتب اسماً واضحاً مثل:

```text
Content Factory TikTok Publisher
```

6. أكمل الحقول الإلزامية التي يعرضها TikTok. واجهة هذه الصفحة قد تختلف حسب بلدك وحالة حسابك؛ لا تختر تطبيقاً تجريبياً عشوائياً ولا تنشئ تطبيقاً باسم قناة واحدة إذا كنت تريد استخدام نفس الناشر لقنوات متعددة.
7. بعد الحفظ، ابق داخل صفحة التطبيق. أنت الآن في المكان الذي ستجد فيه `client_key` و`client_secret` ومنتجات TikTok.

**ما يجب أن تراه:** صفحة تفاصيل التطبيق أو لوحة بها اسم التطبيق وحالته ومنتجاته. إذا أعادك الموقع إلى تسجيل الدخول، أعد تسجيل الدخول بالحساب الذي يملك التطبيق، ولا تستخدم حساب TikTok مختلفاً عن الحساب الذي تريد تفويضه لاحقاً.

### الخطوة 2: أضف Login Kit واضبط Redirect URI المكتبي

سنستخدم أداة المشروع المحلية `scripts/tiktok_oauth_desktop.py`. لذلك سنستخدم تدفق **Desktop** مع عنوان loopback محلي، وليس عنوان موقع عام.

1. من صفحة تفاصيل التطبيق، ابحث عن قسم **Products** أو **Add products**.
2. أضف **Login Kit** إذا لم يكن مضافاً. افتح إعدادات Login Kit.
3. عندما يطلب منك نوع المنصة، اختر **Desktop** أو الخيار الذي يطابق تطبيق سطح مكتب/أداة محلية.
4. في حقل **Redirect URI** أو **Redirect URI(s)**، أضف هذه القيمة حرفياً، بما في ذلك `http` والمنفذ والشرطة المائلة الأخيرة:

```text
http://localhost:3455/callback/
```

5. اضغط **Save** أو **Submit**.

قواعد المطابقة الحرفية هي: `http` لا `https`، المضيف `localhost`، المنفذ `3455`، المسار `/callback/`، والشرطة المائلة الأخيرة موجودة. هذه القيمة لا تساوي `http://localhost:3455/callback` ولا `http://127.0.0.1:3455/callback/`. تسمح وثائق TikTok لتطبيقات سطح المكتب بعناوين localhost أو loopback IP مع منفذ، وتمنع إضافة query parameters أو fragments إلى URI المسجل.[13]

**ما يجب أن تراه:** يبقى Redirect URI محفوظاً في قائمة URIs الخاصة بـ Login Kit. إذا ظهر خطأ في الحفظ، تحقق من أن URI مطلق ويحتوي منفذاً وليس نصاً مثل `localhost:3455/callback/` بلا `http://`.

### الخطوة 3: أضف Content Posting API وفَعّل Direct Post

1. ارجع إلى صفحة التطبيق في TikTok for Developers.
2. من **Products** اضغط **Add products** أو **Add product**.
3. اختر **Content Posting API** ثم اضغط **Add** أو **Configure**.
4. داخل إعدادات Content Posting API، ابحث عن **Direct Post** أو **Direct Post configuration** وفَعّله.
5. ابحث عن الصلاحية أو النطاق `video.publish`. اطلبه أو فعّله من إعدادات المنتج بحسب ما تعرضه بوابة TikTok.
6. احفظ التغييرات.
7. افتح [دليل Content Posting API الرسمي](https://developers.tiktok.com/doc/content-posting-api-get-started/) في تبويب آخر واقرأ قسم **Prerequisites**. يجب أن يكون التطبيق مسجلاً، وأن يكون Content Posting API مضافاً، وأن يكون Direct Post مفعلاً، وأن يكون نطاق `video.publish` معتمداً للتطبيق.[11]

**تنبيه النشر:** التطبيقات غير المدققة قد تكون مقيدة بالنشر الخاص `SELF_ONLY` حتى تجتاز تدقيق TikTok. نجاح OAuth لا يعني أن الفيديو سيظهر للعامة.[11]

**ما يجب أن تراه:** صفحة المنتج تظهر أن Content Posting API مضاف، وDirect Post مفعّل أو في حالة انتظار مراجعة. إذا لم يظهر `video.publish`، فالتطبيق لم يحصل على الصلاحية بعد؛ لا تحاول تخمين اسم نطاق آخر.

### الخطوة 4: انسخ client key وأبقِ client secret خارج GitHub

1. من صفحة التطبيق اضغط **Settings** أو **Basic information**، أو افتح القسم الذي يعرض مفاتيح التطبيق.
2. انسخ قيمة **Client key** أو `client_key` إلى مدير كلمات المرور المؤقتاً. هذه ليست قيمة `TIKTOK_ACCESS_TOKEN`.
3. اضغط لإظهار **Client secret** أو `client_secret` وانسخه إلى مدير كلمات المرور. لا تلصقه في Issue أو ملف أو GitHub Secret لهذا المشروع؛ الأداة المحلية ستطلبه في الطرفية بإدخال مخفي.
4. لا تستخدم زر **Regenerate** إلا إذا كنت مستعداً لإبطال القيمة القديمة وإعادة تفويض التطبيق.

| الاسم | مثال آمن فقط | ما يفعله |
|---|---|---|
| `client_key` | `REPLACE_WITH_TIKTOK_CLIENT_KEY` | يحدد أي تطبيق يطلب التفويض |
| `client_secret` | `REPLACE_WITH_TIKTOK_CLIENT_SECRET` | يثبت هوية التطبيق أثناء استبدال code |
| `access_token` | `REPLACE_WITH_TIKTOK_ACCESS_TOKEN` | يسمح بطلبات Content Posting نيابة عن المستخدم |
| `refresh_token` | `REPLACE_WITH_TIKTOK_REFRESH_TOKEN` | يستخدم لتجديد access token وفق دورة TikTok |

### الخطوة 5: شغّل أداة OAuth المحلية من المشروع

هذه الخطوة تتم على جهازك المحلي، وليس داخل GitHub Actions. الأداة تفتح متصفحك، تولّد `state` وPKCE، تستقبل callback على localhost، تتحقق من `state`، ثم تستبدل code بالرموز عبر نقطة TikTok الرسمية. لا تسجل الأداة client secret أو tokens في الطرفية.

افتح Terminal أو PowerShell في مجلد المشروع الذي يحتوي على `scripts/tiktok_oauth_desktop.py`.

**macOS أو Linux:**

```bash
cd /path/to/content-factory-gha
python3 -m pip install -r requirements.txt
TIKTOK_CLIENT_KEY='REPLACE_WITH_TIKTOK_CLIENT_KEY' python3 scripts/tiktok_oauth_desktop.py
```

**Windows PowerShell:**

```powershell
Set-Location 'C:\path\to\content-factory-gha'
py -m pip install -r requirements.txt
$env:TIKTOK_CLIENT_KEY = 'REPLACE_WITH_TIKTOK_CLIENT_KEY'
py scripts\tiktok_oauth_desktop.py
```

لا تضع `client_secret` داخل الأمر. بعد تشغيل الأمر ستظهر مطالبة مثل:

```text
TikTok client secret (hidden input):
```

ألصق `client_secret` عندما تظهر المطالبة؛ لن تظهر الأحرف على الشاشة. اضغط Enter. لا تلصق `client_secret` في المثال نفسه ولا ترسله في رسالة.

بعد ذلك تفتح الأداة صفحة TikTok تلقائياً. إذا لم تفتح، انسخ رابط التفويض الذي يظهر في الطرفية والصقه في متصفحك أنت. سجل الدخول إلى **حساب TikTok الذي تريد أن ينشر المشروع باسمه**، وليس بالضرورة الحساب الذي أنشأ تطبيق Developers، ثم راجع شاشة الموافقة.

عندما ترى أن التطبيق يطلب صلاحية `video.publish`، راجع اسم التطبيق والنطاق ثم اضغط **Authorize / Allow / Agree** بحسب النص الظاهر. هذه موافقة مالك حساب TikTok، ولا يجوز تجاوزها أو قبول نطاق لم تقصده.

بعد الموافقة يعيد TikTok المتصفح إلى:

```text
http://localhost:3455/callback/?code=ONE_TIME_CODE&scopes=video.publish&state=...
```

لن تنسخ هذا الرابط. ستعرض الأداة صفحة تفيد بأن التفويض وصل، ثم ستعود إلى الطرفية وتتحقق من `state` وتستدعي نقطة token الرسمية تلقائياً.

**ما يجب أن تراه في الطرفية:**

```text
Opening TikTok authorization in your default browser...
Registered callback: http://localhost:3455/callback/
SUCCESS: token response saved locally to .tiktok/tokens.json
Granted scopes: user.info.basic,video.publish
Next: copy only access_token to GitHub Secret TIKTOK_ACCESS_TOKEN.
```

إذا لم يفتح المتصفح، اترك Terminal يعمل وافتح رابط التفويض يدوياً في متصفحك. إذا قال النظام إن المنفذ 3455 مشغول، أغلق البرنامج الذي يستخدمه ثم أعد المحاولة؛ لا تغيّر المنفذ إلا إذا غيّرت Redirect URI في TikTok أولاً.

### الخطوة 6: افهم ملف الناتج قبل نسخ القيمة

بعد النجاح ستنشئ الأداة ملفاً محلياً:

```text
.tiktok/tokens.json
```

هذا الملف مستثنى من Git عبر `.gitignore`. لا ترفعه ولا ترسله.

افتح الملف محلياً فقط. ستجد حقولاً مشابهة للآتي، لكن القيم الحقيقية يجب ألا تظهر في مستند أو سجل:

```json
{
  "access_token": "REPLACE_WITH_REAL_VALUE",
  "expires_in": 86400,
  "open_id": "REPLACE_WITH_PUBLIC_OR_INTERNAL_ID",
  "refresh_expires_in": 31536000,
  "refresh_token": "REPLACE_WITH_REAL_VALUE",
  "scope": "user.info.basic,video.publish",
  "token_type": "Bearer"
}
```

| الحقل | ماذا تفعل به؟ |
|---|---|
| `access_token` | انسخه فقط إلى GitHub Secret باسم `TIKTOK_ACCESS_TOKEN` |
| `refresh_token` | لا يقرأه المشروع الحالي تلقائياً؛ احتفظ به في مدير كلمات مرورك لتجديد access token لاحقاً |
| `open_id` | هوية TikTok الداخلية للمستخدم؛ لا تضعه في `TIKTOK_ACCESS_TOKEN` |
| `scope` | يجب أن يحتوي `video.publish` قبل محاولة النشر |
| `expires_in` | مدة صلاحية access token؛ لا تفترض أنه دائم |
| `refresh_expires_in` | مدة صلاحية refresh token؛ أعد التفويض قبل انتهائها |

### الخطوة 7: أضف access token إلى GitHub Secret الصحيح

1. افتح صفحة [GitHub Actions Secrets للمستودع](https://github.com/ysrg2003/content-factory-gha/settings/secrets/actions).
2. تأكد أن العنوان هو مستودع `ysrg2003/content-factory-gha`، وليس مستودعاً آخر.
3. ابق في تبويب **Secrets**، وليس **Variables**.
4. اضغط **New repository secret**.
5. في خانة **Name** اكتب حرفياً:

```text
TIKTOK_ACCESS_TOKEN
```

6. افتح ملف `.tiktok/tokens.json` محلياً وانسخ قيمة `access_token` فقط، أي النص بين علامات الاقتباس بعد المفتاح `access_token`. لا تنسخ علامات JSON ولا تنسخ `refresh_token`.
7. ألصق القيمة في خانة **Secret**.
8. اضغط **Add secret**.
9. النتيجة الصحيحة هي ظهور اسم `TIKTOK_ACCESS_TOKEN` في قائمة GitHub من دون ظهور قيمته.

لا تنشئ `TIKTOK_CLIENT_KEY` أو `TIKTOK_CLIENT_SECRET` أو `TIKTOK_REFRESH_TOKEN` في GitHub لهذا المشروع الحالي؛ workflow لا يقرأها. احتفظ بها محلياً فقط لتشغيل أداة OAuth وإعادة التفويض لاحقاً.

### الخطوة 8: نفّذ فحصاً قبل النشر

1. افتح تبويب **Actions** في مستودع GitHub.
2. اضغط workflow **Process and Publish Short Video**.
3. اضغط **Run workflow**.
4. في الاختبار الأول اختر `publish_tiktok=true` فقط، واترك YouTube وInstagram وFacebook على `false`.
5. اترك `allow_tiktok_browser_fallback=false`؛ لا تستخدم cookies في الاختبار الأول.
6. أدخل رابط HTTPS مباشر لفيديو MP4 تملك حق استخدامه.
7. اضغط **Run workflow** وانتظر التشغيل.

قبل النشر، يشغّل المشروع `creator_info/query` عبر نقطة TikTok الرسمية:

```text
POST https://open.tiktokapis.com/v2/post/publish/creator_info/query/
Authorization: Bearer <TIKTOK_ACCESS_TOKEN>
Content-Type: application/json; charset=UTF-8
```

لن تضع هذه القيمة في الطرفية؛ الناشر يضيفها داخلياً. النجاح يعني أن الاستجابة تحتوي حقولاً مثل `creator_username` و`privacy_level_options` و`max_video_post_duration_sec`. يستخدم المشروع الخيارات المعادة بدلاً من تخمين مستوى الخصوصية. [11] [14]

بعد الفحص، يبدأ Direct Post. إذا كان التطبيق غير مدقق، قد ترى أن الفيديو أصبح `SELF_ONLY` حتى لو اخترت عاماً؛ هذا قيد TikTok، وليس خطأ في Secret.[11]

### إذا فشل TikTok: شخّص الرسالة حرفياً

| الرسالة أو النتيجة | السبب المحتمل | التصحيح الحرفي |
|---|---|---|
| `redirect_uri_mismatch` | URI في TikTok لا يساوي URI في الأداة | اجعل القيمة في الاثنين `http://localhost:3455/callback/` حرفياً، بما في ذلك المنفذ والشرطة الأخيرة، ثم أعد OAuth |
| `invalid_client` | client key أو secret من تطبيق مختلف | افتح نفس التطبيق في Manage apps، وانسخ القيم من صفحة التطبيق الصحيح، ثم أعد الأداة |
| `invalid_grant` | code منتهي أو استُخدم مرة ثانية أو PKCE غير مطابق | شغّل الأداة من البداية ولا تعِد استخدام رابط callback القديم |
| `scope_not_authorized` | التطبيق أو التفويض لا يحتوي `video.publish` | فعّل Content Posting API وDirect Post، اطلب النطاق، ثم وافق عليه من حساب TikTok المستهدف وأعد التفويض |
| `access_token_invalid` | الرمز منتهي أو أُلغي أو نُسخ خطأ | شغّل الأداة مرة أخرى، انسخ `access_token` الجديد فقط، واستبدل GitHub Secret |
| `401` من `creator_info/query` | Token غير صالح أو لا يخص الحساب المقصود | أعد OAuth وأكد أنك سجلت الدخول بالحساب الذي تريد النشر إليه |
| `429` أو `rate_limit_exceeded` | تجاوز حد الطلبات | انتظر ولا تعِد تشغيل الحلقة بسرعة؛ الحد الحالي لـ `creator_info/query` هو 20 طلباً في الدقيقة لكل user access token.[14] |
| التطبيق يرفض النشر العام | العميل غير مدقق | اختبر النشر الخاص أولاً، ثم اتبع [صفحة تدقيق Content Posting API](https://developers.tiktok.com/application/content-posting-api) وقدّم طلب المراجعة |
| لم ينشئ `tokens.json` | الأداة لم تستلم callback | اترك Terminal مفتوحاً، استخدم متصفحاً على نفس الجهاز، وتأكد من أن المنفذ 3455 غير مشغول |

### التجديد والإلغاء

المشروع الحالي يقرأ `TIKTOK_ACCESS_TOKEN` ولا ينفذ تجديداً تلقائياً من `refresh_token`. عندما تنتهي صلاحية access token، شغّل أداة OAuth من جديد، أو نفذ تدفق التجديد الرسمي على خادم آمن باستخدام `client_key` و`client_secret` و`refresh_token`، ثم استبدل GitHub Secret.

لإلغاء وصول التطبيق، استخدم صفحة إدارة التطبيقات في TikTok أو نقطة الإلغاء الرسمية `https://open.tiktokapis.com/v2/oauth/revoke/` وفق [دليل TikTok لإدارة User Access Tokens](https://developers.tiktok.com/doc/oauth-user-access-token-management). بعد الإلغاء احذف `TIKTOK_ACCESS_TOKEN` من GitHub، واحذف ملف `.tiktok/tokens.json` محلياً، وأنشئ تفويضاً جديداً إذا أردت إعادة الاستخدام.


## 6.2 متغيرات TikTok غير السرية

| الاسم | الافتراضي | القيم/الاستخدام | التحقق أو الإصلاح |
| --- | --- | --- | --- |
| `TIKTOK_PRIVACY_LEVEL` | `PUBLIC_TO_EVERYONE` | يجب أن تكون إحدى `privacy_level_options` التي يعيدها الحساب | إذا ظهر عدم تطابق، استخدم إحدى القيم المعادة بدلاً من التخمين |
| `TIKTOK_DISABLE_DUET` | `false` | `true` أو `false` | يعطل Duet عند `true` |
| `TIKTOK_DISABLE_STITCH` | `false` | `true` أو `false` | يعطل Stitch عند `true` |
| `TIKTOK_DISABLE_COMMENT` | `false` | `true` أو `false` | يعطل التعليقات عند `true` |
| `TIKTOK_BRAND_CONTENT` | `false` | `true` عند شراكة مدفوعة | استخدمه عند انطباق الإفصاح |
| `TIKTOK_BRAND_ORGANIC` | `false` | `true` عند الترويج لنشاط المنشئ | استخدمه عند انطباق الإفصاح |

لا يضمن `PUBLIC_TO_EVERYONE` نشراً عاماً من تطبيق غير مدقق؛ هذا قيد تفرضه TikTok على العميل نفسه. [11]

## 6.3 `TIKTOK_BROWSER_COOKIES_BASE64` — البديل عالي الخطورة

**الغرض.** يعطي متصفح Playwright جلسة حساب TikTok قائم. لا يعد هذا بديلاً عن التدقيق أو OAuth، ولا ينبغي أن يكون الخيار الأول.

لا يستدعى البديل إلا إذا تحققت الشروط الثلاثة: اخترت TikTok في workflow، وفشل API الرسمي، وفعلت `allow_tiktok_browser_fallback=true`. لا تفعله في التجربة الأولى.

إذا قررت استخدامه، اجعل ملف الكوكيز JSON لقائمة cookies من **جلسة حسابك أنت**، ثم حوّله محلياً إلى Base64:

```bash
base64 -w 0 cookies.json
```

أنشئ GitHub Secret باسم `TIKTOK_BROWSER_COOKIES_BASE64` والصق الناتج. Base64 تحويل نصي وليس تشفيراً. لا ترسل ملف `cookies.json` بالبريد أو الدردشة أو Git، ولا تستخدمه على حساب لا تملكه. إذا تغيرت كلمة مرور TikTok أو انكشفت الكوكيز أو انتهت الجلسة، احذف Secret واستخرج جلسة جديدة بعد تسجيل دخولك أنت. [1]

---

# 7. متغيرات المعالجة وسير العمل

## `WHISPER_MODEL`

هذه Variable غير سرية. افتراضها `base`. استخدم اسم نموذج Whisper صالح مثل `tiny` أو `base` أو `small` أو `medium` أو `large` بحسب دقة التفريغ وزمن التشغيل الذي تقبله. النموذج الأكبر قد يحسن الدقة لكنه يستهلك وقتاً وذاكرة أكثر. إذا فشل التحميل أو تجاوز workflow الوقت، ارجع إلى `base` ثم اختبر من جديد.

## مدخلات workflow وليست Variables

عند فتح **Actions → Process and Publish Short Video → Run workflow** تظهر الحقول التالية. لا تضفها إلى GitHub Variables لأن workflow يتلقى قيمتها مع كل تشغيل.

| الحقل | مطلوب؟ | كيفية استخدامه بأمان |
| --- | ---:| --- |
| `video_url` | نعم | رابط HTTPS مباشر لملف MP4 تملك حق استخدامه؛ اختبر برابط صغير أولاً |
| `publish_youtube` | نعم | فعله فقط بعد إكمال أسرار YouTube |
| `publish_instagram` | نعم | فعله فقط بعد إعداد Meta وInstagram ID |
| `publish_facebook` | نعم | فعله فقط بعد إعداد Meta وPage ID |
| `publish_tiktok` | نعم | فعله فقط بعد إعداد TikTok OAuth |
| `allow_tiktok_browser_fallback` | نعم | اتركه `false` إلا عند فشل API الرسمي وحيازة موافقة صاحب الجلسة |
| `language` | نعم | رمز لغة Whisper؛ ابدأ بـ`ar` للفيديو العربي |

---

# 8. قائمة تحقق قبل النشر الأول

1. تأكد من ظهور أسماء الأسرار المطلوبة في GitHub من دون قيمها.
2. ابدأ بـ`AI_ROUTER_GEMINI_KEYS_JSON` أو `HF_TOKEN` واحد على الأقل، ثم شغّل workflow وتحقق من أن خطوة فحص الموجّه تعرض عداداً أكبر من صفر.
3. فعّل **منصة نشر واحدة فقط** واستخدم فيديو قصيراً تملك حق نشره.
4. في YouTube، ابدأ بـ`YOUTUBE_PRIVACY_STATUS=unlisted` إذا أردت مراجعة النتيجة قبل جعلها عامة.
5. راقب **Summary** وملفات `publish-result-*.json` داخل Artifact. لا تنسخ الأسرار إلى السجل لإصلاح خطأ.
6. عند نجاح التجربة، أضف المنصات الأخرى تدريجياً. إذا فشل أحد الناشرين، راجع جدول التشخيص في [README](../README.md#الخطوة-3-نفذ-أول-تشغيل) أو رسالة API، ولا تغير أكثر من متغير في الوقت نفسه.

## المراجع

[1]: https://docs.github.com/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions "GitHub Actions — Using secrets"
[2]: https://github.com/ysrg2003/ai-provider-router "AI Provider Router"
[3]: https://ai.google.dev/gemini-api/docs/api-key "Google Gemini API — API keys"
[4]: https://huggingface.co/docs/hub/en/security-tokens "Hugging Face — User access tokens"
[5]: https://developers.google.com/youtube/v3/docs/videos/insert "YouTube Data API — Videos: insert"
[6]: https://developers.google.com/youtube/registering_an_application "YouTube Data API — Obtaining authorization credentials"
[7]: https://developers.google.com/youtube/v3/guides/auth/installed-apps "YouTube Data API — OAuth 2.0 for installed apps"
[8]: https://developers.facebook.com/documentation/instagram-platform/overview "Meta — Instagram Platform overview"
[9]: https://developers.facebook.com/documentation/video-api/guides/reels-publishing "Meta — Facebook Reels Publishing"
[10]: https://developers.facebook.com/documentation/instagram-platform/content-publishing "Meta — Instagram Content Publishing"
[11]: https://developers.tiktok.com/doc/content-posting-api-get-started "TikTok — Content Posting API Get Started"
[12]: https://developers.tiktok.com/doc/login-kit-manage-user-access-tokens/ "TikTok — Manage User Access Tokens"
[13]: https://developers.tiktok.com/doc/login-kit-desktop/ "TikTok — Login Kit for Desktop"
[14]: https://developers.tiktok.com/doc/content-posting-api-reference-query-creator-info "TikTok — Query Creator Info"
[15]: https://developers.tiktok.com/doc/oauth-user-access-token-management "TikTok — OAuth v2 User Access Token Management"
