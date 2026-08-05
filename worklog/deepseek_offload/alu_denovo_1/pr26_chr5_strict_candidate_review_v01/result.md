**ALU-DeNovo-1 – Compact Review of PR26 chr5 Strict Survivor Candidate**  

**Report note:**  
- Candidate: chr5:51263989-51264294 (AluYa5 element, consensus pos 54). Child has a G→A variant (away from consensus) supported by 16/28 high-quality reads (8F/8R, mapQ 60, baseQ 30, median edge dist ~45, 8 read groups). Both parents show 0/28 (father) and 0/21 (mother) A reads – only G at high quality.  
- This is the first candidate surviving strict filters in the current expansion (previous candidates on PR26 chr14 and PK16 chr5 were primary-only and ruled out biologically).  
- The pattern is interesting: clean parent-child discordance, strand-balanced support, and no A in parents. However, it remains a **screen candidate only**. It has not passed source-locus, mapping ambiguity, copy number, local depth, read-pair, or independent validation checks.  

**Prioritized next-check list (best falsification attempts):**  
1. **Mapping ambiguity & source-locus check** – Verify that the child A reads do not map better to a paralogous or multi-copy Alu element elsewhere (e.g., a different AluYa5 copy in the genome or an AluY polymorphism). Realign candidate reads to all known AluYa5 consensus copies; check for split or secondary mappings that would indicate the variant is actually inherited from a more distant allele.  
2. **Local depth & copy number check** – Examine read depth at the candidate site in child vs. parents. A de novo event should have normal local depth in the child (no unusual gain/loss). An apparent A allele could also arise from a nearby structural variant (e.g., deletion or duplication) that misrepresents mapping or creates an apparent mismatch. Use read-pair discordance and depth ratios across the element and flanking regions.  
3. **Independent call / orthogonal validation** – If possible (given experimental resources), design a PCR or pull consensus from a separate sequencing run. The strongest falsification is failure to reproduce the A allele in a fresh library or in a different read set from the same child.  

*Status: Interesting candidate; not proven; these three checks will either confirm or refute biological de novo status.*
