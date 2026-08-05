# Android Vocalizer architecture review

Date: 2026-07-28

Design a practical implementation for Max's "Android Vocalizer": agents and
Unix/Windows workers must send short text alerts over the internet to Max's
Android phone, which should immediately speak the message with Android
text-to-speech and show an acknowledgeable notification. The app should later
grow into a universal, updatable Max utility.

Constraints:

- One Android installation is strongly preferred over chaining multiple apps.
- It must work while the app is backgrounded and the screen is locked.
- Urgent alerts should be conspicuous and optionally repeat until acknowledged.
- Routine alerts should not become noisy.
- Sender integration should be a tiny authenticated HTTP or command-line call.
- Avoid a bespoke server when a mature open protocol/service can safely do the
  transport.
- App should be light themed, minimal, and updateable through a stable HTTPS
  download page initially; Play Store publishing may come later.
- Current host has no Java or Android SDK installed, but dependencies can be
  installed. An always-on Linux host is available.
- Candidate transport: ntfy (hosted or self-hosted). Candidate rapid bridge:
  ntfy plus a notification reader such as SpeakThat or MacroDroid. Candidate
  custom app: Kotlin Android client using Firebase Cloud Messaging or ntfy.

Research facts already found:

- ntfy accepts simple HTTP PUT/POST, has an Android app, urgent priorities,
  notification channels, and both Firebase and non-Firebase delivery modes.
- Firebase data messages reach FirebaseMessagingService in the background, but
  handling windows are short and Android background restrictions apply.
- Pushover emergency messages repeat until acknowledged but do not speak text.
- SpeakThat is an open-source Android app that reads notifications aloud.

Return a concise recommendation with:

1. Best MVP and best long-term architecture.
2. Whether to build a custom app now or configure existing apps first.
3. Exact component boundaries and security model.
4. Android background-delivery pitfalls and mitigations.
5. A bounded version-01 build scope and verification checklist.

Do not include credentials. Do not assume access to proprietary APIs.
