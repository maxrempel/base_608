# Restream API — recording download notes | 2026-05-04

Source: Max's research, Restream Developer Portal (launched Apr 2026).

## Endpoints
- List recordings for an event: `GET /events/{eventId}/recordings`
  - Returns primary videos, secondary videos, audio files
  - Scope: `storage.read`
  - Doc: https://developers.restream.io/events/events-recordings
- Get temporary download URL for a file: `GET /events/recordings/download-url`
  - Pass the `fileName` from the recordings endpoint
  - Doc: https://developers.restream.io/events/events-recording-download-url
- Storage management (list/delete) also available via API.

## Auth
- OAuth, scope `storage.read`
- Credentials at https://developers.restream.io

## Use case
- Auto-sync recordings to external storage on schedule (Restream storage has size cap).
- Exactly the bulk-download workflow we'd want for the weekly mirror.

## Status
- Not yet built. Currently using yt-dlp from Odysee/YouTube as the source.
- Revisit if/when we want a direct path that skips re-encoding by the upload sites.
