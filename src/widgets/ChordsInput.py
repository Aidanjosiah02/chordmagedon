from textual.app import App, ComposeResult
from textual.widgets import Input
from textual.validation import Regex
from textual.binding import Binding
from src.constants import CHORD_REGEX


class ChordsInput(App):
    BINDINGS = [
        Binding("ctrl+q", "custom_quit", "Quit"),
        Binding("ctrl+c", "custom_quit", "Quit"),
    ]

    submitted = False

    def compose(self) -> ComposeResult:
        # This is chord regex without the capture group names
        SINGLE_CHORD_VALIDATOR = (
            r'(?:[A-G](?:s(?!us)|b)?)'
            r'(?:min|no3d|aug|dim|sus2|sus4)?'
            r'(?:(?:maj)?[bs]?(?:7|9|11|13|15|17)(?:[bs](?![0-9]))?)?'
        )

        PROG_PATTERN = fr"^{
            SINGLE_CHORD_VALIDATOR}(?:\s*,\s*{SINGLE_CHORD_VALIDATOR})*$"
        yield Input(
            placeholder="Enter chords (e.g., Cmaj7, Csus2, Db/F)",
            restrict=r"[a-zA-Z0-9,\s/]*",
            validators=[Regex(PROG_PATTERN)],
            id="chord_input"
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.validation_result and event.validation_result.is_valid:
            self.submitted = True
            self.exit(event.value)
        else:
            self.notify("Invalid chord. Check for typos!", severity="error")

    def action_custom_quit(self) -> None:
        if self.submitted:
            self.exit()
        else:
            self.notify("Submit valid chords first.", severity="warning")


if __name__ == "__main__":
    app = ChordsInput()
    result = app.run()
    if result:
        print(f"Final Chords: {result}")
