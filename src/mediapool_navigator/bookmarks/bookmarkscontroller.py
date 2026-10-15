import typing
from .callbacks import MPIBookmarkCallbacks

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

		new_item = self._tree_bookmarks.NewItem()

		new_item.Text[0] = folder_path

		self._tree_bookmarks.AddTopLevelItem(new_item)

	def _on_folder_clicked(self, event:dict):

		#print(event["item"].Text[0])

		self._send_callback(MPIBookmarkCallbacks.FOLDER_HIGHLIGHTED, event["item"].Text[0])

#		index = self._tree_bookmarks.IndexOfTopLevelItem(event["item"])
#		folder = self._media_pool_input_controller.current_folder_info().subfolder_handles()[index]
#		self._media_pool_input_controller.set_path_from_folder(folder)

	def _on_folder_chosen(self, event:dict):

		self._send_callback(MPIBookmarkCallbacks.FOLDER_CHOSEN, event["item"].Text[0])

#		index = self._main_widget.bookmark_list_view().IndexOfTopLevelItem(event["item"])
#
#		folder = self._media_pool_input_controller.current_folder_info().subfolder_handles()[index]
#		self._media_pool_input_controller.set_path_from_folder(folder)
#		mp = resolve.GetProjectManager().GetCurrentProject().GetMediaPool()
#		mp.SetCurrentFolder(folder)

	def register_callback(self, callback:MPIBookmarkCallbacks, callback_function:typing.Callable):
		"""Register a callback function"""

		self._callbacks[callback].append(callback_function)

	def _send_callback(self, callback:MPIBookmarkCallbacks, args:typing.Any=None):

		for cb in self._callbacks[callback]:
			cb(args)