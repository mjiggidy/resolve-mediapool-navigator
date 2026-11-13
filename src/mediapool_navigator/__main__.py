import sys, typing

from mediapool_navigator.utils import user_config
from resolvecommon import userpaths

from .app import MPNApplicationController

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes

PATH_USER_BASE = userpaths.get_user_data_base_path() / "GlowingPixel" / "Resolve Media Pool Navigator"
PATH_CFG_USER  = PATH_USER_BASE / "config" / "user_config.json"
PATH_LOG_USER  = PATH_USER_BASE / "logs" / "user_logs.log"

def main(bmd:typing.Any, resolve:dvrtypes.Resolve, fusion:dvrtypes.Fusion):

	user_config_manager = user_config.ConfigFileManager(PATH_CFG_USER)
	user_bookmarks = user_config_manager.bookmarks()

	try:
		start_folder = resolve.GetProjectManager().GetCurrentProject().GetMediaPool().GetCurrentFolder()

	except Exception as e:
		
		print("Not setting folder: ", e, file=sys.stderr)
		start_folder = None

	app = MPNApplicationController(
		bmd,
		resolve,
		fusion,
		bookmarks    = user_bookmarks,
		start_folder = start_folder,
	)

	user_config_manager.write_user_config(
		bookmarks = app.main_controller().bookmarks_controller().folder_paths()
	)

if __name__ == "__main__":

	main()