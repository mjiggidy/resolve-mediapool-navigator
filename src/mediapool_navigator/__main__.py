import json, sys, typing
from .mainwindow import maincontroller, mainwidget
from resolvecommon import userpaths, folders

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes

PATH_USER_BASE = userpaths.get_user_data_base_path() / "GlowingPixel" / "Resolve Media Pool Navigator"
PATH_CFG_USER  = PATH_USER_BASE / "config" / "user_config.json"
PATH_LOG_USER  = PATH_USER_BASE / "logs" / "user_logs.log"

def main(bmd:typing.Any, resolve:dvrtypes.Resolve, fusion:dvrtypes.Fusion):

	dispatcher = bmd.UIDispatcher(fusion.UIManager)

	def _on_main_closed(event:dict):
		"""Clean up 'n' close"""

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

		dispatcher.ExitLoop(0)
	
	main_widget = mainwidget.MPNMainWindow(ui_manager=fusion.UIManager)
	app = maincontroller.MPNMainController(project_manager=resolve.GetProjectManager(), main_widget=main_widget)

	wnd_main = dispatcher.AddWindow({
			"ID": mainwidget.ID_WINDOW_MAIN,
			"WindowTitle": "Media Pool Navigator Pro!",
			"FixedSize": [500,200],
			"Events": {"Close": True, "KeyRelease": True,},
		}, [main_widget.layout()])

	wnd_main.On[mainwidget.ID_WINDOW_MAIN].Close = _on_main_closed

	app.register_window_handle(wnd_main)
#	wnd_main.RecalcLayout()

	try:
		
		start_folder = resolve.GetProjectManager().GetCurrentProject().GetMediaPool().GetCurrentFolder()
		start_path   = folders.get_path_from_folder(start_folder, relative_to=resolve.GetProjectManager().GetCurrentProject().GetMediaPool().GetRootFolder()).strip("/Master/")

		if start_folder:
			app._media_pool_input_controller.set_path_from_text(start_path, show_autocomplete=False)

	except Exception as e:

		print("Didn't set start folder: ", e)

	settings = dict()
	
	try:
		
		with open(PATH_CFG_USER) as handle_settings:
			settings.update(json.load(handle_settings))
	
	except Exception as e:
		print("Error loading settings: ", e, file=sys.stderr)

	if "Bookmarks" in settings:

		for folder_path in reversed(settings["Bookmarks"]):
			app.bookmarks_controller().add_folder_path(folder_path)

	wnd_main.Show()

	dispatcher.RunLoop()


if __name__ == "__main__":

	main()