from textual.app import App, ComposeResult
from textual.widgets import Header, Select
from textual import on
from src.constants import NOTE_MAP


class CompositionKeySelection(App):

    def compose(self) -> ComposeResult:
        self.title = "Select a Key"
        yield Header()
        yield Select((key, value) for key, value in NOTE_MAP.items())

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        if event.value in NOTE_MAP.values():
            self.exit(result=event.value)
