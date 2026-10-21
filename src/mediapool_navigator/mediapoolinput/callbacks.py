import enum

class MPILineEditCallbacks(enum.Enum):

	CURRENT_FOLDER_CHANGED = enum.auto()
	"""The current folder has changed"""

	PATH_VALIDITY_CHANGED = enum.auto()
	"""The full path including subfolder is valid or not"""