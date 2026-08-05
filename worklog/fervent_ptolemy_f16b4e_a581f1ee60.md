
## [2026-06-18 14:33] ? f0883cf5
- DID: Set up access to AstolfoDebian (asto), Liz's PC = aux compute node. Installed Tailscale on Pine, joined 'rempel house' tailnet via Max's GITHUB login. Saved bitwarden_ed25519 key + creds. SSH works over tailscale (rempel@astolfodebian.tail251d88.ts.net, 4ms).
- STATE: asto reachable. Specs: i5-12600K 16T, 31GB RAM, ~1TB free btrfs, Radeon RX6650XT now detected (GPU re-seated by Max). rempel in sudo group but host sudo needs pw; per Liz use distrobox(Fedora) for root. Creating fedora distrobox container now (bg).
- NEXT: Confirm container created + sudo dnf works inside. Then asto ready for python/transcription/video/genomics jobs.
