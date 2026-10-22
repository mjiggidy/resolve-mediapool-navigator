PACKAGE_ID = "com.glowingpixel.navigator"

import sys, pathlib, typing
from resolvecommon import userpaths

if typing.TYPE_CHECKING:

	import DaVinciResolveScript as dvrtypes
	
	bmd    :object
	resolve:dvrtypes.Resolve
	fusion :dvrtypes.Fusion

PATH_WORKFLOW_INTEGRATION_PLUGINS = userpaths.workflow_integrations_path()
PATH_LIB = PATH_WORKFLOW_INTEGRATION_PLUGINS / PACKAGE_ID / "lib"

if not pathlib.Path(PATH_LIB).is_dir():

	print("Required library path not found: ", PATH_LIB, file=sys.stderr)
	sys.exit(1)

if str(PATH_LIB) not in sys.path:
	sys.path.insert(0, str(PATH_LIB))

from mediapool_navigator.__main__ import main

try:
	# Pass injected variables
	main(bmd=bmd, resolve=resolve, fusion=fusion)

except Exception as e:
	print(f"Quit unexpectedly: {str(e)}", file=sys.stderr)