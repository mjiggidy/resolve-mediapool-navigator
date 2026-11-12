import typing, logging
from ._callbacks import MPNBookmarksCallbacks

_logger = logging.getLogger(__name__)

class MPNBookmarksController:
	"""Turns a `Tree` into a list of folder bookmarks"""

	def __init__(self, treeview:object):

		self._tree_bookmarks = treeview

		self._callbacks:dict[MPNBookmarksCallbacks, list[typing.Callable]] = dict()

		# Register callback types
		for callback in MPNBookmarksCallbacks:
			self._callbacks[callback] = []

	def register_window_handle(self, window_handle:object):
		"""Register `TextEdited` event with dispatcher window handle"""
		
		# TODO: Figure out how to set TextEdited event on the line edit in the constructor?

		window_handle.On[self._tree_bookmarks.ID].ItemActivated = self._on_folder_chosen
		window_handle.On[self._tree_bookmarks.ID].ItemClicked   = self._on_folder_clicked

	# Callbacks

	def register_callback(self, callback:MPNBookmarksCallbacks, callback_function:typing.Callable):
		"""Register a callback function"""

		_logger.debug("Callback to %s registered with %s", callback, callback_function)

		self._callbacks[callback].append(callback_function)

	def _send_callback(self, callback:MPNBookmarksCallbacks, args:typing.Any=None):

		_logger.debug("Emitting callback %s", callback)
		
		for cb in self._callbacks[callback]:
			cb(args)

	def _on_folder_clicked(self, event:dict):

		self._send_callback(MPNBookmarksCallbacks.FOLDER_HIGHLIGHTED, event["item"].Text[0])

	def _on_folder_chosen(self, event:dict):

		self._send_callback(MPNBookmarksCallbacks.FOLDER_CHOSEN, event["item"].Text[0])

	# Modify paths

	def folder_paths(self) -> list[str]:
		"""A list of current folder paths"""

		return [self._tree_bookmarks.TopLevelItem(idx).Text[0] for idx in range(self._tree_bookmarks.TopLevelItemCount())]
	
	def add_folder_path(self, folder_path:str):
		"""Add a new folder path"""

		if folder_path not in self.folder_paths():

			new_item = self._tree_bookmarks.NewItem()
			new_item.Text[0] = folder_path
			self._tree_bookmarks.InsertTopLevelItem(0, new_item)

		else:
			_logger.debug("Folder path %s already added", folder_path)

		self.select_folder_path(folder_path)

	def remove_folder_path(self, folder_path:str):
		"""Remove a given folder path"""

		for idx in range(self._tree_bookmarks.TopLevelItemCount()):

			if self._tree_bookmarks.TopLevelItem(idx).Text[0] == folder_path:

				_logger.debug("Removing folder path %s", folder_path)

				self._tree_bookmarks.TakeTopLevelItem(idx)
				return

		_logger.debug("Folder path not found for removal: %s", folder_path)

		raise ValueError("Path not found in list:", folder_path)

	def select_folder_path(self, folder_path:str):

		for item in (self._tree_bookmarks.TopLevelItem(idx) for idx in range(self._tree_bookmarks.TopLevelItemCount())):

			item.Selected = item.Text[0] == folder_path

	def selected_folder_path(self) -> str|None:
		"""Get the currently selected folder path, or `None`"""

		selected_items = list(self._tree_bookmarks.SelectedItems().values())

		return selected_items[0].Text[0] if selected_items else None

	def reorder_selection(self, move_up:bool=True):
		"""Move the selected folder up (default) or down"""

		try:
			selected_item = next(iter(self._tree_bookmarks.SelectedItems().values()))
	
		except Exception as e:
			
			_logger.debug("Skipped re-ordering because nothing selected")
			return
		
		selected_index = self._tree_bookmarks.IndexOfTopLevelItem(selected_item)
		selected_text  = selected_item.Text[0]

		dest_index = max(0, selected_index-1) if move_up else min(self._tree_bookmarks.TopLevelItemCount()-1, selected_index+1)

		if selected_index == dest_index:
			
			_logger.debug("Not reordering %s because already at extents", selected_text)
			return

		dest_item = self._tree_bookmarks.TopLevelItem(dest_index)
		dest_text = dest_item.Text[0]

		# NOTE TO SELF ABOUT ALL THIS:
		# Swapping the text of the items isn't my favorite plan of attack, but there's 
		# a lot of weirdness around item and "current item" stuff that just doesn't seem 
		# to work out well if you "Take" and re-insert actual `TreeItem`s.

		dest_item    .Text[0] = selected_text
		selected_item.Text[0] = dest_text

		selected_item.Selected = False
		dest_item    .Selected = True

		self._tree_bookmarks.ScrollToItem(dest_item)