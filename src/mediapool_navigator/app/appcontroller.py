from __future__ import annotations

import typing

from .. import __VERSION__, URL_GITHUB, URL_DONATE, TITLE_WINDOW, SHOW_NAG, ID_WINDOW_MAIN, DEFAULT_WINDOW_SIZE
from .. import mainwindow

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes

class MPNApplicationController:
	"""Set up application-specific window and settings"""

	def __init__(
		self,
		bmd:typing.Any,
		resolve:dvrtypes.Resolve,
		fusion:dvrtypes.Fusion,
		/,
		bookmarks:list[str]|None = None,
		bookmarks_visible:bool = True,
		start_folder:dvrtypes.Folder|None = None,
		show_nag:bool = SHOW_NAG,
		window_title:str = TITLE_WINDOW,
		window_size:list[int] = DEFAULT_WINDOW_SIZE,
	):

		dispatcher = bmd.UIDispatcher(fusion.UIManager)

		main_widget = mainwindow.MPNMainWindow(
			ui_manager=fusion.UIManager
		)
		
		self._main_controller = mainwindow.MPNMainWidgetController(
			project_manager=resolve.GetProjectManager(),
			main_widget=main_widget
		)

		self._wnd_main = dispatcher.AddWindow({
				"ID": ID_WINDOW_MAIN,
				"WindowTitle": window_title,
				"FixedSize": window_size,
				"Events": {"Close": True, "KeyPress": True, "KeyRelease": True,},
			}, [main_widget.layout()])

		self._wnd_main.On[ID_WINDOW_MAIN].Close = lambda _: dispatcher.ExitLoop(0)

		self._main_controller.register_window_handle(self._wnd_main)

		self._wnd_main.Show()

		# NOTE: Setting initial values AFTER showing the window
		# so that window geometry isn't affected by things like
		# long folder paths in the combo box

		self._main_controller.set_info_label(
			version_string=__VERSION__,
			github_url=URL_GITHUB,
			donate_url=URL_DONATE if show_nag else None
		)

		if start_folder:
			self._setup_start_folder(start_folder)

		if bookmarks:
			self._setup_bookmarks(bookmarks)

		if not all((bookmarks_visible, bookmarks)):
			self.main_controller().toggle_bookmark_visibility()

		dispatcher.RunLoop()

	def _setup_bookmarks(self, bookmarks:list[str]):

		for bookmark in reversed(bookmarks):
			self._main_controller.bookmarks_controller().add_folder_path(bookmark)

	def _setup_start_folder(self, start_folder:dvrtypes.Folder):

		self._main_controller.set_current_path_from_folder(start_folder)

	def main_controller(self) -> mainwindow.MPNMainWidgetController:

		return self._main_controller

	def window_handle(self) -> object:

		return self._wnd_main