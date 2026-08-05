
## [2026-07-03 15:34] ? 2b941dd4
- DID: Found Max's existing interview inventory: Notion '2026-03-10 YouTube Talks Inventory' (48 entries, id 3200316f55608112bd20dfc784abc86d) + ~60 local transcripts in Nextcloud/zSyncMain/youtube_transcripts/txt/. Also 'Interview Linkset' Notion page.
- STATE: Task = collect Max's English alien/hybridization interview links, start from Memex transcripts, then thorough online search. No English alien-interviews playlist/page exists yet.
- NEXT: Build consolidated alien-interview list from inventory + online sweep

## [2026-07-03 16:07] ? 2b941dd4
- DID: Built maxrempel.com/interviews page (D1 pages+nav, no redeploy): 8 external interviews + 2 Hucolo ancient-aliens/artifacts talks + 'In the media' section (2 Daily Mail incl June 2026 CIA/hybrids feature, NY Post, VICE). All links target=_blank. Added Whitley Strieber Dreamland, swapped Camelot->Kerry Cassidy Rumble.
- STATE: Interviews page live. Press section = 4 top articles.
- NEXT: Await Max: confirm Hucolo pair, any additions

## [2026-07-10 14:35] ? 6bb8eae1
- DID: GENTLE re-run per Max: filter too aggressive (threw out 93%). Max's rule: child alt-read support >=6 = clean if parents clean (no objection). Modified denovo_caller to emit EVERY clean-parent carrier (parents strict GQ20/DP10/0-alt; child wide open) with cALT read count, so future threshold changes need no re-stream. Re-streaming chr22 on box 98.80.196.208, output denovo_chr22_gentle.tsv (~144k expected).
- STATE: gentle caller running detached pid 4881 on box; box RUNNING (stop when done). Downstream: filter cALT>=6 locally + tag tiers, re-run beautification.
- NEXT: Wait for gentle caller, pull table, apply Max's >=6-read clean filter + quality-tier tagging, re-run orderliness analysis across tiers, STOP box.

## [2026-07-10 15:19] ? 6bb8eae1
- DID: BEAUTIFICATION v2 design memo written (per Max: report before coding, separate subfolder). Metric=general compressibility (LZ), separate simple-repeats, focus non-repeats. Normalization=per-site internal control (each spot vs its own alternative bases), frequency never the yardstick. Memo: beautification_compress/BEAUTIFICATION_compress_DESIGN_v01_tomemex.md. Committed+pushed. NO code yet.
- STATE: Awaiting Max's answers on 5 open decisions before coding v2. All v2 work is local (gentle chr22 table, 144k rows), no box.
- NEXT: On greenlight: build LZ compressibility + per-site internal control, positive-control (3 cases), run stratified grid (repeat/non-repeat x rare/frequent x window), LOOK, report distributions.

## [2026-07-10 22:56] ? 6bb8eae1
- DID: Autonomous A,B,C per Max (he's asleep). A: genome-wide gentle de-novo caller streaming all 23 chr in parallel on box 35.175.111.41 (pid driver 4878, resumable per-chrom .done, output ~/beaut/gw/, merge->denovo_gw.tsv). B built+chr22-piloted: repeat-structure restoration real t=6 but common-tilted (fresh t=1.9). C built+chr22-piloted: palindrome/hairpin = null everywhere. All committed+pushed. Scripts in beautification_compress/scripts/ (repstruct_v01, palindrome_v01, + runners; all accept a table path arg).
- STATE: A running (~60-90min, 195k rows so far, 0 chr done). B,C metrics done+piloted. Box RUNNING - must stop when A done + analyses run.
- NEXT: When denovo_gw.tsv ready: run beaut_compress_run, beaut_repstruct_run, beaut_palindrome_run on it (genome-wide, ~30x power for fresh signals); write combined final report; STOP box. Then report to Max.

## [2026-07-11 01:53] ? 6bb8eae1
- DID: A genome-wide de-novo COMPLETE: 3.06M clean-parent carriers all 23 chr, pulled to outputs/real/beaut_gw/denovo_gw.tsv, box STOPPED. Running all 3 metrics genome-wide (compress/repstruct/palindrome) in background -> outputs/GW_RESULTS_v01.txt.
- STATE: 3 analyses running background (bxua691um). Box stopped+confirmed pending.
- NEXT: Read GW_RESULTS when done; write combined final report A+B+C; commit+push; report to Max (genome-wide verdict on beautification).

## [2026-07-12 21:18] ? 6bb8eae1
- DID: Read-level check (Max's method) at 2 restoration sites via samtools on CRAMs. Site1 NA19677 chr1:1716427 = pristine (37 reads all MAPQ60 150M) = real. Site2 HG01514 chr1:2443684 (GC-rich) = messy (12bp insertions + soft-clips) = likely alignment artifact. Repeat-restoration signal is a MIXTURE: clean sites real, GC-rich/low-complexity sites artifact. Box stopped.
- STATE: Signal partly artifact (GC-rich misalignment). Need mappability/clean-alignment filter to isolate real fraction.
- NEXT: Propose: filter restoration sites to high-mappability/clean-alignment (exclude GC-rich low-complexity + near-indel), re-measure the fresh restoration signal on trustworthy sites only.

## [2026-07-14 09:36] ? 6bb8eae1
- DID: CONTEXT-MATCHED NULL PASSED: fresh repeat-restoration observed 0.365 vs trinucleotide-chemistry-expected 0.332, SIGNAL +0.033 z=+8.9 -> exceeds mutation chemistry. Effect survived: genotype QC (z8.1), mappability Umap-k36+ENCODE (z8.0), trinuc chemistry (z8.9). Caveat: slippage longer-range than trinuc; full repeat-context null = final rigor. Regenerated denovo_gw_clean.tsv from box EBS (worktree copy deleted by shared blob-strip), box stopped. Committed+pushed.
- STATE: Signal now real+not-artifact+not-chemistry(standard test). Strongest it has looked. Box stopped.
- NEXT: Optional final rigor: full repeat-context (period-aware) mutation null, esp period>=2 repeats. Also per-person beautifier/degrader split on this confirmed signal; which repeat families/periods drive it.

## [2026-07-15 18:22] ? 6bb8eae1
- DID: REDO done: built read-level clean-alignment filter (beaut_readclean_v01.py), classified all 2340 degraded-repeat de-novo sites via child CRAM pileups on AWS box.
- STATE: P2 beautification z=6.7 restoration finding RETRACTED as an alignment artifact: null on 586 clean sites (z=0.7), all signal in 1754 dirty sites, dose-response with alignment dirtiness. v04 report written, committed+pushed to master, box stopped.
- NEXT: Await Max direction. If pursuing hypothesis further, needs indel-aware method (local reassembly/graph/long reads), not short-read SNV counting.
- LESSON: One read-level look overturned a 6-control robust result; k-mer mappability cannot see intra-repeat indel-placement ambiguity.
