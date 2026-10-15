from __future__ import annotations
import logging, typing

if typing.TYPE_CHECKING:
	import DaVinciResolveScript as dvr

from .. import resolve
from ..utils import folders, formatting
from .callbacks import MPILineEditCallbacks

_logger     = logging.getLogger(__name__)

class _MPIFolderInfo:
	"""Path and subfolder info for a given folder"""

	EXCLUDE_MASTER = True

	def __init__(self, ):

		self._folder_handle:dvr.Folder|None = None
		self._folder_path:str   = ""

		self._callbacks:dict[MPILineEditCallbacks, list[typing.Callable]] = dict()

		# Register callback types
		for callback in MPILineEditCallbacks:
			self._callbacks[callback] = []

	def _set_folder(self, folder:dvr.Folder) -> bool:
		"""Set the current folder.  Returns `True` if the folder changed since last."""

		if self._folder_handle and self._folder_handle.GetUniqueId() == folder.GetUniqueId():

			_logger.debug("Set current folder ignored because unchanged")
			return False

		self._folder_path   = self._format_folder_path(folders.get_path_from_folder(folder))
		self._folder_handle = folder

		self._send_callback(MPILineEditCallbacks.CURRENT_FOLDER_CHANGED, folder)

		return True

	def _format_folder_path(self, folder_path_raw:str) -> str:
		"""Format folder string for display"""

		if self.EXCLUDE_MASTER and folder_path_raw.startswith("/Master"):
			return folder_path_raw[len("/Master/"):]

		else:
			return folder_path_raw

	def _set_folder_path(self, folder_path:str) -> bool:
		"""Set the current folder from a given path string.  Returns `True` if the folder changed since last."""

		if self._folder_path == folder_path:
			return False
		
		root_folder = resolve.GetProjectManager().GetCurrentProject().GetMediaPool().GetRootFolder()
		
		self._folder_handle = folders.get_folder_from_path(folder_path, root_folder)
		self._folder_path   = self._format_folder_path(folder_path)

		self._send_callback(MPILineEditCallbacks.CURRENT_FOLDER_CHANGED, self._folder_handle)

		return True

	def _clear_folder(self) -> bool:
		"""Clear the current folder.  Returns `True` if this is a change."""

		if not self._folder_handle:
			return False

		self._folder_handle = None
		self._folder_path   = ""

		self._send_callback(MPILineEditCallbacks.CURRENT_FOLDER_CHANGED, self._folder_handle)

		return True

	def folder_handle(self) -> dvr.Folder|None:
		"""The current folder handle"""

		return self._folder_handle

	def folder_path(self) -> str:
		"""The current folder"""

		return self._folder_path

	def folder_is_valid(self) -> bool:
		"""Pointing to a valid folder path"""

		return bool(self._folder_handle)

	def subfolder_handles(self) -> list[dvr.Folder]:
		"""List of available subfolder handles"""

		return sorted(
			self._folder_handle.GetSubFolderList(),
			key = lambda f: formatting.format_string_for_natural_sort(f.GetName())
		) if self.folder_is_valid() else []

	def subfolder_paths(self) -> list[str]:
		"""List of available subfolder paths"""

#		print("Folder path is ", self.folder_path(), "For base folder", self.folder_handle().GetName())

		print("Folder path:", self.folder_path())

		return [str(self.folder_path() + "/" + f.GetName()).lstrip("/") for f in self.subfolder_handles()]

	def register_callback(self, callback:MPILineEditCallbacks, callback_function:typing.Callable):
		"""Register a callback function"""

		self._callbacks[callback].append(callback_function)

	def _send_callback(self, callback:MPILineEditCallbacks, args:typing.Any=None):

		for cb in self._callbacks[callback]:
			cb(args)
		

class MPILineEditController:

	def __init__(self, line_edit:object):

		self._folder_tracker   = _MPIFolderInfo()

		self._line_edit        = line_edit
		self._last_edit_length = len(self._line_edit.Text)

	def register_window_handle(self, window_handle:object):
		"""Register `TextEdited` event with dispatcher window handle"""
		
		# TODO: Figure out how to set TextEdited event on the line edit in the constructor?

		window_handle.On[self._line_edit.ID].TextEdited       = self._on_user_modified_path
		window_handle.On[self._line_edit.ID].EditingFinished  = self._on_user_finished_path

	def current_folder_info(self) -> _MPIFolderInfo:
		"""Info about the current base folder"""

		return self._folder_tracker

	def set_path_from_folder(self, folder:object):
		"""Set the current path from a given media pool folder object"""

		self._folder_tracker._set_folder(folder)

		folder_path = self._folder_tracker.folder_path()

		self.set_path_from_text("", folder_path)

	def set_path_from_text(self, base_text:str, autocomplete_text:str=""):
		"""Set the current path from text"""

		self._line_edit.Text   = base_text + autocomplete_text
		self._line_edit.SetSelection(len(self._line_edit.Text), -len(autocomplete_text))

		self._last_edit_length = len(base_text)

		_logger.debug("Edit length set to %s", self._last_edit_length)
	
	def _on_user_finished_path(self, event:dict):
		"""Reformat/standardize user input"""

		self._line_edit.Text = self._line_edit.Text.strip("/")

	def _on_user_modified_path(self, event:dict):
		"""Test event for media pool browser thing"""

		current_edit_length = len(event["Text"])

		# Add a trailing slash to allow for "root" folders to be split between "" (Master) and the partial folder name
		# NOTE: Yes, that comment made sense to me when I wrote it
		
		sanitized_text:str = "/" + event["Text"] if not event["Text"].startswith("/") else event["Text"]

		# Split input string into base path and "partial" (or... full, really) folder name
		# NOTE: For a trailing slash, partial_folder_name becomes "" which is perfect

		base_path, partial_folder_name = sanitized_text.rsplit("/", 1)
		
		# Try to resolve the base Folder handle from the given path, and query any subfolders therein
		# If any of this fails, something's invalid about the path, so just set subfolders to an empty
		# list so we don't autocomplete anything atoll, and any subfolder listings are cleared out

		try:
			self._folder_tracker._set_folder_path(base_path)
	
		except FileNotFoundError as e:
			
			_logger.error("Invalid media pool folder: %s", e)
			self._folder_tracker._clear_folder()

		filtered_subfolders = list(
			filter(lambda f: f.GetName().startswith(partial_folder_name), self._folder_tracker.subfolder_handles())
		)

		# If the user is editing text (either backspacin' or editing in the middle), don't autocomplete
		if any([
#			not filtered_subfolders,
			current_edit_length <= self._last_edit_length,
			self._line_edit.CursorPosition < current_edit_length,
		]):
			
#			if not filtered_subfolders:
#				logger.debug("Because no subfolders")
			
			if current_edit_length <= self._last_edit_length:
				_logger.debug("Because edit length: current_length=%s, last_length=%s", current_edit_length, self._last_edit_length)
			
			if self._line_edit.CursorPosition < current_edit_length:
				_logger.debug("Because cursor position")

			self._last_edit_length = current_edit_length
			return


		next_subfolder_name = filtered_subfolders[0].GetName() if filtered_subfolders else ""

		self.set_path_from_text(event["Text"], next_subfolder_name[len(partial_folder_name):])