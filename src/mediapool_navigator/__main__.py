from __future__ import annotations

import sys, typing, logging

from mediapool_navigator.utils import user_config
from resolvecommon import userpaths

from . import ID_WINDOW_MAIN, RESOLVE_MINIMUM_VERSION
from .utils import logs
from .app import MPNApplicationController

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes

PATH_USER_BASE = userpaths.get_user_data_base_path() / "GlowingPixel" / "Resolve Media Pool Navigator"
PATH_CFG_USER  = PATH_USER_BASE / "config" / "user_config.json"
PATH_LOG_USER  = PATH_USER_BASE / "logs" / "user_logs.log"

def main(bmd:typing.Any, resolve:dvrtypes.Resolve, fusion:dvrtypes.Fusion):

	if win:= fusion.UIManager.FindWindow(ID_WINDOW_MAIN):

		win.Show()
		win.Raise()

		print("Window instance already running.  There can only be one.", file=sys.stderr)
		return

	logs.setup_logging(PATH_LOG_USER)
	_logger = logging.getLogger(__name__)

	try:

		resolve_version = resolve.GetVersion()
		logging.getLogger(__name__).debug("Resolve reports version=%s", resolve_version)

		if RESOLVE_MINIMUM_VERSION > resolve_version:
			raise RuntimeError(f"This plugin requires Resolve version {'.'.join(str(v) for v in RESOLVE_MINIMUM_VERSION)} or newer (got: {'.'.join(str(v) for v in resolve_version)})")

	except Exception as e:

		print("Cannot run: ", str(e), file=sys.stderr)
		return

	user_config_manager = user_config.ConfigFileManager(PATH_CFG_USER)

	if not user_config_manager.debug_logs():

		_logger.debug("No debug logs requested. Goodbye from me. :(")
		logging.getLogger().setLevel(logging.INFO)

	try:
		start_folder = resolve.GetProjectManager().GetCurrentProject().GetMediaPool().GetCurrentFolder()

	except Exception as e:
		
		_logger.error("Not setting folder: %s", e)
		_logger.debug("Additional info:", exc_info=True)
		
		start_folder = None

	app = MPNApplicationController(
		bmd,
		resolve,
		fusion,
		start_folder      = start_folder,
		bookmarks         = user_config_manager.bookmarks(),
		bookmarks_visible = user_config_manager.bookmarks_visible(),
	)

	user_config_manager.write_user_config(
		bookmarks = app.main_controller().bookmarks_controller().folder_paths(),
		bookmarks_visible = not app.main_controller().main_widget().bookmark_list_view().Hidden,
	)

if __name__ == "__main__":

	main()