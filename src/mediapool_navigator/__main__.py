from .mainwindow import maincontroller, mainwidget
from . import ui, dispatcher


import json, sys
PATH_SETTINGS = "mpn_settings.json"


def main():

	def _on_main_closed(event:dict):

		settings = {
			"Bookmarks" : app.bookmarks_controller().folder_paths()
		}

		try:
			with open(PATH_SETTINGS, "w") as handle_settings:
				json.dump(settings, handle_settings, indent="\t")
		
		except Exception as e:
			print("Error writing settings: ", e, file=sys.stderr)

		dispatcher.ExitLoop(0)
	
	main_widget = mainwidget.MPNMainWindow(ui)
	app = maincontroller.MPNMainController(main_widget)

	wnd_main = dispatcher.AddWindow({
			"ID": mainwidget.ID_WINDOW_MAIN,
			"WindowTitle": "Media Pool Navigator Pro!",
			"FixedSize": [500,90],
			"Events": {"Close": True},
		}, [main_widget.layout()])

	wnd_main.On[mainwidget.ID_WINDOW_MAIN].Close = _on_main_closed

	app.register_window_handle(wnd_main)
	wnd_main.RecalcLayout()

	settings = dict()
	
	try:
		
		with open(PATH_SETTINGS) as handle_settings:
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