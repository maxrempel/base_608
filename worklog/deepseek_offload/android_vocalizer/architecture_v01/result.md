## Recommendation: Android Vocalizer

### 1. Best MVP & Best Long-Term Architecture

| Phase | Architecture | Components |
|-------|--------------|------------|
| **MVP** (immediate) | **Existing apps configured** → no custom build | **ntfy Android app** (subscribe to topic) + **MacroDroid** (trigger TTS & notification on ntfy alert) |
| **Long-term** | **Custom Kotlin app** with ntfy direct integration + self-hosted ntfy server on your Linux box | Sender: `curl -u token: -H "Priority: urgent" -d "msg" https://ntfy.example.com/topic`<br>App: foreground service → ntfy WebSocket → TTS & notification |

### 2. Build Custom App Now or Configure Existing Apps?

**Start with existing apps** (MVP in < 1 hour):  
- Install ntfy Android app (set topic, enable "Create notification")  
- Install MacroDroid (free) → trigger on ntfy notification → action: speak text + show custom notification  
- No Java/SDK needed. Works background/locked if phone’s battery optimisation exempted.  

**Build custom app later** (within 2–3 days after SDK installed) when you need:  
- Reliable urgent acknowledge (repeating until ack)  
- Unified UI, updateable via HTTPS download  
- No dependency on third-party macro apps  

### 3. Component Boundaries & Security Model

```
Sender (agent/worker) ─── HTTPS ───> ntfy server (self‑hosted or ntfy.sh)
                                          │
                                    WebSocket / FCM
                                          │
                               Android Custom App
                              ┌─────────────────────┐
                              │ Foreground Service   │
                              │  (ntfy subscriber)   │
                              │  + TTS engine        │
                              │  + Notification Mgr  │
                              └─────────────────────┘
```

**Security**:  
- Sender authenticates via ntfy topic token (bearer token in header)  
- Server uses **HTTPS only** (Let’s Encrypt on self-hosted)  
- Topic name is effectively a shared secret – generate a long random string per sender  
- No additional auth in app (it simply connects to the topic)  

### 4. Android Background-Delivery Pitfalls & Mitigations

| Pitfall | Mitigation |
|---------|------------|
| **Doze mode** – app stopped after screen off | Use **foreground service** with persistent low‑priority notification (e.g. “Vocalizer is running”) – exempt from doze during active foreground. |
| **Battery optimisation** kills service | Prompt user to disable battery optimisation for the app at first launch (Settings → Special access → Battery optimisation → don’t optimise). |
| **FCM data messages** – 10–20s execution limit | Switch to **ntfy’s WebSocket** inside the foreground service – keeps persistent connection, no short window. |
| **Screen locked** – TTS may not play | Use **`AudioAttributes.USAGE_ALARM`** for TTS and `FLAG_INSISTENT` + `CATEGORY_ALARM` for urgent notifications. Request `WAKE_LOCK` briefly. |
| **Multiple alerts stack** – noisy | Use **Notification Channels**: one for “routine” (low priority, no sound) and one for “urgent” (high priority, alarm sound, full‑screen intent). |

### 5. Version-01 Build Scope & Verification Checklist

**Build Scope** (custom Kotlin app, first release):  
- Single activity to show settings (topic, token, toggle urgent)  
- Foreground service with ntfy WebSocket client (use `io.ntfy:ntfy-android-client`)  
- Receive message → extract priority + text  
- Urgent: speak with `TextToSpeech` (alarm stream), show full‑screen notification that starts a “dismiss activity” – repeats every 30s until user taps “Acknowledge”  
- Routine: speak but no repeat, small notification  
- Notification channel for each priority  
- Update mechanism: app downloads APK from static HTTPS URL (e.g. `https://your-server/vocalizer.apk`) – manual install dialog (no auto‑update)  

**Verification Checklist** (test on Android 10/11/12/13/14):  
- [ ] Sender’s `curl` command reaches app (display “Hello World”)  
- [ ] App speaks the text while screen off & locked  
- [ ] Urgent message shows notification with `answer action` – tapping “Ack” stops repeats  
- [ ] Routine message shows silent notification, no repeat  
- [ ] No play store dependency – app can be installed via downloaded APK  
- [ ] Doze mode: after 30 min idle, app still speaks a new alert  
- [ ] Battery optimisation prompt appears and works  
- [ ] App survives phone reboot (foreground service restart with `START_STICKY`)
