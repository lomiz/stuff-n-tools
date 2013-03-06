#!/usr/bin/python

import logging
logging.basicConfig(filename="myapp.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.debug('debug')
logging.info('infooooooo')
logging.warning('warningggg')
logging.error('errorrrrr')
logging.critical('panicccccc')
