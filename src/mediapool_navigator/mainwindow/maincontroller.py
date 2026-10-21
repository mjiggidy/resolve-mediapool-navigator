from __future__ import annotations

import typing

from . import mainwidget

from .. import __VERSION__, URL_GITHUB, URL_DONATE
from ..bookmarks import MPIBookmarkManager
from ..bookmarks import MPIBookmarkCallbacks
from mediapoolinput import MPILineEditCallbacks, MPILineEditController

from resolvecommon import folders

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes

class MPNMainController:
	"""Main application controller"""

	def __init__(self, project_manager:dvrtypes.ProjectManager, main_widget:mainwidget.MPNMainWindow):

		self._resolve_project_manager = project_manager
		self._main_widget = main_widget

		self.set_info_label(version_string=__VERSION__, github_url=URL_GITHUB, donate_url=URL_DONATE)

		self._media_pool_input_controller = MPILineEditController(self._resolve_project_manager, self._main_widget.media_pool_path_editor())
		self._bookmarks_controller        = MPIBookmarkManager(self._main_widget.bookmark_list_view())

		self._media_pool_input_controller.current_folder_info().register_callback(MPILineEditCallbacks.CURRENT_FOLDER_CHANGED, self._update_combo_choices)
		self._media_pool_input_controller.current_folder_info().register_callback(MPILineEditCallbacks.PATH_VALIDITY_CHANGED, self._on_path_validity_changed)
		self._bookmarks_controller.register_callback(MPIBookmarkCallbacks.FOLDER_HIGHLIGHTED, self._on_bookmark_highlighted)
		self._bookmarks_controller.register_callback(MPIBookmarkCallbacks.FOLDER_CHOSEN, self._on_go_button_clicked)

		self._combo_options:list[str] = []

		start_folder = self._resolve_project_manager.GetCurrentProject().GetMediaPool().GetCurrentFolder()

		if start_folder:

			self.set_ready(False)
			try:
				self._media_pool_input_controller.set_path_from_folder(start_folder)
			except Exception as e:
				print(e)

			self.set_ready(True)

	def _update_combo_choices(self, folder):

		if self._combo_options == self._media_pool_input_controller.current_folder_info().subfolder_paths():
			return

		user_text = self._main_widget.media_pool_path_editor().Text

		self._combo_options = self._media_pool_input_controller.current_folder_info().subfolder_paths()

		self._main_widget.media_pool_path_combo().Clear()
		self._main_widget.media_pool_path_combo().AddItems(self._combo_options)

		self._main_widget.media_pool_path_editor().Text = user_text

	def register_window_handle(self, window_handle:object):

#		window_handle.On[mainwidget.ID_BTN_GO].Clicked          = self._on_go_button_clicked
		window_handle.On[self._main_widget.button_use_current().ID].Clicked           = self._on_set_current_button_clicked
		window_handle.On[self._main_widget.media_pool_path_editor().ID].ReturnPressed = self._on_go_button_clicked

		window_handle.On[self._main_widget.button_add_bookmark().ID].Clicked          = self._on_add_bookmark

		self._media_pool_input_controller.register_window_handle(window_handle)
		self._bookmarks_controller.register_window_handle(window_handle)

	def _on_path_validity_changed(self, is_valid:bool):

		self._main_widget.button_add_bookmark().Enabled = is_valid

	def _on_add_bookmark(self, event:dict):

		self._bookmarks_controller.add_folder_path(self._main_widget.media_pool_path_editor().Text)

	def _on_bookmark_highlighted(self, folder_path:str):

		self.set_ready(False)
		self._media_pool_input_controller.set_path_from_text(folder_path)

		self.set_ready(True)

		self._main_widget.media_pool_path_combo().SetFocus()

	def _on_set_current_button_clicked(self, event:dict):

		self.set_ready(False)

		current_folder = self._resolve_project_manager.GetCurrentProject().GetMediaPool().GetCurrentFolder()

		if current_folder:
			self._media_pool_input_controller.set_path_from_folder(current_folder)

		self.set_ready(True)
		self._main_widget._txt_media_pool_path.SetFocus("OtherFocusReason")

	def _on_go_button_clicked(self, event:dict):

		self.set_ready(False)

		mp = self._resolve_project_manager.GetCurrentProject().GetMediaPool()

		folder_path = self._main_widget._txt_media_pool_path.Text

		try:

			if folder_path.strip():
				folder = folders.get_folder_from_path(folder_path, mp.GetRootFolder())
			else:
				folder = mp.GetRootFolder()
				
			mp.SetCurrentFolder(folder)

		except Exception as e:

			print(e)

		self.set_ready(True)

		self._bookmarks_controller.select_folder_path(folder_path)
		self._main_widget.media_pool_path_combo().SetFocus()


	def set_ready(self, is_ready:bool=True):

		self._main_widget.button_use_current().Enabled    = is_ready
		self._main_widget.button_add_bookmark().Enabled   = is_ready
		self._main_widget.media_pool_path_combo().Enabled = is_ready
		self._main_widget.bookmark_list_view().Enabled    = is_ready

	def set_info_label(self, /, version_string:str, github_url:str, donate_url:str=""):

		parts = [
			f"v{version_string}",
			f"<a href=\"{github_url}\">Github</a>",
		]

		if donate_url:
			parts.append(f"<a href=\"{donate_url}\">Donate</a>")

		self._main_widget.info_label().Text = " | ".join(parts)

	def bookmarks_controller(self) -> MPIBookmarkManager:

		return self._bookmarks_controller