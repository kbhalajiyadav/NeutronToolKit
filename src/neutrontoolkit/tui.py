"""Terminal UI: Space select, P plot, U unselect, / filter, 1-4 plot styles."""
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header, Input, Static
from .files import discover
from .plots import plot_files

class DataBrowser(App):
    TITLE = "NeutronToolKit — file selection"
    BINDINGS = [
        ("space", "toggle", "Select"),
        ("a", "select_all", "Select visible"),
        ("u", "unselect", "Unselect all"),
        ("p", "plot", "Plot selected"),
        ("slash", "filter", "Filter"),
        ("1", "kind('iq')", "I(Q)"),
        ("2", "kind('kratky')", "Kratky"),
        ("3", "kind('porod')", "Porod"),
        ("4", "kind('guinier')", "Guinier"),
        ("r", "reload", "Reload"),
        ("q", "quit", "Quit"),
    ]
    CSS = """
    #filter { display: none; margin: 0 1; }
    #state { padding: 1; }
    DataTable { height: 1fr; }
    """
    def __init__(self, directory="data/reduced"):
        super().__init__()
        self.directory = Path(directory).expanduser().resolve()
        self.files = []
        self.visible = []
        self.selected = set()
        self.kind = "iq"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("", id="state")
        yield Input(placeholder="Filter by file name, Enter to return", id="filter")
        yield DataTable(id="table", cursor_type="row")
        yield Footer()

    def on_mount(self):
        table = self.query_one("#table", DataTable)
        table.add_columns("✓", "File", "Folder")
        self.action_reload()
        table.focus()

    def refresh_table(self):
        needle = self.query_one("#filter", Input).value.casefold()
        self.visible = [p for p in self.files if needle in str(p.relative_to(self.directory)).casefold()]
        table = self.query_one("#table", DataTable)
        table.clear()
        for p in self.visible:
            table.add_row("✓" if p in self.selected else "",
                          p.name, str(p.parent.relative_to(self.directory)))
        self.query_one("#state", Static).update(
            f"{self.directory} | {len(self.selected)} selected | {len(self.visible)} visible | plot: {self.kind}"
        )

    def action_reload(self):
        try:
            self.files = discover(self.directory)
            self.selected.intersection_update(self.files)
            self.refresh_table()
        except (ValueError, OSError) as exc:
            self.notify(str(exc), severity="error")

    def action_toggle(self):
        row = self.query_one("#table", DataTable).cursor_row
        if 0 <= row < len(self.visible):
            item = self.visible[row]
            if item in self.selected:
                self.selected.remove(item)
            else:
                self.selected.add(item)
            self.refresh_table()

    def action_select_all(self):
        self.selected.update(self.visible)
        self.refresh_table()

    def action_unselect(self):
        self.selected.clear()
        self.refresh_table()

    def action_filter(self):
        field = self.query_one("#filter", Input)
        field.display = True
        field.focus()

    def on_input_changed(self, event: Input.Changed):
        if event.input.id == "filter":
            self.refresh_table()

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "filter":
            event.input.display = False
            self.query_one("#table", DataTable).focus()

    def action_kind(self, name):
        self.kind = name
        self.refresh_table()

    def action_plot(self):
        paths = [p for p in self.visible if p in self.selected]
        if not paths:
            self.notify("Use Space to select file(s), then P to plot", severity="warning")
            return
        try:
            target = plot_files(paths, self.kind)
            self.notify(f"Saved {target}; open figure in VS Code or Jupyter", timeout=8)
        except (ValueError, OSError) as exc:
            self.notify(str(exc), severity="error", timeout=8)
