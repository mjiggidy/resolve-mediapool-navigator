import typing
from ._callbacks import MPIBookmarkCallbacks

class MPIBookmarkManager:

	def __init__(self, treeview:object):

		self._tree_bookmarks = treeview

		self._callbacks:dict[MPIBookmarkCallbacks, list[typing.Callable]] = dict()

		# Register callback types
		for callback in MPIBookmarkCallbacks:
			self._callbacks[callback] = []

	def register_window_handle(self, window_handle:object):
		"""Register `TextEdited` event with dispatcher window handle"""
		
		# TODO: Figure out how to set TextEdited event on the line edit in the constructor?

		window_handle.On[self._tree_bookmarks.ID].ItemActivated = self._on_folder_chosen
		window_handle.On[self._tree_bookmarks.ID].ItemClicked   = self._on_folder_clicked


	def add_folder_path(self, folder_path:str):

		if folder_path not in self.folder_paths():

			new_item = self._tree_bookmarks.NewItem()
			new_item.Text[0] = folder_path
			self._tree_bookmarks.InsertTopLevelItem(0, new_item)

		self.select_folder_path(folder_path)

	def select_folder_path(self, folder_path:str):

		for item in (self._tree_bookmarks.TopLevelItem(idx) for idx in range(self._tree_bookmarks.TopLevelItemCount())):

			item.Selected = item.Text[0] == folder_path

	def remove_folder_path(self, folder_path:str):
		"""Remove a giveni folder path"""

		for idx in range(self._tree_bookmarks.TopLevelItemCount()):

			if self._tree_bookmarks.TopLevelItem(idx).Text[0] == folder_path:

				self._tree_bookmarks.TakeTopLevelItem(idx)
				return

		raise ValueError("Path not found in list:", folder_path)

	def selected_folder_path(self) -> str|None:
		"""Get the currently selected folder path, or `None`"""

		selected_indexes = list(self._tree_bookmarks.SelectedItems().values())

		if not selected_indexes:
			return None

		return selected_indexes[0].Text[0]

	def folder_paths(self) -> list[str]:
		"""A list of current folder paths"""

		return [self._tree_bookmarks.TopLevelItem(idx).Text[0] for idx in range(self._tree_bookmarks.TopLevelItemCount())]

	def _on_folder_clicked(self, event:dict):

		#print(event["item"].Text[0])

		self._send_callback(MPIBookmarkCallbacks.FOLDER_HIGHLIGHTED, event["item"].Text[0])

	def _on_folder_chosen(self, event:dict):

		self._send_callback(MPIBookmarkCallbacks.FOLDER_CHOSEN, event["item"].Text[0])

	def register_callback(self, callback:MPIBookmarkCallbacks, callback_function:typing.Callable):
		"""Register a callback function"""

		self._callbacks[callback].append(callback_function)

	def _send_callback(self, callback:MPIBookmarkCallbacks, args:typing.Any=None):

		for cb in self._callbacks[callback]:
			cb(args)