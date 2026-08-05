# vk_upload — VK community video uploader

CLI tool. Uploads a local video file to a VK community via the official VK API (`video.save` + multipart POST to the returned upload URL).

## Files
- `vk_upload.py` — the script (v01)
- `GET_TOKEN_tomemex.md` — one-time setup: how to obtain the access token

## Usage
```
python vk_upload.py <file> --title "Title" [--desc "..."] [--group-id N]
                   [--token-file PATH] [--no-wall]
```

## Defaults
- token-file: `C:\Users\maxre\Nextcloud\zSyncMain\ssh\vk_user_token.txt` (one line, just the token)
- group id:   `C:\Users\maxre\Nextcloud\zSyncMain\ssh\vk_group_id.txt` (one line, positive integer)
- api version: 5.199

## Required token scopes
`video`, `groups`, `offline`

## Returns
On success prints the public URL `https://vk.com/video{owner_id}_{video_id}`. Exit code 0.

## Exit codes
- 0 ok
- 2 missing/empty file or token
- 3 VK API error (json on stderr)
- 4 upload server HTTP error
