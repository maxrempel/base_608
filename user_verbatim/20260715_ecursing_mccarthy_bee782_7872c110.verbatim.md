# VERBATIM user (Max) log - session 7872c110-bb3f-48c8-ad4b-6c0df0807d04
# cwd: C:\claude_base\.claude\worktrees\recursing-mccarthy-bee782
# Every line Max typed, saved verbatim, so it survives compaction.
# Recover specs / investigate trouble by reading this file.


## [2026-07-15 11:17:26] turn 1
Rename yourself to x7c and read the instructions how to write emails to Kristen and let's work on the report number 2 for Kristen. Let's explain it to her and use the version where you do email message plus technical report attached with all the methods and results.

## [2026-07-15 11:28:34] turn 2
Oh, yeah, yeah, yeah, sorry, wait a second, yes, scale it up if it is good, yes, scale it up. Do like, do maybe half an hour worth of work, summarize the results and keep digging further until you finish everything.

## [2026-07-15 11:58:00] turn 3
Genome-wide maternal-SNV scan check (Kristen report-2 scale-up, session x7c). Do: (1) SSH asto and aggregate partial: /home/rempel/miniconda3/envs/xtea/bin/python3 /home/rempel/genomics/omega_run/scripts/run_gw_maternal_snv_v01.py agg (shows windows done / total + summed buckets + MATERNAL_DENOVO candidate rows). Also check the scan is alive: ls gw_maternal_snv/*.done | wc -l is increasing, and tail driver.log. (2) If windows-done is NOT increasing since last check, diagnose (don't just re-sleep) - check driver.log for errors, confirm PID 2938007 or restart with `run` (resumable). (3) If not all 300 done: summarize the partial to Max briefly, re-arm a ~1500s ScheduleWakeup with this same prompt. (4) If all 300 done: QC every MATERNAL_DENOVO candidate at read level (samtools mpileup Oliver+Kristen at the site + anchor; a genome-wide 0 must be explained per the too-clean rule, not celebrated), then run the chrX bonus case (Oliver X variants Kristen lacks = maternal by inheritance, no phasing), then write Kristen's report-2 letter (email + technical report attachment, Anna voice from anna@maxrempel.com, investigation-not-declaration, defined terms, no reassurance, non-medical disclaimer, no work-promise). NOTHING sends without Max's explicit approval. asto BAMs (kristen.bwa.mq.bam/oliver.mq.bam) are the last copies - never delete.
