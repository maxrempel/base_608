## ALU-DeNovo-1 Production Inventory – Checklist

**1. Admission: PR04 as shortest safe next trio**
Yes. PR04 is the only approved manifest trio with a fully verified local child (HG00642). The ten completed trios are done; no other pending trio has a local child or provenanced data. Proceeding with PR04 minimizes new data transfer and risk.

**2. Fail-closed preflight checks for first small chromosome unit (e.g., chr1)**
- [ ] Confirm frozen manifest for PR04 is uncorrupted and contains authoritative public URLs + MD5 for mother (HG00641) and father (HG00640).
- [ ] Verify local child HG00642 CRAM size (15,237,550,938 B) and MD5 (3a8834d6876876e53d4d96cee63d539c) exactly match manifest.
- [ ] Confirm child’s CRAI (index) is present and valid.
- [ ] Assert no Alu scientific or transfer service is running (confirmed none active).
- [ ] Check Asto disk space: 431 GB free – sufficient for two parent CRAMs (~30 GB each) and temporary workspace.
- [ ] Ensure network access to remote parent URLs (test connectivity, no firewall blocks).
- [ ] Verify runner binary (two cores, remote indexed CRAM reader) passes a dry‑run on a small region of the local child.
- [ ] Confirm that the prohibited Taygeta HG02883 is not referenced anywhere in the manifest or workflow.
- [ ] Lock the working directory to prevent concurrent transfers.

**3. Acquisition plan for missing parents (HG00641, HG00640)**
- **Tool:** `aria2c` (preferred for resumability and parallel connections) or `curl -C -`; no duplicate transfer.
- **Step A (check duplicates):** For each parent, if CRAM already exists in source‑accepted tree and its MD5 matches manifest, skip download. Otherwise proceed.
- **Step B (download):** Use `aria2c --continue --max-connection-per-server=4 -x 4 -o <output.cram> <URL>`; redirect to a staging directory (e.g., `$STAGING/PR04/`).
- **Step C (checksum gate):** After download, compute MD5 of staged file. Abort if mismatch; else move into source‑accepted tree (e.g., `$SOURCE/PR04/`). Retain original URL and manifest MD5 in provenance log.
- **Step D (index):** Verify or download corresponding .crai from manifest (if provided) or generate with `samtools index`.
- **Resumption:** If interrupted, same command will resume partial download; checksum gate re‑validates only on complete file.

**4. Evidence retained after first chromosome (e.g., chr1)**
- Local child CRAM MD5 + provenance.
- Fetched parent CRAM MD5 records (with URLs and timestamps).
- Chromosome‑specific analysis output (exact copy counts, annotated loci).
- Per‑chromosome checksums of all three CRAMs (from `samtools md5` or equivalent).
- Logs of preflight checks, download steps, and any abort conditions.
- Runner session logs (two‑core configuration).

**5. Scientific/operational hazards flagged**
- **Prohibited sample:** Taygeta HG02883 must never be included – verify manifest does not contain it.
- **Disk space:** Only 431 GB free; monitor during two simultaneous downloads (peak may exceed free space if temp files large). Consider sequential download or reduce connection count.
- **No active network transfer tools:** Before starting, confirm aria2/curl are installed and permitted.
- **Runner limitations:** Two cores may bottleneck small‑chromosome processing; ensure analysis is incremental and checkpointed per chromosome.
- **Manifest integrity:** Must be frozen and backed up – any corruption during acquisition invalidates gates.
