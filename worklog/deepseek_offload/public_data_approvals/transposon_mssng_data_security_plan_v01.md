# TRANSPOSON MSSNG data security plan v01

Last edited: 2026-08-01 by Codex (GPT-5.6 SOL)

Status: Project-specific control plan prepared for institutional approval. It applies only to the proposed cloud-only MSSNG project. No MSSNG data have been accessed or downloaded.

## Scope and responsible person

- Institution: TRANSPOSON
- Researcher and initial sole data user: Max Myakishev-Rempel, Ph.D., Chief Executive Officer
- Institutional IT reviewer: Charles Crawford, IT Director
- Data location: the MSSNG-approved cloud environment only
- Local download: prohibited during the initial phase
- Removable-media storage: prohibited
- External linkage, re-identification, credential sharing, and redistribution: prohibited

## Access controls

1. Only a person listed on the approved application may access MSSNG data.
2. Every approved user must use an individual account. Accounts and authentication factors may not be shared.
3. The workstation must use a password-protected, non-shared user account, automatic screen locking, active firewall, current antimalware protection, and current operating-system security updates.
4. Any later addition of a user requires MSSNG approval and this plan must be revised before access begins.
5. Any later local download requires prior written MSSNG approval, verified full-disk encryption, a locked room or office, auditable access controls, and a revised data-location inventory.

## Logging and audit

1. MSSNG and cloud-provider access logs are the authoritative audit record for database and genomic-data access.
2. The researcher may not disable, alter, or delete provider audit logs.
3. Project scripts will create timestamped, append-only analysis logs inside the approved cloud project. Logs will record the software version, input dataset release, operation, and output location without copying participant identifiers into external logs.
4. Aggregate exported results and destruction actions will be recorded in a retained institutional project register.

## Network and endpoint protection

- Windows Firewall is enabled for Domain, Private, and Public profiles.
- Microsoft Defender antivirus, antispyware, real-time protection, behavior monitoring, and downloaded-file scanning are enabled.
- No inbound service is required for MSSNG work.
- Raw or participant-level MSSNG data will not be synchronized to personal cloud drives, local backup systems, external drives, or removable media.
- Full-disk encryption status must be verified with administrator privileges before any local download is proposed. Until then, local download remains prohibited.

## Analysis and disclosure controls

1. Participant and family identifiers remain inside the approved environment.
2. Only aggregate results needed for the approved research question may be exported.
3. Small cells and outputs that could enable singling out a participant or family will not be exported.
4. Candidate sequences will be screened and summarized inside the approved environment. Read-level evidence and reconstructed participant-level sequences remain there.
5. MSSNG approval will be obtained before any collaboration, new use, or external transfer that is not already covered by the agreement.

## Incident response

Any suspected credential compromise, unauthorized access, unintended disclosure, malware event, or loss of control over MSSNG data will trigger immediate suspension of access. TRANSPOSON will preserve relevant logs, contain the event, and notify the MSSNG Coordinating Center immediately as required by the agreement.

## Retention and destruction

At project completion or earlier expiration or termination of the agreement, access will cease and all MSSNG data or copies under TRANSPOSON's control will be deleted. Destruction will be checked against the data-location inventory and certified to MSSNG when required. Aggregate non-identifying research outputs may be retained only to the extent permitted by the agreement.

## Verification record

On 2026-08-01, Codex verified on the intended Windows 11 Pro workstation that all Windows Firewall profiles and Microsoft Defender real-time protections were active. The non-administrative check could not read BitLocker status. This does not affect the initial cloud-only phase because local download is prohibited, but it must be resolved before any local data storage.

## Approval

Technical confirmation: pending Charles Crawford's review as TRANSPOSON IT Director.

Institutional approval: pending Oksana Polesskaya's review as TRANSPOSON Signing Official. The plan must not be represented as institutionally approved until those confirmations are received.
