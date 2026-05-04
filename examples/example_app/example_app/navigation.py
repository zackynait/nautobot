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
                        link="plugins:example_app:models",
                        name="Storage Models",
                        permissions=["example_app.view_examplemodel"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:example_app:examplemodel_add",
                                permissions=[
                                    "example_app.add_examplemodel",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="plugins:example_app:models",
                        name="Example Models filtered",
                        permissions=["example_app.view_examplemodel"],
                        query_params={"number": "100"},
                    ),
                    NavMenuItem(
                        link="plugins:example_app:other-models",
                        name="Another Example Models",
                        permissions=["example_app.view_anotherexamplemodel"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:example_app:anotherexamplemodel_add",
                                permissions=[
                                    "example_app.add_anotherexamplemodel",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
    NavMenuTab(
        name="Storage",
        weight=NavigationWeightChoices.CLOUD + 10,
        groups=(
            NavMenuGroup(
                name="Infrastructure",
                weight=100,
                items=(
                    NavMenuItem(
                        link="plugins:example_app:models",
                        name="Cluster",
                        permissions=["example_app.view_examplemodel"],
                    ),
                    NavMenuItem(
                        link="plugins:example_app:models",
                        name="Server Storage",
                        permissions=["example_app.view_examplemodel"],
                    ),
                ),
            ),
            NavMenuGroup(
                name="Storage Hardware",
                weight=200,
                items=(
                    NavMenuItem(
                        link="plugins:example_app:models",
                        name="Dischi",
                        permissions=["example_app.view_examplemodel"],
                    ),
                    NavMenuItem(
                        link="plugins:example_app:models",
                        name="RAID",
                        permissions=["example_app.view_examplemodel"],
                    ),
                    NavMenuItem(
                        link="plugins:example_app:models",
                        name="POOL",
                        permissions=["example_app.view_examplemodel"],
                    ),
                ),
            ),
            NavMenuGroup(
                name="Storage Logical",
                weight=300,
                items=(
                    NavMenuItem(
                        link="plugins:example_app:models",
                        name="Volumi - LUN",
                        permissions=["example_app.view_examplemodel"],
                    ),
                    NavMenuItem(
                        link="plugins:example_app:models",
                        name="Filesystem",
                        permissions=["example_app.view_examplemodel"],
                    ),
                ),
            ),
            NavMenuGroup(
                name="File Sharing",
                weight=400,
                items=(
                    NavMenuItem(
                        link="plugins:example_app:models",
                        name="CIFS / SMB / NFS",
                        permissions=["example_app.view_examplemodel"],
                    ),
                    NavMenuItem(
                        link="plugins:example_app:models",
                        name="FilePath",
                        permissions=["example_app.view_examplemodel"],
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
                        link="plugins:example_app:models",
                        name="Storage Models",
                        permissions=["example_app.view_examplemodel"],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:example_app:examplemodel_add",
                                permissions=[
                                    "example_app.add_examplemodel",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
)
