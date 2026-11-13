from __future__ import annotations

import typing, logging

from mediapoolinput import MPILineEditCallbacks, MPILineEditController
from resolvecommon import folders

from . import _mainwidget

from .. import __VERSION__, URL_GITHUB, URL_DONATE, PREVENT_INVALID_BOOKMARKS

from ..bookmarks import MPNBookmarksController, MPNBookmarksCallbacks
from ..suggestionsbox import MPNSuggestionsBoxController

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvrtypes

KEY_ARROW_UP   = 16777235
KEY_ARROW_DOWN = 16777237
KEY_DELETE     = 16777223

_logger = logging.getLogger(__name__)

class MPNMainWidgetController:
	"""Main widget controller"""

	def __init__(self, project_manager:dvrtypes.ProjectManager, main_widget:_mainwidget.MPNMainWindow):

		self._resolve_project_manager = project_manager
		self._main_widget = main_widget

		self.set_info_label(version_string=__VERSION__, github_url=URL_GITHUB, donate_url=URL_DONATE)

		self._media_pool_input_controller = MPILineEditController(self._resolve_project_manager, self._main_widget.media_pool_path_editor())
		self._bookmarks_controller        = MPNBookmarksController(self._main_widget.bookmark_list_view())
		self._suggestions_controller      = MPNSuggestionsBoxController(self._main_widget.media_pool_path_combo())

		self._media_pool_input_controller.current_folder_info().register_callback(MPILineEditCallbacks.CURRENT_FOLDER_CHANGED, self._on_current_folder_changed)
		self._media_pool_input_controller.current_folder_info().register_callback(MPILineEditCallbacks.PATH_VALIDITY_CHANGED, self._on_path_validity_changed)
		
		self._bookmarks_controller.register_callback(MPNBookmarksCallbacks.FOLDER_HIGHLIGHTED, self._on_bookmark_highlighted)
		self._bookmarks_controller.register_callback(MPNBookmarksCallbacks.FOLDER_CHOSEN, self._on_go_button_clicked)

	def _on_current_folder_changed(self, folder:dvrtypes.Folder):

		current_subfolder_paths = self._suggestions_controller.suggestions()
		new_subfolder_paths     = self._media_pool_input_controller.current_folder_info().subfolder_paths()

		if set(current_subfolder_paths) == set(new_subfolder_paths):
			
			_logger.debug("Got `CURRENT_FOLDER_CHANGED`, but subfolders remain the same...")
			return

		_logger.debug("Setting new paths: %s (Currently: %s)", new_subfolder_paths, current_subfolder_paths)

		user_text = self._main_widget.media_pool_path_editor().Text
		
		self._suggestions_controller.set_suggestions(new_subfolder_paths)
		self._main_widget.media_pool_path_editor().Text = user_text

	def set_current_path_from_folder(self, folder:dvrtypes.Folder):

		self._media_pool_input_controller.set_path_from_folder(folder)

	def register_window_handle(self, window_handle:object):
		
		window_handle.On[self._main_widget.button_use_current().ID].Clicked           = self._on_set_current_button_clicked
		window_handle.On[self._main_widget.media_pool_path_editor().ID].ReturnPressed = self._on_go_button_clicked

		window_handle.On[self._main_widget.button_add_bookmark().ID].Clicked          = self._on_bookmark_button_clicked
		window_handle.On[window_handle.ID].KeyRelease                                 = self._on_key_released

		self._media_pool_input_controller.register_window_handle(window_handle)
		self._bookmarks_controller.register_window_handle(window_handle)

	def _on_key_released(self, event:dict):

		if event["IsAutoRepeat"] or not self._main_widget.bookmark_list_view().HasFocus():
			return

		if event["Key"] == KEY_DELETE:

			try:
				self._bookmarks_controller.remove_folder_path(self._bookmarks_controller.selected_folder_path())
			
			except ValueError as e:
				_logger.error("Error removing selected folder path from bookmarks: %s", e, exc_info=True)

		elif event["Key"] == KEY_ARROW_UP and event["Modifiers"]["ShiftModifier"]: # Alt+Up

			self._bookmarks_controller.reorder_selection()

		elif event["Key"] == KEY_ARROW_DOWN and event["Modifiers"]["ShiftModifier"]: # Alt+Down

			self._bookmarks_controller.reorder_selection(move_up=False)

	def _on_path_validity_changed(self, is_valid:bool):

		if PREVENT_INVALID_BOOKMARKS:
			self._main_widget.button_add_bookmark().Enabled = is_valid

	def _on_bookmark_button_clicked(self, event:dict):

		if(event["modifiers"]["AltModifier"]):
			self.toggle_bookmark_visibility()

		else:
			self._bookmarks_controller.add_folder_path(self._main_widget.media_pool_path_editor().Text)

	def toggle_bookmark_visibility(self):

		window_handle  = self._main_widget.bookmark_list_view().Window()
		window_size    = list(window_handle.Size().values())
		bookmarks_size = list(self._main_widget.bookmark_list_view().Size().values())

		if self._main_widget.bookmark_list_view().Hidden:

			window_handle.Resize({1: window_size[0], 2: window_size[1] + bookmarks_size[1]})
			self._main_widget.bookmark_list_view().Hidden = False
			window_handle.RecalcLayout()

		else:

			self._main_widget.bookmark_list_view().Hidden = True
			window_handle.RecalcLayout()
			window_handle.Resize({1: window_size[0], 2: window_size[1] - bookmarks_size[1]})

	def _on_bookmark_highlighted(self, folder_path:str):

		self._media_pool_input_controller.set_path_from_text(folder_path)

	def _on_set_current_button_clicked(self, event:dict):
		
		current_folder = self._resolve_project_manager.GetCurrentProject().GetMediaPool().GetCurrentFolder()

		if current_folder:
			self._media_pool_input_controller.set_path_from_folder(current_folder)

		self._main_widget._txt_media_pool_path.SetFocus("OtherFocusReason")

	def _on_go_button_clicked(self, event:dict):

		folder_path = self._main_widget.media_pool_path_editor().Text

		try:
			
			mp = self._resolve_project_manager.GetCurrentProject().GetMediaPool()

			if folder_path.strip():
				folder = folders.get_folder_from_path(folder_path, mp.GetRootFolder())
			
			else:
				folder = mp.GetRootFolder()
				
			mp.SetCurrentFolder(folder)

		except Exception as e:
			_logger.error("Error setting current folder to %s: %s", folder_path, e, exc_info=True)

		self._bookmarks_controller.select_folder_path(folder_path)
		self._main_widget.media_pool_path_combo().SetFocus()


	def set_ready(self, is_ready:bool=True):
		"""Set ready state of the widgets"""
		# NOTE: Currently unused

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

	def bookmarks_controller(self) -> MPNBookmarksController:

		return self._bookmarks_controller

	def suggestions_box_controller(self) -> MPNSuggestionsBoxController:

		return self._suggestions_controller

	def main_widget(self) -> _mainwidget.MPNMainWindow:
		"""The main widget this controller is assigned to"""

		return self._main_widget