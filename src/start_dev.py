import logging
from mediapool_navigator import __main__

import DaVinciResolveScript as bmd

logging.basicConfig(level=logging.DEBUG)

__main__.main(bmd, bmd.scriptapp("resolve"), bmd.scriptapp("fusion"))