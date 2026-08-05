# Scribe handover - milestone 5 (~382K tokens)
# session: 20260704_relaxed_dijkstra_f7ccbd_1d3440d2
# cwd: C:\claude_base\.claude\worktrees\relaxed-dijkstra-f7ccbd
# written: 2026-07-04 12:15:04 by deepseek-v4-pro

## HANDOVER - Omega Contig Foreign-Insertion Detector

### GOAL (in Max's words)

"We need to look at all insertions, catalogue them, see what organisms they are. Human insertions out of place, animal, bacterial, viral, even transposons if they look artificial - not natural transposition scars. And especially 'nearly human but not human' - that's the distant-relative signal. Then compare across multiple self-reported abductees. It's a long-term project. Right now document everything we find on Kristen first."

More concretely: "I predict tons of insertions, uniform, transposon?like but **not** known transposons - a big family of near?identical payloads scattered across the genome. That's the signature we hunt. Also, nothing blind?excluded - inventory first, calibrate second. And we expect the real insertions to be **rare** (a small percent of the population, not the consensus genome) - hunt the rare tail."

### DECISIONS MADE AND WHY

**Target shape - the "omega contig"**
We defined an **omega (?) contig** = a single assembled piece where the **first ?100?bp** and the **last ?100?bp** both align perfectly to human, same chromosome, same strand, and land **adjacent** (head?to?tail) - the genome was cut at one spot. The middle matches nothing human. This forces a single clean breakpoint, avoids aligner black?hole regions, and directly shows the payload.

- **Adjacency tolerance:** ?20?bp, exact gap recorded per hit. True zero?gap splices stand out.
- **Germline only** (~99% of cells) - so at 30? coverage an insertion has full support; VAF is not a limit. AWS is only for horsepower, not sensitivity.
- **No blind exclusion.** All five "gates" (MEI, organism?ID, ref?gap, junction proof, population recurrence) are now **label?and?count**, not filters. Every candidate stays in the census with per?gate annotation. The first deliverable is a full inventory; thresholds come *after* we see the real numbers.

**Payload classification taxonomy** (added from Max's feedback)
- Origin: human?out?of?place, animal, bacterial, viral, near?human?diverged (percent?identity recorded), true unknown.
- Insertion signature: natural transposon scar (TSD, poly?A tail) vs **artificial** (blunt ends, no TSD, CRISPR?style). A transposon sitting there *without* its natural scar is a candidate engineered insertion.
- Population frequency: hunt the **rare tail** - present in a few % of people, absent from the consensus genome. "Found in a database" does not disqualify if it's rare there. This also naturally kills segdup/mismap artifacts (they recur in everyone).

**Cross?locus payload clustering (future)**
Max predicts that a foreign, transposon?like element would appear as many near?identical copies at scattered loci. So after initial detection we will cluster the payloads *against each other* - a large family that matches **no** known transposon (not in Dfam/RepeatMasker) is the prediction. That step is **not yet built** - it's the next layer after the baseline inventory.

**Compute decisions**
- Data lives on **asto** (Liz's borrowed Debian box), but Omega was 4th in the queue there. Max directed us to move to **Sol** (192.168.1.113) across the same 1 Gb LAN. Copy of the 35?GB BAM was throttled (<50% link, I/O?niced) and is byte?exact verified.
- **No internet downloads** - the house connection is nearly dead. All tools (samtools, minimap2, megahit, kraken2) were copied as binaries from asto over the LAN and verified running with local libs.
- Resource cap on all boxes: CPU/RAM/disk/network each ?50% ideal, ?70% hard. Sol has 826?GB free, 8 cores, 28?GB usable RAM - room to spare.
- Pipeline launched with **graduated piloting**: 5?Mb slice ? chr22 (autosomal) ? chr21 (acrocentric stress?test) ? genome?wide. Each stage timed and extrapolated before scaling, per Max's "scale up a little bit, don't do everything at once."

### CURRENT STATE

The genome?wide run is **live on Sol** as of ~11:47?PT (2026?07?04).  
It is processing chromosomes one at a time via `omega_genome.sh`, using the resumable per?region wrapper and the per?cluster assembler. Configuration:
- `NPROC=6` (out of 8 cores)
- Each chromosome produces `.done` markers; if stopped, restart skips finished chromosomes.
- Every candidate cluster assembled individually (resumable per cluster with its own `.done`).
- Final step after assembly: `omega_census.py` will produce the full inventory.

**Pilot results that validate the pipeline**
- 5?Mb slice: 21 candidates, 0 hits (correct).
- chr22 (50?Mb): 202 candidates, all assembled, 0 hits (correct).
- chr21 (acrocentric, heavy repeats): 3451 raw clusters ? segdup mask ? 332 candidates, all assembled, **0 hits** (the omega adjacency filter correctly rejects the repeat pile?ups).
- Measured rate: ~1.5?sec per cluster at NPROC=6 ? genome?wide ~12-15?k candidates ? **total run ??2?hours** (extraction ~40?min, assembly ~40-55?min), comfortably under the 5?h ideal.

All scripts, environment, tools, and masks are committed and on Sol.

**Key files / paths**
- Project root: `C:\claude_base\projects\XG1\kenefick\omega_detector\`
- Design doc: `OMEGA_PIPELINE_DESIGN_v01_tomemex.md`
- Sol working dir: `~/omega_run/`
- Scripts on Sol: `~/omega_run/scripts/` - `omega_genome.sh`, `omega_run_region.sh`, `omega_extract.py`, `omega_mask.py`, `omega_percluster.sh` (v03, resumable+parallel), `omega_census.py`, `omega_gates.sh` (partial)
- Data: `kristen.mq.bam` + `.bai`, ref `GRCh38.fa` (numeric contig names), `segdups_nochr.bed` (X9A's mask)
- Board/coord: the `omega_contig` room in `bcast`; x1 is building the T2T/pangenome gate on Sol/Lak.

### EXACT NEXT STEP

**When the genome?wide run finishes** (expected ~1:45?PT, i.e., soon):
1. Verify `RUN_COMPLETE` marker, check for any failed chromosomes.
2. Run the census (`omega_census.py`) to produce the full inventory table (per?candidate annotations by gate) and the summary distribution.
3. Post a summary and the inventory path to the board.
4. If any candidate passes the omega shape + minimal adjacency filter, flag it immediately (that would be the first actual hit). Then proceed to gate?labeling (kraken2/UniVec organism ID, mobile element check) - but the gates are for annotation, not exclusion.
5. After Max reviews the census, we calibrate which bins to set aside and build the cross?locus payload clustering.

If the run is still grinding when you take over, the next autonomous tick will check progress, log it, and re?arm the timer.

### OPEN QUESTIONS (awaiting Max)

- **Adjacency tolerance:** He agreed to ?20?bp with gap recorded - no further objection raised.
- **Minimum reads per anchor:** He didn't finalize a hard threshold; the current `MINSIDE=8` (?8 soft?clipped reads on **both** borders, balanced) is a working assumption that gave clean pilots.
- **Cross?locus clustering:** He endorsed it but hasn't given a concrete threshold for "family size" or identity. That's a future design, not yet needed for the inventory.
- **Full census review:** The inventory is the point where he'll decide what's "interesting" vs. background, so that's the next human?required checkpoint.

### GOTCHAS AND DEAD ENDS

- **PowerShell's `tr "\\\\r"` bug:** A CR?stripping command escaped through PowerShell and became `tr -d "r"` - deleting every letter 'r' from a script. Always strip line?endings **in bash**, never via PowerShell.
- **Environment `set -u` crash:** `env.sh` referenced `$LD_LIBRARY_PATH` when unset, killing the strict?mode script. All env files now use `${LD_LIBRARY_PATH:-}` defaults.
- **SAMtools libs on Sol:** The binary from asto needed `libhtscodecs.so.2`; had to copy the whole library set and run with `LD_LIBRARY_PATH` pointing to local. Works now.
- **Contig names are numeric** (e.g., `20`, not `chr20`). All scripts use that convention.
- **Big repeat pile?ups:** Segdup mask only removes ~16% of candidates; the real discriminator is requiring both borders present and balanced (support <~30 each side). The centromere/heterochromatin mask is still not applied - the artificial regions produce artifacts that fail the omega adjacency filter, but they eat assembly time. A more complete mask would speed things up further.
- **House internet near?dead:** Any tool/DB fetch (MEI library, T2T reference for x1's gate) must wait or be copied over LAN from a machine that already has them.
- **No?silent?exclusion principle:** The gates are label?and?count, never delete?filters. If anything gets dropped later, its counts and reasons must remain visible in the census. This is embedded in all design docs.
