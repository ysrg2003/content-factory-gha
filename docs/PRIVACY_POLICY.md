# Privacy Policy

**Effective date:** 2026-08-14

This Privacy Policy describes how the Social Media Publisher project available at [the project repository](https://github.com/ysrg2003/social-media-publisher) processes information when an authorized user runs its automation workflow.

> **Important notice.** This is an operational draft prepared for the project’s developer-portal configuration. It is not legal advice. Review it with a qualified attorney and adapt it to your actual operating entity, jurisdiction, users, and deployment before relying on it as a complete legal notice.

## 1. Who controls the processing

The person or organization that owns and runs the repository and connects the external accounts controls the workflow configuration and the content submitted through it. The repository is public, but credentials and workflow inputs must not be published in the repository.

For project questions, use the [public repository issue tracker](https://github.com/ysrg2003/social-media-publisher/issues). Do not put passwords, tokens, private video links, or personal information in an issue.

## 2. Information the workflow may process

Depending on the options selected for a run, the workflow may process the following categories:

| Category | Examples | Why it is needed |
| --- | --- | --- |
| Video and media | A direct MP4 URL, downloaded source video, converted vertical video, subtitle file, audio transcript | To transform the supplied media and prepare a publication |
| Generated metadata | Title, description, hashtags, language, translation, AI-content label | To prepare the information sent to selected platforms |
| Account and platform identifiers | YouTube channel context, Meta Page or Instagram account ID, TikTok open ID or creator information | To direct an authorized publication to the intended account |
| Credentials | API keys, OAuth client configuration, access tokens, refresh tokens | To authenticate with a provider; these must remain in secret storage |
| Technical records | Workflow run ID, timestamps, status, error messages, model/provider identifiers, limited rate or quota responses | To diagnose failures and prevent repeated work |
| Optional browser session | TikTok browser cookies when the explicitly enabled fallback is used | To access an account session in the fallback path; this is high-risk and disabled by default |

The project does not intentionally require your personal photograph, contact list, unrelated files, or unrelated account passwords. A connected platform may nevertheless process information under its own privacy notice when you authorize an API request or publish content.

## 3. How processing works

The workflow runs on GitHub Actions when you manually start it and choose a direct video URL and destination platforms. FFmpeg and Whisper process the media inside the workflow runner. The AI Provider Router may send prompts or metadata-generation inputs to the AI provider selected by its configured chain, such as Gemini or Hugging Face. The selected YouTube, Meta, or TikTok API may then receive the media and publication metadata required by that platform.

The exact provider and destination depend on the secrets and workflow inputs you configure. A platform is not contacted merely because its credentials exist; it is contacted when its publication input is enabled for the run.

## 4. Third-party recipients

Information may be processed by the following categories of recipients when you enable the corresponding integration:

| Recipient | Data that may be sent | Where to read its rules |
| --- | --- | --- |
| GitHub Actions | Workflow inputs, build artifacts, logs, and repository configuration | [GitHub Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement) |
| Configured AI provider through AI Provider Router | Metadata-generation prompt, transcript or summarized content, and model request data | [Google Gemini API terms](https://ai.google.dev/gemini-api/terms) and [Hugging Face privacy policy](https://huggingface.co/privacy) |
| YouTube Data API | Video, title, description, tags, and selected YouTube settings | [Google Privacy Policy](https://policies.google.com/privacy) |
| Meta APIs | Reel media, caption, and selected account/page publication data | [Meta Privacy Policy](https://www.facebook.com/privacy/policy/) |
| TikTok APIs | Reel/video media, caption, creator authorization, and publication settings | [TikTok Privacy Policy](https://www.tiktok.com/legal/privacy-policy) |

A provider may process data in other countries, retain it under its own policy, or reject content under its own moderation and security rules. Review the linked provider documents before sending confidential, regulated, or personal data.

## 5. Credentials and security

Credentials are stored in GitHub Actions Secrets or in a local ignored file during a one-time OAuth setup. They must never be committed, pasted into an issue, placed in a workflow log, or included in a screenshot. The workflow is designed to pass secrets to the relevant process without printing their values.

The TikTok desktop OAuth helper writes a local token response to `.tiktok/tokens.json`; that directory is excluded by `.gitignore`. The project currently consumes `TIKTOK_ACCESS_TOKEN` for the official TikTok publisher and does not automatically refresh it from `refresh_token`. The owner must rotate or revoke a credential immediately after suspected exposure.

The TikTok browser-cookie fallback is disabled by default. If enabled, a cookie or session file may provide account-equivalent access and must be treated as a password. It must be used only for an account owned or controlled by the operator and must be deleted and revoked when no longer necessary.

## 6. Retention and deletion

The workflow keeps generated files and the AI Router state database in a GitHub Actions Artifact with the retention configured by the workflow, currently one day unless GitHub or repository settings impose a different limit. GitHub may retain workflow logs under its own policies. Local downloads, token files, cookies, and temporary media should be deleted by the operator after the run and must not be committed.

A user who wants to stop processing can disable the workflow, delete its artifacts, remove the relevant GitHub Secrets, revoke provider authorizations, and delete the repository or local working files. Deleting a local file does not revoke a token that was already issued; revoke the token at its provider.

## 7. User choices and rights

The operator chooses which platforms to enable, which video to submit, which AI provider chain to use, and whether to publish. The operator should not submit another person’s personal data or media without a lawful basis and the necessary permissions. Requests concerning access, correction, deletion, objection, or other privacy rights should be directed to the person or organization that operates the repository, subject to applicable law and the policies of the relevant provider.

## 8. Children and sensitive information

Do not submit sensitive personal information, children’s data, health information, financial information, government identifiers, or confidential business information unless you have a lawful basis, appropriate safeguards, and the necessary disclosures. The project is not represented as a service designed for children.

## 9. Changes to this Policy

An updated version will be published in this repository with a new effective date. The operator should review the policy whenever the workflow adds a provider, changes data retention, adds a new destination, or changes the way credentials are handled.

## References

- [Project repository](https://github.com/ysrg2003/social-media-publisher)
- [GitHub Actions — Using secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)
- [Google Gemini API terms](https://ai.google.dev/gemini-api/terms)
- [Hugging Face privacy policy](https://huggingface.co/privacy)
- [YouTube Data API policies](https://developers.google.com/youtube/terms/api-services-terms-of-service)
- [Meta Privacy Policy](https://www.facebook.com/privacy/policy/)
- [TikTok Privacy Policy](https://www.tiktok.com/legal/privacy-policy)
