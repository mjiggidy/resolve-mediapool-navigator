import logging

_logger = logging.getLogger(__name__)

class MPNSuggestionsBoxController:

	def __init__(self, combo_box:object):

		self._combo_box = combo_box

	def suggestions(self) -> list[str]:
		"""Current list of suggestions"""

		return [self._combo_box.ItemText[idx] for idx in range(self._combo_box.Count())]

	def set_suggestions(self, suggestions:list[str]):
		"""Clear the suggetsions box and set a new list"""

		_logger.debug("Setting suggestions box to: %s", suggestions)

		self._combo_box.Clear()
		self._combo_box.AddItems(suggestions)

	def suggestions_box(self) -> object:
		"""The combo box"""

		return self._combo_box