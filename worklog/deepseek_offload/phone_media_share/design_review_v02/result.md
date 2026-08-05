Security gaps:
- No TLS: token and media are sent cleartext over the LAN; sniffing/ARP spoofing can expose both.
- Token is bearer-only and apparently non-expiring; if leaked via logs, browser history, or other paths, there is no revocation/reissue control.
- Binding a private IPv4 is not a security boundary; any LAN host can attempt access. No mention of host firewall rules or client IP allowlisting.

Compatibility gaps:
- "96 kbps AAC" is incomplete without specifying container (e.g., MP4/MKV) and output video codec. Some client players require fragmented MP4 for seeking/streaming; otherwise byte-range seeks may not work as expected.
- Byte-range support is not fully specified: multi-range requests, `If-Range`, and correct 206/416 responses are common failure points and should be explicitly tested with a real player seeking into the file.

Verification gaps:
- Tests covered local and one second LAN machine only; no verification across reboot, DHCP lease change/adapter reset, Windows Firewall profile changes, or multiple concurrent clients.
- PID/state robustness is unproven: stale PID files from unclean exits can point to an unrelated process; "verify command line" reduces risk but does not cover PID reuse.
- No evidence that FFmpeg conversion was tested with varied input codecs/containers, or that the resulting file actually plays in the intended target clients.
