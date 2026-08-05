Write one compact Python 3 script, code only, under 180 lines. It must profile only a supplied TSV manifest of approved public controls, never participant inputs.

CLI: `script.py --manifest controls.tsv --reference REF.fa --samtools /usr/bin/samtools --output profile.tsv --region chr1:25230000-25460000`.

Manifest columns: sample_id, alignment_path, alignment_bytes, alignment_md5, index_path, index_sha256. Requirements:
- refuse duplicate IDs, non-GRCh38 region spelling, missing files, nonpositive bytes, invalid hashes, or more than 20 rows;
- for every row verify current alignment/index byte sizes where supplied and run only `samtools stats --reference REF ALIGNMENT REGION` sequentially;
- capture no reads, coordinates beyond the fixed region, or individual variants;
- parse SN raw total sequences, reads mapped, error rate, average length, insert size average, insert size standard deviation;
- parse IS histogram columns (insert size and pairs total) and calculate weighted median insert size;
- write an atomic TSV with exact denominators plus status, stderr-safe failure reason, elapsed seconds; fail entire publication if any row fails;
- use a private umask, no shell=True, deterministic ordering, temporary files beside output, and atomic os.replace;
- output a final coordinate-free aggregate row using medians across samples for error rate, insert mean, insert SD, and insert weighted median.

No simulation, no calling, no downloads, no scientific inference. Keep code plain and dependency-free.
