# مصنع المحتوى المباشر

يعالج هذا المستودع رابط فيديو MP4، يحوّله إلى فيديو عمودي بدقة **1080×1920** مع ترجمة عربية مدمجة، وينشئ بيانات وصفية منظمة، ثم ينشره مباشرة إلى المنصات التي تختارها في تشغيل واحد. لا يحتوي المشروع على تليجرام، ولا على رسالة معاينة، ولا على مرحلة موافقة بين المعالجة والنشر.

> **النشر فوري.** عند تفعيل منصة في نموذج التشغيل وإعداد أسرارها، يُنفّذ النشر إليها بعد انتهاء المعالجة. لا تستخدم المشروع على محتوى لا تملك حق نشره.

## مسار التنفيذ

```text
رابط MP4 → FFmpeg + Whisper → ترجمة مدمجة + metadata.json
                                  ├─ YouTube Shorts (API رسمي)
                                  ├─ Instagram Reels (API رسمي)
                                  ├─ Facebook Page Reels (API رسمي)
                                  └─ TikTok Direct Post (API رسمي)
                                          └─ بديل متصفح معزول، عند فشل API فقط واختياره صراحة
```

| الوجهة | المسار الافتراضي | نتيجة التنفيذ |
| --- | --- | --- |
| YouTube Shorts | `videos.insert` مع OAuth 2.0 | ملف `publish-result-youtube.json` ومعرف الفيديو |
| Instagram Reels | حاوية وسائط ثم رفع قابل للاستئناف ثم `media_publish` | ملف `publish-result-meta.json` ومعرف Reel |
| Facebook Page Reels | بدء جلسة رفع ثم رفع الملف ثم `video_reels` finish | ملف `publish-result-meta.json` ومعرف الفيديو |
| TikTok | Content Posting API مع `FILE_UPLOAD` | ملف `publish-result-tiktok.json` وحالة `publish_id` |
| TikTok — احتياطي | متصفح Chromium بكوكيز مشفّرة | يعمل فقط إن فشل المسار الرسمي وفُعِّل الحقل الاحتياطي |

## التشغيل

افتح تبويب **Actions** في المستودع، واختر **Process and Publish Short Video** ثم اضغط **Run workflow**. أدخل رابط HTTPS مباشر للفيديو الخام، واختر المنصات المطلوب النشر عليها. تفعيل خيار `allow_tiktok_browser_fallback` يجعل البديل المتصفحي متاحاً فقط إذا أخفق نشر TikTok عبر الواجهة الرسمية.

ينتج التنفيذ ملخصاً في صفحة التشغيل، ويحفظ الفيديو المعالج والترجمة وملف البيانات الوصفية كـ Artifact لمدة يوم واحد فقط. هذا ليس تخزيناً دائماً للوسائط.

## متطلبات الفيديو

ينبغي أن يكون الرابط المدخل قابلاً للتنزيل مباشرة بصيغة MP4. يحوّل النظام الفيديو إلى H.264/AAC، ويحافظ على نسبة 9:16. توصي Meta لفيديوهات Facebook Reels بدقة 1080×1920، بنسبة 9:16، ومدة بين 3 و90 ثانية. [1]

## الإعداد الأولي

راجع [دليل الإعداد](docs/SETUP.md) لإضافة الأسرار والمتغيرات اللازمة. لا تضع أي مفتاح أو ملف OAuth أو كوكيز في ملفات المشروع؛ فالمستودع عام.

## ملاحظات مهمة

لا تكون دقائق GitHub Actions للمستودعات الخاصة مجانية بلا حد، لكن تشغيل الـ runners القياسية للمستودعات العامة مجاني وفق وثائق GitHub. ما زال تخزين Artifacts وتكوين الحصة يخضعان لسياسات المنصة، لذلك حُدد الاحتفاظ بيوم واحد. [2]

يرفع TikTok المنشورات العلنية عبر Direct Post فقط للتطبيقات التي اجتازت مراجعة المنصة؛ التطبيقات غير المدققة مقيدة بالنشر الخاص. يُفضّل إبقاء الواجهة الرسمية هي المسار الأساسي، واستخدام البديل المتصفحي فقط عند الحاجة وبمسؤولية صاحب الحساب. [3]

## المراجع

[1]: https://developers.facebook.com/documentation/video-api/guides/reels-publishing "Meta — Reels Publishing API"
[2]: https://docs.github.com/en/billing/concepts/product-billing/github-actions "GitHub Actions billing"
[3]: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post "TikTok — Direct Post"
