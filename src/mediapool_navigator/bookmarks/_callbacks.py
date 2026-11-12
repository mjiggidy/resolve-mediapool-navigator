import enum

class MPNBookmarksCallbacks(enum.Enum):
	"""Available callbacks from the Bookmarks controller"""

	FOLDER_HIGHLIGHTED = enum.auto()
	"""User highlighted a folder path"""

	FOLDER_CHOSEN      = enum.auto()
	"""User activated a folder path"""