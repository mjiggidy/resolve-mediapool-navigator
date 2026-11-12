import typing

from .. import mainwindow

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes

ID_WINDOW_MAIN = "com.glowingpixel.navigator.mainwindow"

class MPNApplicationController:
	"""Set up application-specific window and settings"""

	def __init__(
		self,
		bmd:typing.Any,
		resolve:dvrtypes.Resolve,
		fusion:dvrtypes.Fusion,
		/,
		bookmarks:list[str]|None = None,
		start_folder:dvrtypes.Folder|None = None,
	):

		dispatcher = bmd.UIDispatcher(fusion.UIManager)

		main_widget = mainwindow.MPNMainWindow(
			ui_manager=fusion.UIManager
		)
		
		self._main_controller = mainwindow.MPNMainWidgetController(
			project_manager=resolve.GetProjectManager(),
			main_widget=main_widget
		)

		wnd_main = dispatcher.AddWindow({
				"ID": ID_WINDOW_MAIN,
				"WindowTitle": "Media Pool Navigator Pro!",
				"FixedSize": [500,200],
				"Events": {"Close": True, "KeyRelease": True,},
			}, [main_widget.layout()])

		wnd_main.On[ID_WINDOW_MAIN].Close = lambda _: dispatcher.ExitLoop(0)

		self._main_controller.register_window_handle(wnd_main)

		wnd_main.Show()

		# NOTE: Setting initial values AFTER showing the window
		# so that window geometry isn't affected by things like
		# long folder paths in the combo box

		if start_folder:
			self._setup_start_folder(start_folder)

		if bookmarks:
			self._setup_bookmarks(bookmarks)

		dispatcher.RunLoop()

	def _setup_bookmarks(self, bookmarks:list[str]):

		for bookmark in reversed(bookmarks):
			self._main_controller.bookmarks_controller().add_folder_path(bookmark)

	def _setup_start_folder(self, start_folder:dvrtypes.Folder):

		self._main_controller.set_current_path_from_folder(start_folder)