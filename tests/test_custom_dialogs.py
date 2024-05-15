# pyright: reportGeneralTypeIssues=false, reportAttributeAccessIssue=false
from ipymediator.dialogs import FileDialog

##############################################
# poetry run pytest --cov=ipymediator tests/ #
##############################################


def test_file_dialog():
    """"""
    dialog_one = FileDialog(dialog_name=None, filter_pattern=None)
    # dialog_name is None
    assert dialog_one.dialog_name == f"{type(dialog_one).__name__}"
    # test traits are present
    assert dialog_one.has_trait("dialog_open")
    assert dialog_one.has_trait("dialog_selection")
    # filter_pattern is None
    assert dialog_one.file_option["layout"].visibility == "hidden"
    assert dialog_one.file_option["disabled"] is True
    assert dialog_one.file_option["options"] == (("", "*"),)

    # dialog_two = FileDialog(
    #     dialog_name="TestDialog", filter_pattern=(("", "*.py"),))

    # TODO:
    # print(dialog_two.file_option["options"])
    # print(dialog_two.file_option["label"])
    # print(dialog_two.directory["options"])

    # assert dialog_two.file_option["options"] is False
