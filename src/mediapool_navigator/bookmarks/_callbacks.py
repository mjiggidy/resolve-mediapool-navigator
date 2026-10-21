import enum

class MPIBookmarkCallbacks(enum.Enum):
	"""Available callbacks from the Bookmark Manager"""

	FOLDER_HIGHLIGHTED = enum.auto()
	"""User highlighted a folder path"""

	FOLDER_CHOSEN      = enum.auto()
	"""User activated a folder path"""