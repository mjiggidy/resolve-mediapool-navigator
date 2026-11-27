import pathlib, logging, typing, json
from os import PathLike

from .. import SHOW_NAG, DEFAULT_WINDOW_SIZE

_logger = logging.getLogger(__name__)

CURRENT_CONFIG_VERSION = 1
"""The current config schema version"""

class ConfigFileManager:
	"""Read and write the config files"""

	def __init__(self, path_user_config:str|PathLike[str]):

		self._path_user_config = pathlib.Path(path_user_config)
		self._user_config      = self.read_user_config()

		_logger.debug("Config file manager initiated with path %s", self._path_user_config)

	def user_config(self) -> dict[str, typing.Any]:
		"""Raw user config dict"""

		return self._user_config

	def read_user_config(self) -> dict[str, typing.Any]:
		"""Read user config from `.json` on disk"""

		user_config = {}

		try:

			with open(self._path_user_config) as json_config:

				user_config = json.load(json_config)
				_logger.debug("Loaded saved config from %s: %s", self._path_user_config, user_config)

		except PermissionError as e:

			_logger.error("Error accessing config file path %s: %s", self._path_user_config, e)
			_logger.debug("Additional info:", exc_info=True)
			pass

		except json.JSONDecodeError as e:

			_logger.error("Error decoding %s: %s", self._path_user_config, e)
			_logger.debug("Additional info:", exc_info=True)
			pass

		except FileNotFoundError:

			_logger.debug("No config file found at %s. To The Defaults!", self._path_user_config)
			_logger.debug("Additional info:", exc_info=True)
			pass

		except Exception as e:

			_logger.error("Strange error accessing %s: %s", self._path_user_config, e)
			_logger.debug("Additional info:", exc_info=True)
			pass

		# Check config version
		# NOTE: Basic for now

		if not user_config:
			user_config["version"] = CURRENT_CONFIG_VERSION

		elif "version" not in user_config:
			
			_logger.error("Config file lacks schema version number.  Invalidating!")
			user_config = {"version": CURRENT_CONFIG_VERSION}

		elif user_config["version"] > CURRENT_CONFIG_VERSION:
			
			_logger.error("Config file schema version is greater than supported.  Invalidating!")
			user_config = {"version": CURRENT_CONFIG_VERSION}

		return user_config

	def bookmarks(self) -> list[str]:
		"""Saved user bookmarks"""

		user_bookmarks = self._user_config.get("bookmarks", [])

		if not isinstance(user_bookmarks, list):
		
			_logger.error("User bookmarks are not in a known format.  Ignoring.")
			user_bookmarks = []

		return user_bookmarks

	def bookmarks_visible(self) -> bool:

		visible = self._user_config.get("bookmarks_visible", True)

		if not isinstance(visible, bool):

			_logger.error("Bookmark visibility not an expected bool.  Ignoring.")
			visible = True

		return visible

	def last_window_size(self) -> list[int]:

		try:
			last_window_size = self._user_config["window_size"]
			if not all(isinstance(x, int) for x in last_window_size) or not len(last_window_size) == 2:
				raise ValueError
			return last_window_size
		except Exception as e:
			return DEFAULT_WINDOW_SIZE
		

	def debug_logs(self) -> bool:
		"""Should logs use debug"""

		try:
			return bool(self._user_config["debug_logs"])
		except:
			return False

	def show_nag(self) -> bool:
		"""Show the little Donate nag"""

		try:
			return bool(self._user_config["show_nag"])
		except:
			return SHOW_NAG

	def write_user_config(self,
		bookmarks:list[str],
		bookmarks_visible:bool,
		window_size:list[int]|None,
	):
		"""Write user config to disk"""

		self._user_config.update({
			"version"  : CURRENT_CONFIG_VERSION,
			"bookmarks": bookmarks,
			"bookmarks_visible": bookmarks_visible,
		})

		if window_size:
			self._user_config["window_size"] = window_size

		# Roll in `debug_logs` if True
		if self.debug_logs():
			self._user_config["debug_logs"] = True

		# Roll in `show_nag` if it's False
		if not self.show_nag():
			self._user_config["show_nag"] = False

		try:

			self._path_user_config.parent.mkdir(parents=True, exist_ok=True)

			with open(self._path_user_config, "w") as json_file:

				json.dump(self._user_config, json_file, indent="\t")
				_logger.debug("Wrote config to %s: %s", self._path_user_config, self._user_config)

		except Exception as e:
			
			_logger.error("Strange error writing %s: %s", self._path_user_config, e, exc_info=True)
			pass