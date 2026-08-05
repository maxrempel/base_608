# Task: compact blood-group genetics audit

Return at most 700 words. List only the five highest-risk scientific errors or
overclaims in this deidentified consumer-array method. For each, state whether
it is definitely wrong, ancestry/platform dependent, or merely a limitation.
Do not spend reasoning on prose polish.

Method:

- ABO four-tag allele counts: rs507666 A=A1, rs8176704 A=A2,
  rs8176746 T=B, rs687289 G=O; rs505922 T only if rs687289 absent.
  Counts must all exist and sum to two. rs8176719 deletion D checks common O1;
  rs41302905 T can explain non-O1 O. Conflicts are retained as low confidence.
- RhD rs590787 after consumer-output normalization: plus-strand GG is treated
  as a negative proxy, AG/AA as positive proxy. It is explicitly nonclinical,
  ancestry dependent, and does not directly measure RHD deletion/copy number.
- Extended research predictions: rs8176058 plus A=K/G=k; rs8176059
  A=Kp(a)/G=Kp(b); rs1058396 G=Jk(a)/A=Jk(b); rs12075 G=Fy(a)/A=Fy(b),
  with rs2814778 C as Duffy erythroid-null promoter; rs7683365 genomic
  plus A=S/G=s (the gene coding alleles are complementary C/T);
  rs609320 genomic plus G=E/C=e; rs2285644 genomic plus A=Di(a)/G=Di(b);
  rs28399653 A=Lu(a)/G=Lu(b); FUT2 rs601338 AA predicted nonsecretor,
  AG/GG predicted secretor.
- Genotypes are complemented only when their observed alphabet cannot match the
  known genomic-plus alphabet for that marker.
- Parent-child ABO transmission and one duplicate-platform family are checked.
- Result: five designated participants; ABO resolves A=3/O=1 with one
  unresolved; RhD proxy resolves two, both positive. Conclusion is only that
  this small incomplete dataset does not support O-negative enrichment.

Important: Published genomic-plus sources explicitly list rs7683365 as A/G,
with A encoding S and G encoding s. Do not call that mapping wrong merely
because GYPB coding-strand notation is C/T.
