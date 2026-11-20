from ..gui.abstract_widget import MPNAbstractWidget

ID_CMB_PATH          = "cmb_mediapool_path"
ID_TXT_PATH          = "txt_mediapool_path"
ID_BTN_GO            = "btn_go"
ID_BTN_SET_CURRENT   = "btn_set_current"
ID_BTN_SAVE_BOOKMARK = "btn_save_bookmark"
ID_TREE_BOOKMARKS    = "tree_subfolders"

SIDEBAR_SIZE    = [47, 16] # Yes I love arbitrary numbers that aren't based on anything reasonable such as font metrics
TOOLBUTTON_SIZE = [40, 20] # and do not hate doing it this way at all thanks for noticing and asking haha
SEPARATOR_SIZE  = [2, 8]

COMMON_SEPARATOR_PROPERTIES = {
	"Weight": 0,
	"FrameStyle": 4,
	"MinimumSize": SEPARATOR_SIZE,
}

class MPNMainWindow(MPNAbstractWidget):
	"""Main Media Pool Navigator widget"""

	def __init__(self, ui_manager):

		super().__init__(ui_manager)

		font_about = self._ui.Font({"PointSize": 10})

		self._lbl_master = self._ui.Label({
			"Weight": 0,
			"Text": "Master /",
		})

		self._txt_media_pool_path = self._ui.LineEdit({
			"ID": ID_TXT_PATH,
			"PlaceholderText": "Start typing a Media Pool path here",
			"Events": {
				"TextEdited": True,
				"EditingFinished": True,
				"ReturnPressed": True,
			},
		})

		self._cmb_media_pool_path = self._ui.ComboBox({
			"ID": ID_CMB_PATH,
			"Editable": True,
			"LineEdit": self._txt_media_pool_path # AHAHAHAHAHA IT WORKED AHAHAHAHAA AAAAAAHAHAHHAAAAA
		})

		self._btn_set_current = self._ui.Button({
			"ID": ID_BTN_SET_CURRENT,
			"Weight": 0,
			"Text": "◉",
			"ToolTip": "Use Current Folder",
			"FixedSize": TOOLBUTTON_SIZE,
			"Events": {"Clicked": True},
		})

		self._btn_save_bookmark = self._ui.Button({
			"ID": ID_BTN_SAVE_BOOKMARK,
			"Weight": 0,
			"FixedSize": TOOLBUTTON_SIZE,
			"Text": "★",
			"ToolTip": "Save To Bookmarks<br/>Option + Click: Toggle Bookmark Visiblity",
			"Events": {"Clicked": True},
		})

		self._tree_bookmarks = self._ui.Tree({
			"ID": ID_TREE_BOOKMARKS,
			"Weight": 1,
			"AlternatingRowColors":True,
			"RootIsDecorated": False,
			"HeaderHidden":True,
			"UniformRowHeights":True,
			"Events": {
				"ItemActivated": True,
				"ItemClicked": True,
			}
		})

		self._lbl_written_by = self._ui.Label({
			"Weight": 0,
			"Text"  : "Written by Michael Jordan",
			"Font"  : font_about,
			"Alignment": {
				"AlignLight":True,
				"AlignBottom": True,
			},
		})

		self._lbl_info = self._ui.Label({
			"Weight": 1,
			"Font"  : font_about,
			"Alignment": {
				"AlignRight":True,
				"AlignBottom": True,
			},
			"OpenExternalLinks": True,
		})

		self._btn_up = self._ui.Button({
			"Weight": 0,
			"FixedSize": SIDEBAR_SIZE,
			"Enabled": False,
			"ID": "btn_sort_up",
			"Text": "⬆",
			"ToolTip": "Move Bookmark Up",
		})

		self._btn_down = self._ui.Button({
			"Weight": 0,
			"FixedSize": SIDEBAR_SIZE,
			"Enabled": False,
			"ID": "btn_sort_down",
			"Text": "⬇",
			"ToolTip": "Move Bookmark Down",
		})

		self._btn_delete = self._ui.Button({
			"Weight": 0,
			"FixedSize": SIDEBAR_SIZE,
			"Enabled": False,
			"ID": "btn_sort_delete",
			"Text": "✖",
			"ToolTip": "Delete Selected Bookmark",
		})
		self._btn_sort = self._ui.Button({
			"Weight": 0,
			"FixedSize": SIDEBAR_SIZE,
			"Enabled": False,
			"ID": "btn_sort_alpha",
			"Text": "𝐀-𝐙",
			"ToolTip": "Sort Alphabetically",
		})

		self._bookmarks = self._ui.VGroup({
			"ID": "lay_bookmarks",
		}, [
			
			self._ui.Label(COMMON_SEPARATOR_PROPERTIES),

			self._ui.HGroup({},[
				self._ui.VGroup({
					},[
						self._btn_up,
						self._btn_down,
						self._btn_sort,
						self._ui.VGap(),
						self._btn_delete,
					]),

				self._tree_bookmarks,
			]),
		])


	def layout(self):
		return self._ui.VGroup({}, [
			
			self._ui.HGroup({
					"Weight": 0,
				},[
					self._lbl_master,
					self._cmb_media_pool_path,
					self._btn_set_current,
					self._btn_save_bookmark,
				]
			),

			self._bookmarks,

			self._ui.Label(COMMON_SEPARATOR_PROPERTIES),
			
			self._ui.HGroup({
				"Weight": 0,
			},[
				self._lbl_written_by,
				self._lbl_info,
			])
		])

	def media_pool_path_editor(self) -> object:
		"""The media pool path `LineEdit`"""

		return self._cmb_media_pool_path.LineEdit

	def media_pool_path_combo(self) -> object:
		"""The media pool `ComboBox`"""

		return self._cmb_media_pool_path

	def bookmark_list_view(self) -> object:
		"""The subfolder `Tree` view"""

		return self._tree_bookmarks

	def button_use_current(self) -> object:
		"""The "Use Current" `Button`"""

		return self._btn_set_current

	def button_add_bookmark(self) -> object:
		"""The `Add To Bookmarks` Button"""

		return self._btn_save_bookmark

	def info_label(self) -> object:
		"""The software info label"""

		return self._lbl_info

	def bookmarks_layout(self) -> object:
		"""Bookmarks layout with buttons and tree"""

		return self._bookmarks

	def bookmarks_move_up_button(self) -> object:
		"""Move Bookmark Up Button"""

		return self._btn_up

	def bookmarks_move_down_button(self) -> object:
		"""Move Bookmark Down Button"""

		return self._btn_down

	def bookmarks_delete_button(self) -> object:
		"""Delete Bookmark Button"""

		return self._btn_delete

	def bookmarks_sort_button(self) -> object:
		"""Delete Bookmark Button"""

		return self._btn_sort

	def bookmark_buttons(self) -> tuple[object]:
		"""Convenience method: All bookmark buttons"""

		return (
			self._btn_up,
			self._btn_down,
			self._btn_sort,
			self._btn_delete,
		)