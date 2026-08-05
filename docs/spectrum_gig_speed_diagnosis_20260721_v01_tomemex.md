# Spectrum Gig speed diagnosis and recovery report

**PRELIMINARY - July 21, 2026 - version 01**

## Main conclusion

The home is paying about $120 per month for Spectrum Internet Gig, but recent measured download speeds are far below the service tier. The clearest laptop test was about **55 Mbps download and 31 Mbps upload**. This is not a small difference caused by normal "up to" wording.

The investigation found two credible bottlenecks that must be separated with one controlled wired test:

1. **The customer-owned OpenWrt router may be limiting routed throughput.** It is a TP-Link Archer A7 v5 running old OpenWrt 22.03.2 firmware, and software flow offloading is disabled. OpenWrt says software flow offloading can commonly improve routed throughput by two to three times.
2. **Spectrum, the cable modem, or the coax line may be delivering the wrong service.** Plausible causes include incorrect Gig provisioning, the wrong modem registered to the account, degraded cable signal, errors following the June outage, or neighborhood congestion.

The Ethernet connection between the OpenWrt router and cable modem is healthy: it negotiates at **1,000 Mbps full duplex with zero recorded Ethernet errors**. Therefore, a bad 100 Mbps Ethernet negotiation is not the explanation.

No modem or router was restarted, bypassed, or reconfigured during this investigation. Taygeta and Asto are being used by other troubleshooting sessions, so disruptive testing should wait for a coordinated maintenance window.

## What equipment is actually in use

### Confirmed router

- TP-Link Archer A7 hardware version 5
- Hostname: RempelOpenWrt
- OpenWrt 22.03.2, released in 2022
- Gigabit Ethernet wide-area-network port and four Gigabit local-area-network ports
- Wi-Fi 5, also called 802.11ac

The Archer A7 is a **router**, not a cable modem. It has no coax connector and cannot itself connect to Spectrum's cable network. "Open modem software" appears to refer to OpenWrt, the open-source software running on this router.

### Probable cable modem

Spectrum's March 20, 2026 shipment email lists a **DOCSIS 3.1 cable modem with a 2.5 Gigabit Ethernet port** and a Spectrum Wi-Fi 6E router. The current topology and earlier handover notes indicate that the Spectrum cable modem probably remains upstream in bridge mode, while the Spectrum Wi-Fi router was replaced by the Archer A7 so existing port forwarding would work.

The exact cable modem model and ownership cannot yet be confirmed remotely. Its usual management address, 192.168.100.1, did not respond from either the laptop or the OpenWrt router. Spectrum should verify the modem serial and media-access-control address registered to the account without exposing those identifiers in a public report.

## Evidence collected

| Check | Result | Meaning |
|---|---:|---|
| Current plan | Spectrum Internet Gig, upgraded March 18, 2026 | The paid tier should provide roughly Gig-class wired download service |
| Spectrum's earlier typical wired target | About 1,045 Mbps down and 40 Mbps up | The recent 55 Mbps result is far outside the expected range |
| Laptop internet test | About 55 Mbps down, 31 Mbps up | Severe real-world degradation is present |
| Laptop loaded latency | About 84 milliseconds | The connection also slows noticeably under load |
| Laptop Wi-Fi link | 351 Mbps receive, 702 Mbps transmit, 89 percent signal | Wi-Fi prevents a clean 1,000 Mbps proof, but it does not reasonably explain only 55 Mbps |
| Router-to-modem Ethernet | 1,000 Mbps, full duplex | The physical Ethernet link is not stuck at 100 Mbps |
| Router WAN errors | Zero receive errors, transmit errors, and recorded drops | No evidence of a failing WAN cable or Ethernet port |
| Router processor at rest | Light load | No sign of constant background processor overload |
| OpenWrt flow offloading | Disabled | A credible router throughput limitation under heavy routed traffic |
| Smart Queue Management | Not installed or active | No known configured bandwidth shaper is imposing a low ceiling |
| June 16 Spectrum event | Area outage; intermittent problems were expected afterward | A Spectrum-side or coax issue remains credible |

Two single-stream wired downloads from Lakarian measured about **8.9 Mbps and 4.8 Mbps**. These support the degradation finding but are not decisive because the remote download servers may have limited each stream. The 55 Mbps browser test is the better current internet measurement.

## What online user reports add

Independent reports do not prove the cause at this house, but they reveal recurring failure patterns worth testing:

- Spectrum customers report Gig upgrades that remained slow until the modem was correctly provisioned. One customer later said the service had been only partially provisioned.
- Other users report that customer-owned modems may not be accepted for some newer symmetrical tiers, even when the modem hardware is technically fast enough. Spectrum's current compatibility rules therefore matter more than the modem's advertised maximum speed.
- Spectrum community responses repeatedly ask for a speed test directly connected to the modem to distinguish a provider or line problem from a router problem.
- Users also report speeds that drift down again after reprovisioning. That is anecdotal, but it supports asking Spectrum to inspect the modem profile, signal history, and neighborhood node instead of relying only on a reboot.

These reports are consistent with the local evidence, but they do not establish that Spectrum is deliberately throttling the connection.

## Most likely explanations, in order

### 1. Router forwarding limit

The Archer A7 has Gigabit ports, but its processor must still translate and firewall every routed connection. The old OpenWrt release has software flow offloading disabled. Under a fast internet test, processor saturation could sharply cap throughput even though the Ethernet link itself remains at 1,000 Mbps.

### 2. Incorrect modem provisioning or account-to-modem mismatch

The plan was upgraded and equipment was shipped, but no activation-complete email was found. Spectrum may have the wrong modem registered, an old speed profile, or an incomplete Gig provisioning file.

### 3. Cable signal or neighborhood problem

Downstream power, upstream power, signal-to-noise ratio, corrected errors, uncorrectable errors, and neighborhood node utilization are visible to Spectrum even though the modem page is not locally accessible. The June outage makes this branch especially important.

### 4. Wi-Fi limitation

The laptop's current 351 Mbps receive link cannot demonstrate a full Gig service. It may reduce measured speed, but the strong signal and much higher link rate make Wi-Fi alone an incomplete explanation for 55 Mbps.

## Safe recovery plan

### Phase 1: controlled wired test behind OpenWrt

Wait until Taygeta and Asto work can tolerate a short test. Connect a Gigabit-capable computer by Ethernet to the Archer A7. Pause large transfers, then run two or three reputable multi-connection tests while recording:

- download and upload speed in Mbps;
- latency at rest and under load;
- router processor use during the test;
- WAN error counters before and after.

This is the most important missing measurement. It is non-destructive and should not require a restart.

### Phase 2: test OpenWrt software flow offloading

If the wired test is slow and the router processor becomes saturated, enable **software flow offloading only**, restart the firewall, and repeat the same test. Do not enable hardware flow offloading initially. The firewall restart can briefly interrupt connections, so this requires coordination with the other sessions.

OpenWrt warns that flow offloading can conflict with some traffic-control features. No Smart Queue Management configuration is currently active, which lowers that risk.

### Phase 3: isolate Spectrum from the router

If the wired result remains poor, connect one capable wired computer directly to the cable modem and repeat the test. This is disruptive: changing the device connected to a bridged cable modem often requires a modem reboot or lease reset, temporarily removes the home router, and can interrupt Lakarian services. Do it only in an agreed maintenance window.

The result gives a clean decision:

| Result | Conclusion |
|---|---|
| Direct-modem speed is fast, but speed behind Archer is slow | Archer A7 or its OpenWrt configuration is the bottleneck |
| Direct-modem speed is also slow | Spectrum provisioning, modem, coax line, or neighborhood node is the bottleneck |
| Software flow offloading restores high wired speed | Keep it after compatibility checks; router replacement is optional |
| Router processor stays low while wired speed is slow | Escalate Spectrum before buying a router |

### Phase 4: Spectrum escalation

Use this exact support request:

> I pay for Spectrum Internet Gig, but wired speeds are far below the plan. My router's WAN link negotiates at 1,000 Mbps full duplex with zero Ethernet errors. Please verify that the modem currently connected is the modem registered on my account, confirm the Gig provisioning file, and reprovision it. Please also read the downstream and upstream power, signal-to-noise ratio, corrected and uncorrectable errors, and neighborhood node congestion history. Please do not close the case based only on a remote reboot.

Ask for a technician visit if Spectrum cannot verify healthy signal levels and correct provisioning, or if a direct-modem wired test is still slow. Record the case number and every before-and-after speed result.

## Upgrade decision

Do not buy equipment yet. First complete the wired-behind-router and direct-modem comparison.

If the Archer A7 is proven to be the bottleneck, replace it with a modern OpenWrt-capable router that has:

- a substantially faster processor;
- Wi-Fi 6E or Wi-Fi 7;
- at least one 2.5 Gigabit WAN port;
- enough Gigabit or 2.5 Gigabit LAN ports;
- a tested method to preserve the existing port forwards and services.

If the direct-modem test is also slow, a router purchase will not fix the root cause. Spectrum must correct provisioning, modem compatibility, cable signal, or node capacity first.

## Sources

- [OpenWrt flow offloading documentation](https://openwrt.org/docs/guide-user/perf_and_log/flow_offloading)
- [OpenWrt TP-Link Archer A7 v5 hardware page](https://openwrt.org/toh/tp-link/archer_a7_v5)
- [TP-Link Archer A7 product specifications](https://www.tp-link.com/us/home-networking/wifi-router/archer-a7/)
- [OpenWrt firewall configuration](https://openwrt.org/docs/guide-user/firewall/firewall_configuration)
- [OpenWrt Smart Queue Management documentation](https://openwrt.org/docs/guide-user/network/traffic-shaping/sqm)
- [Spectrum community: slow Internet Gig discussion](https://community.spectrum.net/discussion/177359/slow-internet)
- [User report: incomplete modem provisioning after a Gig upgrade](https://www.reddit.com/r/Spectrum/comments/qcgb5w/question_about_modem_provisioning/)
- [Recent user discussion of Spectrum modem compatibility for Gig service](https://www.reddit.com/r/Spectrum/comments/1r36ptk/spectrum_gig_package_and_approved_modems/)
- [Recent user report of speed drifting after modem reprovisioning](https://www.reddit.com/r/Spectrum_Official/comments/1t7kxtd/modem_speed_drifting_lower_over_time/)
- Private evidence: March 2026 Spectrum plan and shipment emails, current billing records, OpenWrt status, local speed tests, and infrastructure notes. Account identifiers, equipment serial numbers, and the service address are intentionally omitted.

## Bottom line

The paid service is not currently delivering an acceptable result. The network's 1,000 Mbps router-to-modem Ethernet link is healthy. The next useful step is not a blind reboot or purchase: it is a controlled wired test behind the Archer A7, followed by a direct-modem test if needed. Those two measurements will assign responsibility to either the router path or Spectrum with far more confidence.
