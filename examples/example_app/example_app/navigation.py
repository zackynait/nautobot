from nautobot.apps.ui import (
    NavigationIconChoices,
    NavigationWeightChoices,
    NavMenuAddButton,
    NavMenuGroup,
    NavMenuItem,
    NavMenuTab,
)

menu_items = (
    NavMenuTab(
        name="Apps",
        icon=NavigationIconChoices.APPS,
        weight=NavigationWeightChoices.APPS,
        groups=(
            NavMenuGroup(
                name="Storage Nautobot App",
                weight=100,
                items=(
                    NavMenuItem(
                        link="plugins:example_app:storagemodel_list",
                        name="Storage Models",
                        permissions=["example_app.view_storagemodel"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:example_app:storagemodel_add",
                                permissions=[
                                    "example_app.add_storagemodel",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:example_app:storagemodel_list",
                        name="Example Models filtered",
                        permissions=["example_app.view_storagemodel"],
                        query_params={"number": "100"},
                    ),
                    NavMenuItem(
                        link="plugins:example_app:anotherstoragemodel_list",
                        name="Another Example Models",
                        permissions=["example_app.view_anotherstoragemodel"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:example_app:anotherstoragemodel_add",
                                permissions=[
                                    "example_app.add_anotherstoragemodel",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
    NavMenuTab(
        name="Storage Menu",
        weight=NavigationWeightChoices.CLOUD + 10,
        groups=(
            NavMenuGroup(
                name="Storage Group 1",
                weight=100,
                items=(
                    NavMenuItem(
                        link="plugins:example_app:storagemodel_list",
                        name="Storage Models",
                        permissions=["example_app.view_storagemodel"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:example_app:storagemodel_add",
                                permissions=[
                                    "example_app.add_storagemodel",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
    NavMenuTab(
        name="Circuits",
        icon=NavigationIconChoices.CIRCUITS,
        weight=NavigationWeightChoices.CIRCUITS,
        groups=(
            NavMenuGroup(
                name="Example Circuit Group",
                weight=150,
                items=(
                    NavMenuItem(
                        link="plugins:example_app:storagemodel_list",
                        name="Storage Models",
                        permissions=["example_app.view_storagemodel"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:example_app:storagemodel_add",
                                permissions=[
                                    "example_app.add_storagemodel",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
)
