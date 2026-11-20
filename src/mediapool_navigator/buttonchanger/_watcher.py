import enum

class MPNButtonStates(enum.Enum):

	NORMAL = enum.auto()
	ALT    = enum.auto()
	SHIFT  = enum.auto()
	CTRL   = enum.auto()

class MPNButtonChanger:
	"""A thing that changes button labels on key press"""

	def __init__(self):

		self._buttons:list[object] = []  # Buttons aren't hashable
		self._states :list[dict[MPNButtonStates,str]] = []

	def register_button(self, button:object, state:MPNButtonStates, text:str):

		if button not in self._buttons:
		
			self._buttons.append(button)
			self._states.append({
				"normal": button.Text,
				state:    text,
			})

		else:
			self._states[self._buttons.index(button)][state] = text

	def set_state(self, state:MPNButtonStates):

		for idx, button in enumerate(self._buttons):

			button.Text = self._states[idx].get(state, self._states[idx]["normal"])