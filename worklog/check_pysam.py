try:
 import pysam
 print('pysam_ok', pysam.__version__)
except Exception as e:
 print('pysam_fail', type(e).__name__, str(e))
