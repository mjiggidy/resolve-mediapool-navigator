"""
Function(s?) for getting relevant paths
"""

import pathlib, os, sys

def get_user_base_path() -> pathlib.Path:
	"""Get the proper user location depending on OS and such"""

	platform_name = sys.platform.lower()

	if platform_name == "darwin":
		app_data = pathlib.Path.home() / "Library" / "Application Support"

	elif platform_name.startswith("win"):
		app_data = pathlib.Path(os.environ.get("APPDATA")) or pathlib.Path.home() / "AppData" / "Roaming"

	else:

		# NOTE: Supposedly Linux does not yet support Workflow Integrations.  FUTURE PROOFING?!
		app_data = pathlib.Path(os.environ.get("XDG_CONFIG_HOME")) or pathlib.Path.home() / ".config"

	return app_data / "GlowingPixel" / "Resolve Media Pool Navigator"