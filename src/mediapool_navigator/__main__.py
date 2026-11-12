import json, sys, typing
from .app import MPNApplicationController
from resolvecommon import userpaths

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes

PATH_USER_BASE = userpaths.get_user_data_base_path() / "GlowingPixel" / "Resolve Media Pool Navigator"
PATH_CFG_USER  = PATH_USER_BASE / "config" / "user_config.json"
PATH_LOG_USER  = PATH_USER_BASE / "logs" / "user_logs.log"

def main(bmd:typing.Any, resolve:dvrtypes.Resolve, fusion:dvrtypes.Fusion):
	def _on_main_closed(event:dict):

		settings = {
			"Bookmarks" : app.bookmarks_controller().folder_paths()
		}

		try:

			import pathlib
			pathlib.Path(PATH_CFG_USER).parent.mkdir(parents=True, exist_ok=True)
			
			with open(PATH_CFG_USER, "w") as handle_settings:
				json.dump(settings, handle_settings, indent="\t")
		
		except Exception as e:
			print("Error writing settings: ", e, file=sys.stderr)
	


	settings = dict()
	
	try:
		
		with open(PATH_CFG_USER) as handle_settings:
			settings.update(json.load(handle_settings))
	
	except Exception as e:
		print("Error loading settings: ", e, file=sys.stderr)

	user_bookmarks = settings.get("Bookmarks", [])

	if not isinstance(user_bookmarks, list):
		
		print("User bookmarks are not in a known format.  Ignoring.", file=sys.stderr)
		user_bookmarks = []

	# Set current folder
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



if __name__ == "__main__":

	main()