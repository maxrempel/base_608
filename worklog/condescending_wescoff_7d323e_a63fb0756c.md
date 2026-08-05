
## [2026-06-21 17:28] ? 80aeca4e
- DID: Grew maxrempel.com /media press-photo gallery to 9 photos; replaced celestial w/ cel_fix; per-image crops to R2 + card/manifest in live D1 page (slug media)
- STATE: Gallery live: max-alien,lab,celestial,shaman,starship,titan,titan2,artbg(vert),artbg-a. Worker /img not edge-cached so R2 overwrite shows instantly. CF zone token lacks purge perm.
- NEXT: Add more photos as Max sends paths via make_press_photo.py <src> <slug> then 2 D1 replaces (card+manifest), verify, commit+merge+push

## [2026-06-22 07:22] ? 80aeca4e
- DID: maxrempel.com /media gallery now 11 photos (lab-selfie first w/ v15, v4 last, celestial fixed); each photo = make_press_photo.py crops to R2 + 2 D1 replaces (card+manifest) on live page
- STATE: Gallery live+pushed. Now starting a NAV change: move Russian menu item to last + normalize its font (currently styled differently)
- NEXT: Find nav item defs in src (config/index), move Russian last, drop its special font class, build+deploy worker, verify
