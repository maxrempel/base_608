Task: Draft a concise preliminary scientific report from deidentified aggregate Omun data.

Privacy: Use only the aggregate data below. Do not invent coordinates, read IDs, alignments, sequences, names, or private participant traits. Labels S1, S2, and S3 are deidentified self-reported Starseed participants.

Style required:
- Plain English.
- Define terms beside the first table or graph.
- State the scientific question first.
- Put the main conclusion near the top.
- Mark the report PRELIMINARY and dated 2026-07-25.
- Do not use unexplained abbreviations.
- Do not claim biological enrichment, depletion, biological absence, or non-human origin.
- Make culture/platform confounding prominent.

Definitions:
- Omun means the project uncommon OMEGA insertion endpoint: clean, deduplicated, two-sided autosomal OMEGA loci that are database-novel or known-rare below 0.001.
- Callable D10 bases are the denominator: autosomal bases passing the locked D10 callable rule.
- Rate means Omun loci per billion callable D10 bases.
- Technical read-support attrition is a stricter read-level diagnostic. It is not truth validation and must not revise the Omun burden.
- The controls are 20 cultured 1000 Genomes controls, balanced four each from AFR, AMR, EAS, EUR, SAS.
- S2 and S3 are not culture-matched to the controls. This is a primary confounder.

Focal endpoint data:
sample_label	culture_status	omun	novel	rare	callable_bases	rate_per_gb	starts2_passes
S1	unknown	155	140	15	2663784865	58.1879	64
S2	uncultured_or_not_culture_matched	3	3	0	2664221029	1.12603	1
S3	uncultured_or_not_culture_matched	1	1	0	2664016901	0.3754	1

Control endpoint data:
label	superpopulation	omun	novel	rare	callable_bases	rate_per_gb	starts2_passes
control_primary_sas_01	SAS	176	156	20	2667498511	65.9794	NA
control_primary_amr_01	AMR	183	168	15	2667164935	68.6122	75
control_primary_eas_01	EAS	185	173	12	2665936573	69.3940	74
control_primary_eas_02	EAS	169	154	15	2666798700	63.3719	54
control_primary_eas_03	EAS	208	193	15	2666528426	78.0040	80
control_primary_eas_04	EAS	220	199	21	2666032645	82.5196	85
control_primary_sas_02	SAS	202	189	13	2669582302	75.6673	92
control_primary_sas_03	SAS	174	157	17	2668285751	65.2104	62
control_primary_sas_04	SAS	175	159	16	2668099760	65.5898	69
control_primary_afr_01	AFR	199	191	8	2666876392	74.6191	84
control_primary_afr_02	AFR	207	193	14	2668072395	77.5841	78
control_primary_afr_03	AFR	224	207	17	2666260814	84.0128	88
control_primary_afr_04	AFR	185	171	14	2665715875	69.3997	71
control_primary_eur_01	EUR	209	197	12	2668226712	78.3292	83
control_primary_eur_02	EUR	143	136	7	2662998220	53.6989	53
control_primary_eur_03	EUR	177	168	9	2669635882	66.3012	70
control_primary_amr_02	AMR	176	162	14	2664854623	66.0449	66
control_primary_amr_03	AMR	173	162	11	2664150718	64.9363	74
control_primary_amr_04	AMR	199	180	19	2668164952	74.5831	76
control_primary_eur_04	EUR	167	153	14	2668505346	62.5818	52

Verified summary statistics:
- Controls n=20.
- Control Omun counts: mean 187.55, standard deviation 20.29, range 143 to 224.
- Control rates: mean 70.322/Gb, standard deviation 7.600/Gb, range 53.699 to 84.013/Gb.
- Approximate 95 percent confidence interval for the cultured-control mean rate: 66.765 to 73.879/Gb.
- Approximate 95 percent prediction interval for one cultured-control-like genome: 54.023 to 86.621/Gb.
- Controls with rates at or below S1: 1 of 20.
- Controls with rates at or below S2: 0 of 20.
- Controls with rates at or below S3: 0 of 20.
- Control starts2 read-support total excluding one unavailable audit: 1386/3575 = 38.77 percent.

Topology boundary:
- S2 has 3 Omun loci and S3 has 1 Omun locus. These Omun endpoints cannot establish scattered topology.
- Any topology section must say it requires a larger named preserved category. For S3 the larger currently supplied category is 7 deduplicated autosomal loci and 6 clean loci. For S2, larger deduplicated/clean categories are not supplied in this packet.

Need report sections:
1. Scientific question.
2. One-paragraph main conclusion.
3. Table-ready explanation of all individuals.
4. Control spread and focal comparison.
5. Technical-audit attrition and what it means.
6. Topology boundary and how to test scattered/dispersed topology without mixing it into Omun burden.
7. Smallest practical uncultured matched-control acquisition/analysis plan.
8. Claims not supported yet.

Return a draft in plain Markdown, not too long.
