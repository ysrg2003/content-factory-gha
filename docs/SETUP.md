# إعداد النشر المباشر

أضف القيم التالية من صفحة **Settings → Secrets and variables → Actions** في المستودع. لا تضفها إلى Git أو Issue أو وصف تشغيل؛ المستودع عام.

## الأسرار

| الاسم | مطلوب لـ | القيمة المطلوبة |
| --- | --- | --- |
| `OPENAI_API_KEY` | معالجة كل فيديو | مفتاح مزود OpenAI لتوليد البيانات الوصفية العربية |
| `YOUTUBE_CLIENT_SECRET_JSON` | YouTube | محتوى JSON لعميل OAuth 2.0 من Google Cloud، كسطر واحد كامل |
| `YOUTUBE_REFRESH_TOKEN` | YouTube | Refresh Token تفويض القناة بنطاق `youtube.upload` |
| `META_PAGE_ACCESS_TOKEN` | Instagram / Facebook | رمز وصول للصفحة لديه صلاحيات النشر المطلوبة |
| `META_INSTAGRAM_ACCOUNT_ID` | Instagram | معرّف الحساب الاحترافي على Instagram |
| `META_FACEBOOK_PAGE_ID` | Facebook | معرّف صفحة Facebook المراد النشر عليها |
| `TIKTOK_ACCESS_TOKEN` | TikTok الرسمي | رمز وصول المستخدم الذي يتضمن نطاق `video.publish` |
| `TIKTOK_BROWSER_COOKIES_BASE64` | بديل TikTok فقط | JSON للكوكيز، مشفّر بـBase64، ولا يُقرأ إلا إذا فشل API وفُعّل البديل |

## المتغيرات الاختيارية

| الاسم | القيمة الافتراضية | الاستخدام |
| --- | --- | --- |
| `OPENAI_MODEL` | `gpt-4.1-mini` | نموذج توليد النصوص |
| `WHISPER_MODEL` | `base` | نموذج تفريغ الصوت؛ يمكن اختيار نموذج أكبر مقابل وقت تشغيل أطول |
| `YOUTUBE_PRIVACY_STATUS` | `public` | `public` أو `unlisted` أو `private` |
| `YOUTUBE_CATEGORY_ID` | `22` | فئة فيديو YouTube |
| `YOUTUBE_MADE_FOR_KIDS` | `false` | `true` عند انطباق سياسة المحتوى الموجّه للأطفال |
| `META_GRAPH_VERSION` | `v26.0` | إصدار Graph API المعتمد في سكربت Meta |
| `TIKTOK_PRIVACY_LEVEL` | `PUBLIC_TO_EVERYONE` | يجب أن يطابق اختياراً معاداً من TikTok لحساب المنشئ |
| `TIKTOK_DISABLE_DUET` | `false` | منع Duet عند ضبطه إلى `true` |
| `TIKTOK_DISABLE_STITCH` | `false` | منع Stitch عند ضبطه إلى `true` |
| `TIKTOK_DISABLE_COMMENT` | `false` | منع التعليقات عند ضبطه إلى `true` |
| `TIKTOK_BRAND_CONTENT` | `false` | الإفصاح عن شراكة مدفوعة، عند انطباقها |
| `TIKTOK_BRAND_ORGANIC` | `false` | الإفصاح عن الترويج لنشاط المنشئ، عند انطباقه |

## تفويض المنصات

### YouTube

أنشئ عميل OAuth في Google Cloud، وأكمل مرة واحدة تدفق تفويض المستخدم للقناة التي ستنشر عليها، ثم خزّن Refresh Token الناتج. يستخدم الناشر نطاق `https://www.googleapis.com/auth/youtube.upload` فقط. واجهة `videos.insert` هي الواجهة الرسمية لرفع الفيديو وتضبط العنوان والوصف والخصوصية. [1]

### Instagram وFacebook

اربط حساب Instagram الاحترافي بصفحة Facebook، وأنشئ تطبيق Meta مهيأ للنشر. يحتاج نشر Instagram إلى الصلاحيات `instagram_business_basic` و`instagram_business_content_publish` عند مسار Instagram Login، أو الصلاحيات النظيرة لمسار Facebook Login. أما نشر Facebook Page Reels فيحتاج Page Access Token ومهمة `CREATE_CONTENT` والأذونات `pages_show_list` و`pages_read_engagement` و`pages_manage_posts`. [2] [3]

### TikTok

أنشئ تطبيق TikTok، وفعّل **Content Posting API — Direct Post**، ثم احصل على تفويض مستخدم بنطاق `video.publish`. يجب أن يتحقق الناشر من خيارات الخصوصية التي يعيدها الحساب ويحترمها. النشر العلني من تطبيق غير مدقّق مقيّد من TikTok؛ يلزم تدقيق التطبيق لرفع هذا القيد. [4]

### البديل المتصفحي لـ TikTok

هذا الخيار موجود كـ **خطة احتياطية فقط**. لا يستدعى إلا مع الشروط الثلاثة التالية: تم اختيار TikTok، وفشل ناشر TikTok الرسمي، وفُعّل `allow_tiktok_browser_fallback` في نموذج التشغيل. لا تطبع الكوكيز في السجل ولا تحفظها في المستودع. يمكنك توليد القيمة محلياً من ملف JSON للكوكيز ثم لصق الناتج في GitHub Secret:

```bash
base64 -w 0 cookies.json
```

> احذف الكوكيز واستبدلها فوراً عند تغيير كلمة المرور أو الاشتباه في وصول غير مصرح به. لا يمكن لهذا المستودع تجاوز تدقيق TikTok أو سياسات المنصة.

## تشغيل أول آمن

في التشغيل الأول، فعّل منصة واحدة فقط. استخدم فيديو قصيراً تجريبياً تملك حقوقه، وراجع ملخص التشغيل وروابط النتائج. بعد نجاح التفويض والإعداد، يمكنك تفعيل كل المنصات في تشغيل واحد. لا توجد أي خطوة تليجرام أو موافقة مرحلية في هذا المشروع.

## المراجع

[1]: https://developers.google.com/youtube/v3/docs/videos/insert "Google — YouTube Videos: insert"
[2]: https://developers.facebook.com/documentation/instagram-platform/content-publishing "Meta — Instagram Content Publishing"
[3]: https://developers.facebook.com/documentation/video-api/guides/reels-publishing "Meta — Facebook Reels Publishing"
[4]: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post "TikTok — Content Posting API Direct Post"
