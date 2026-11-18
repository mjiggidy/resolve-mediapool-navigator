"""
Function(s?) for log setup
"""

import logging, pathlib
from os import PathLike

LOG_FORMAT = "[%(asctime)s]\t%(levelname)s\t%(name)s\t%(message)s"
LOG_FILE_SIZE_MAX_BYTES = 1024 * 1024 # 1 MB
LOG_FILE_MAX_COUNT      = 5

def setup_logging(log_file_path:str|PathLike[str]|None=None):
	"""Establish logging handlers"""

	root = logging.getLogger()
	root.setLevel(logging.DEBUG)

	formatter = logging.Formatter(LOG_FORMAT)

	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.INFO)
	console_handler.setFormatter(formatter)

	root.addHandler(console_handler)

	if log_file_path is None:

		logging.getLogger(__name__).info("Hello from %s.  No file path provided.  We loggin without logs I guess.", __name__)
		return

	from logging.handlers import RotatingFileHandler

	try:
		
		log_file_path = pathlib.Path(log_file_path)
		log_file_path.parent.mkdir(parents=True, exist_ok=True)

	except Exception as e:
		logging.getLogger(__name__).error("Could not create log path: %s", e, exc_info=True)

	else:
		
		file_handler = RotatingFileHandler(str(log_file_path), maxBytes=LOG_FILE_SIZE_MAX_BYTES, backupCount=LOG_FILE_MAX_COUNT)
		file_handler.setLevel(logging.DEBUG)
		file_handler.setFormatter(formatter)

		root.addHandler(file_handler)

	logging.getLogger(__name__).info("Hello from %s", __name__)