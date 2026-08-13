# إعداد الأسرار والمنصات

## قبل البدء

أضف القيم من مستودع **`ysrg2003/content-factory-gha`** عبر **Settings → Secrets and variables → Actions**. هذا المستودع عام؛ لذلك لا تحفظ مفاتيح API أو JSON OAuth أو الكوكيز في أي ملف داخل المشروع.

> هذا الملف ملخص تشغيلي. قبل إنشاء أي قيمة، اتبع **[دليل الاعتمادات والمتغيرات الكامل](CREDENTIALS.md)**؛ فهو يقدم رابط كل مزود، الأذونات والنطاقات، خطوات الإنشاء، صيغة التخزين، اختبار النجاح، وإجراء التدوير أو الإلغاء.

ابدأ بإعداد **AI Provider Router** أولاً، لأن النشر لا يبدأ قبل نجاح توليد بيانات الفيديو الوصفية. بعد ذلك أضف أسرار كل منصة تريد تفعيلها فقط.

## 1. أسرار الذكاء الاصطناعي

| السر | مطلوب؟ | المصدر | الصيغة |
| --- | --- | --- | --- |
| `AI_ROUTER_GEMINI_KEYS_JSON` | اختياري | Google AI Studio أو Google Cloud | مصفوفة JSON لمفاتيح Gemini مرتبة |
| `AI_ROUTER_HF_KEYS_JSON` | اختياري | Hugging Face | مصفوفة JSON لمفاتيح Hugging Face مرتبة |
| `HF_TOKEN` | اختياري | Hugging Face | Token واحد بصلاحية Inference Providers؛ بديل عن المصفوفة |

يلزم واحد على الأقل من الأسرار الثلاثة أعلاه. لا يوجد `OPENAI_API_KEY` في هذا المشروع: كل طلب ذكاء اصطناعي يمر عبر AI Provider Router.

اقرأ **[دليل تكامل AI Provider Router](AI_ROUTER_INTEGRATION.md)** قبل إدخال القيم، لأنه يشرح ترتيب النماذج والبدائل وصيغة JSON الصحيحة وطريقة اختبار الإعداد دون كشف السر.

## 2. أسرار النشر

| السر | مطلوب لـ | القيمة أو مصدرها |
| --- | --- | --- |
| `YOUTUBE_CLIENT_SECRET_JSON` | YouTube Shorts | المحتوى الكامل لملف OAuth client من Google Cloud، بصيغة JSON |
| `YOUTUBE_REFRESH_TOKEN` | YouTube Shorts | Refresh Token للقناة المفوضة بنطاق `youtube.upload` |
| `META_PAGE_ACCESS_TOKEN` | Instagram وFacebook | Page Access Token بصلاحيات النشر المناسبة |
| `META_INSTAGRAM_ACCOUNT_ID` | Instagram Reels | معرف الحساب الاحترافي المرتبط بالصفحة |
| `META_FACEBOOK_PAGE_ID` | Facebook Page Reels | معرف الصفحة التي ستنشر عليها |
| `TIKTOK_ACCESS_TOKEN` | TikTok الرسمي | User access token بنطاق `video.publish` |
| `TIKTOK_BROWSER_COOKIES_BASE64` | بديل TikTok فقط | ملف JSON للكوكيز مشفر بـBase64؛ لا يستخدم افتراضياً |

## 3. متغيرات الاختيار

أضف هذه القيم من قسم **Variables** نفسه. غياب أي قيمة يفعّل الافتراضي الموضح.

| المتغير | الافتراضي | المعنى |
| --- | --- | --- |
| `AI_ROUTER_CHAIN` | `creative` | سلسلة الذكاء الاصطناعي: `creative` أو `cheap` أو `default` |
| `WHISPER_MODEL` | `base` | نموذج Whisper المستخدم للتفريغ |
| `YOUTUBE_PRIVACY_STATUS` | `public` | `public` أو `unlisted` أو `private` |
| `YOUTUBE_CATEGORY_ID` | `22` | فئة فيديو YouTube |
| `YOUTUBE_MADE_FOR_KIDS` | `false` | حدده `true` فقط عند انطباق سياسة المحتوى الموجه للأطفال |
| `META_GRAPH_VERSION` | `v26.0` | إصدار Meta Graph API |
| `TIKTOK_PRIVACY_LEVEL` | `PUBLIC_TO_EVERYONE` | يجب أن يظهر ضمن خيارات خصوصية الحساب التي تعيدها TikTok |
| `TIKTOK_DISABLE_DUET` | `false` | منع Duet عند ضبطه إلى `true` |
| `TIKTOK_DISABLE_STITCH` | `false` | منع Stitch عند ضبطه إلى `true` |
| `TIKTOK_DISABLE_COMMENT` | `false` | منع التعليقات عند ضبطه إلى `true` |
| `TIKTOK_BRAND_CONTENT` | `false` | إفصاح الشراكة المدفوعة إن انطبق |
| `TIKTOK_BRAND_ORGANIC` | `false` | إفصاح الترويج لنشاط المنشئ إن انطبق |

## 4. تفويض كل منصة

### YouTube Shorts

أنشئ OAuth client في Google Cloud، ثم أكمل مرة واحدة تفويض القناة التي ستنشر عليها. خزّن JSON العميل في `YOUTUBE_CLIENT_SECRET_JSON` وRefresh Token في `YOUTUBE_REFRESH_TOKEN`. يستخدم الناشر واجهة `videos.insert` الرسمية لرفع الفيديو وتحديد العنوان والوصف والخصوصية. [1]

### Instagram Reels وFacebook Page Reels

اربط حساب Instagram احترافي بصفحة Facebook، ثم أعد تطبيق Meta للنشر. يتطلب نشر Instagram الأذونات المناسبة لمسار تسجيل الدخول الذي تستخدمه؛ ويتطلب نشر Facebook Page Reels Page Access Token ومهمة `CREATE_CONTENT` والأذونات `pages_show_list` و`pages_read_engagement` و`pages_manage_posts`. [2] [3]

### TikTok

أنشئ تطبيق TikTok وفعل **Content Posting API — Direct Post** ثم احصل على تفويض المستخدم بنطاق `video.publish`. يقرأ الناشر خيارات الخصوصية من الحساب ولا يقبل قيمة ليست ضمن الخيارات المعادة. تطبيق غير مدقق لا يستطيع النشر العلني عبر Direct Post؛ أكمل تدقيق TikTok عند الحاجة للنشر العام. [4]

### بديل TikTok المتصفحي

هذا خيار طوارئ فقط. لتفعيله يجب أن تضع `TIKTOK_BROWSER_COOKIES_BASE64` وتختار `allow_tiktok_browser_fallback=true` عند تشغيل workflow، كما يجب أن يفشل مسار TikTok الرسمي أولاً. لتكوين قيمة الـ Secret محلياً من ملف كوكيز JSON:

```bash
base64 -w 0 cookies.json
```

النتيجة هي نص طويل تلصقه كـGitHub Secret. لا تضع ملف `cookies.json` في المستودع، ولا تشارك محتواه. استبدل الكوكيز فور تغيير كلمة المرور أو الاشتباه في وصول غير مصرح به.

## 5. تحقق قبل أول نشر

ابدأ بفيديو تملكه ومنصة واحدة فقط. افتح **Actions → Process and Publish Short Video → Run workflow**، أدخل رابط MP4 مباشر، واترك `allow_tiktok_browser_fallback=false` في التجربة الأولى.

النتيجة المتوقعة هي نجاح خطوة **Process video, transcribe, and write metadata** ثم ظهور نتيجة المنصة في Summary. إذا فشلت خطوة المعالجة، افحص قسم **استكشاف الأخطاء** في [دليل AI Provider Router](AI_ROUTER_INTEGRATION.md#استكشاف-الأخطاء). إذا فشلت منصة نشر لاحقاً، ستستمر بقية خطوات النشر ويسجل Summary نتيجة مستقلة لكل منصة.

## أمن الأسرار والاسترداد

لا تعرض قيمة Secret في السجل ولا تضفها إلى ملف أو commit أو screenshot. إذا انكشف سر، ألغِه من مزوده، أنشئ بديلاً، ثم حدّث GitHub Secret. لا يكفي حذف النص من README أو من آخر commit فقط.

## المراجع

[1]: https://developers.google.com/youtube/v3/docs/videos/insert "Google — YouTube Videos: insert"
[2]: https://developers.facebook.com/documentation/instagram-platform/content-publishing "Meta — Instagram Content Publishing"
[3]: https://developers.facebook.com/documentation/video-api/guides/reels-publishing "Meta — Facebook Reels Publishing"
[4]: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post "TikTok — Content Posting API Direct Post"
