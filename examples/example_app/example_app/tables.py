import django_tables2 as tables

from nautobot.apps.tables import (
    BaseTable,
    ButtonsColumn,
    ToggleColumn,
)

from example_app.models import AnotherStorageModel, StorageModel


class StorageModelTable(BaseTable):
    """Table for list view of `StorageModel` objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    actions = ButtonsColumn(StorageModel)

    class Meta(BaseTable.Meta):
        model = StorageModel
        fields = ["pk", "name", "number"]


class AnotherStorageModelTable(BaseTable):
    """Table for list view of `AnotherStorageModel` objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    actions = ButtonsColumn(AnotherStorageModel)

    class Meta(BaseTable.Meta):
        model = AnotherStorageModel
        fields = ["pk", "name", "number"]
