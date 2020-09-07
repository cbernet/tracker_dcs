import logging
import sys

level = logging.INFO
log = logging.getLogger(__name__)
log.setLevel(level)

# stream handler
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s | %(message)s')
sh.setFormatter(formatter)
sh.setLevel(level)
log.addHandler(sh)

# error file handler
efh = logging.FileHandler('cynsearch.err.log')
efh.setFormatter(formatter)
efh.setLevel(logging.DEBUG)
log.addHandler(efh)

