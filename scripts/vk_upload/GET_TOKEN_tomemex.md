# Getting the VK access token | 2026-05-04

Token is needed once. With `offline` scope it does not expire.

## Step 1 — pick a client_id (VK app)
The new dev.vk.com app-creation flow was broken at time of writing (404 on `/admin/apps`). Two paths:

A. **Try the new dashboard again** at https://dev.vk.com — sign in, look for "Создать приложение" / "Create app", choose Standalone. Copy the numeric Application ID.

B. **Fallback (commonly used for personal scripts):** use a known public Standalone client_id such as VK Admin (`6121396`) or Kate Mobile (`2685278`). These are widely used by hobby tools but are technically third-party apps; only do this for your own personal automation, never redistribute.

## Step 2 — implicit OAuth flow
Open this URL in a browser logged in as the VK account that admins club tamza:

```
https://oauth.vk.com/authorize?client_id=CLIENT_ID&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=video,groups,wall,offline&response_type=token&v=5.199
```

Replace `CLIENT_ID`. Click "Allow". The browser redirects to a blank page; copy the value of `access_token=` from the URL bar.

`expires_in=0` because of the `offline` scope = permanent until you revoke.
The `wall` scope is required for the standard `wallpost=1` upload workflow.

## Step 3 — save token
Save as one line, no quotes:
```
C:\Users\maxre\Nextcloud\zSyncMain\ssh\vk_user_token.txt
```

## Step 4 — find community id
Open https://vk.com/clubtamza, click any video. URL contains `video-XXXXXXX_...`. The number after `video-` is the group id (positive integer in our usage).

Save:
```
C:\Users\maxre\Nextcloud\zSyncMain\ssh\vk_group_id.txt
```

## Test
```
python vk_upload.py C:\path\to\sample.mp4 --title "test"
```
