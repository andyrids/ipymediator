from pathlib import Path
from typing import Optional, Union

from ipymediator.enumerations import ButtonColour, Options, Value
from ipymediator.interface import Component, Mediator
from ipymediator.utils.common_functions import (
    deiconify_str,
    directory_contents,
    directory_paths,
    singlenotifydispatch
)
from ipywidgets import widgets as w
from traitlets import Bool, HasTraits, Instance


class MediatorWithTraits(Mediator, HasTraits):
    """Abstract Mediator class for Mediator interface implimentation. Extends
    the Mediator interface by allowing traits from the traitlets library,
    through HasTraits inheritence.
    """
    pass


class FileDialog(MediatorWithTraits):
    """A concrete Mediator, which facilitates communication between
    Components used to select a local file, acting as a file explorer.

    Traits:
        dialog_open (bool): FileDialog open flag

        dialog_selection (Path): Currently selected file path

    Class properties:
       _PATH (Path): pathlib Path object set to root directory
    """

    dialog_open = Bool(default_value=True).tag(sync=True)  # type: ignore
    dialog_selection = Instance(Path, allow_none=True).tag(sync=True)

    _PATH = Path().absolute()

    def __init__(
            self,
            dialog_name: Optional[str] = None,
            filter_pattern:  Optional[tuple[tuple[str, str], ...]] = None):
        """Initialise instance variables and Components.

        Params:
            dialog_name (str): Reference name for this Mediator

            filter_pattern (tuple[tuple]): Optional file glob filter patterns


        """
        super(FileDialog, self).__init__()
        self.dialog_name = dialog_name or f"{type(self).__name__}"

        self.button_min = Component(
            mediator=self, widget=w.Button(), widget_name="ButtonMin")

        self.button_close = Component(
            mediator=self, widget=w.Button(), widget_name="ButtonClose")

        self.button_save = Component(
            mediator=self, widget=w.Button(), widget_name="ButtonSave")

        self.button_select = Component(
            mediator=self, widget=w.ToggleButton(), widget_name="ButtonSelect")

        self.label_selected = Component(mediator=self, widget=w.Label())

        self.file_option = Component(
            mediator=self, widget=w.ToggleButtons(), widget_name="FileOptions")

        self.file_output = Component(
            mediator=self, widget=w.Text(), widget_name="FileOutput")

        self.file_selected = Component(
            mediator=self, widget=w.Text(), widget_name="FileSelected")

        self.directory = Component(
            mediator=self, widget=w.Dropdown(), widget_name="Directory")

        self.directory_files = Component(
            mediator=self, widget=w.Select(), widget_name="DirectoryFiles")

        self.button_close["description"] = "X"
        self.button_close["style"].font_weight = "bold"
        self.button_close["style"].button_color = ButtonColour.RED
        self.button_close["layout"].width = "auto"

        self.button_save["icon"] = "file"
        self.button_save["layout"].width = "auto"
        self.button_save["disabled"] = True
        self.button_select["icon"] = "plus"
        self.button_select["disabled"] = True

        self.label_selected["value"] = "Selection:"
        self.label_selected["layout"].min_width = "60px"

        self.file_option["style"].button_width = "88px"
        self.file_option["layout"].grid_area = "FileOption"

        self.file_output["value"] = "..."
        self.file_output["disabled"] = False
        self.file_output["layout"].grid_area = "FileOutput"
        self.file_output["layout"].width = "auto"

        self.file_selected["value"] = "..."
        self.file_selected["disabled"] = True

        self.directory["layout"].grid_area = "DirectoryPath"
        self.directory["layout"].width = "auto"
        self.directory_files["rows"] = 4
        self.directory_files["layout"].grid_area = "DirectoryContent"
        self.directory_files["layout"].width = "auto"
        self.directory_files["layout"].height = "92px"

        self.container_upper = w.HBox()
        self.container_upper.children = (
            self.file_option.widget, self.button_close.widget)

        self.container_upper.layout = w.Layout(
            display="grid",
            margin="2px 0px",
            grid_gap="0px 0px",
            grid_template_rows="auto",
            grid_template_columns="90% 10%",
            grid_template_areas="""
            "FileOption ButtonClose"
            """)

        self.container_middle = w.GridBox()
        self.container_middle.children = (
            self.directory.widget,
            self.file_output.widget,
            self.button_save.widget,
            self.directory_files.widget)

        self.container_middle.layout = w.Layout(
            width="auto",
            height="auto",
            grid_gap="0px 0px",
            grid_template_rows="auto auto",
            grid_template_columns="50% 40% 10%",
            grid_template_areas="""
            "DirectoryPath    FileOutput        ButtonSave      "
            "DirectoryContent DirectoryContent  DirectoryContent"
            """)

        self.container_lower = w.HBox()
        self.container_lower.children = (
            self.button_select.widget,
            w.HBox(
                (self.label_selected.widget, self.file_selected.widget))
        )

        self.container = w.VBox(children=(
            self.container_upper, self.container_middle, self.container_lower))
        self.container.layout = w.Layout(max_width="430px")

        if filter_pattern is not None:
            self.file_option["options"] = filter_pattern
            if len(filter_pattern) == 1:
                self.file_option["disabled"] = True
                if filter_pattern[0][0] == "":
                    self.file_option["layout"].visibility = "hidden"
        else:
            self.file_option["layout"].visibility = "hidden"
            self.file_option["disabled"] = True
            self.file_option["options"] = (("", "*"),)

    @singlenotifydispatch
    def notify(self, reference: str, change: Union[Value, Options]) -> None:
        """Method for notifying a mediator class of a widget event"""
        pass

    @notify.register("FileOptions")
    def _(self, reference: str, change: Value) -> None:
        """"""
        # file_option -> FileDialog -> button_select
        self.button_select["value"] = False

        # file_option -> FileDialog -> directory
        options = directory_paths(self._PATH, self.file_option["value"])
        if len(options) > 0 and self.directory["options"] == options:
            self.directory["index"] = 0
        else:
            self.directory["options"] = options

    @notify.register("Directory")
    def _(self, reference: str, change: Value) -> None:
        # directory -> FileDialog -> directory_files
        self.directory_files["options"] = directory_contents(
            self.patlib_path(str(change["new"])),
            self.file_option["value"],
            rglob=False)

    @notify.register("DirectoryFiles")
    def _(self, reference: str, change: Options) -> None:
        # directory -> FileDialog -> file_selected
        # directory -> FileDialog -> button_select
        if change["new"] is not None:
            self.button_select["disabled"] = False
        else:
            self.file_selected["value"] = "..."
            self.button_select["disabled"] = True
            self.button_select["value"] = False

    @notify.register("ButtonSelect")
    def _(self, reference: str, change: Value) -> None:
        value_idx = int(change["new"])
        # button_select -> FileDialog -> button_select
        self.button_select["icon"] = ("plus", "minus")[value_idx]

        # button_select -> FileDialog -> file_selected
        file_selected = self.directory_files["value"]
        self.file_selected["value"] = ("...", file_selected)[value_idx]

    @notify.register("ButtonSave")
    def _(self, reference: str, change: Value) -> None:
        # button_save -> FileDialog -> Map
        directory = deiconify_str(self.directory["value"])
        filename = deiconify_str(self.file_selected["value"])
        self.dialog_selection = Path(f"{directory}/{filename}")
        self.button_select["value"] = False

    @notify.register("ButtonClose")
    def _(self, reference: str, change: Value) -> None:
        """"""
        self.dialog_open = False

    @notify.register("FileSelected")
    def _(self, reference: str, change: Value) -> None:
        # file_selected -> FileDialog -> file_x_column & file_y_column
        file_selected = deiconify_str(str(change["new"]))
        if file_selected == "...":
            self.file_output["value"] = "..."
            return

        self.file_output["value"] = file_selected
        self.button_save["disabled"] = False

    def patlib_path(self, path_str: str) -> Path:
        return Path(deiconify_str(path_str))
