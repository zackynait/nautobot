from django.db import models

from nautobot.apps.constants import CHARFIELD_MAX_LENGTH
from nautobot.apps.models import extras_features, OrganizationalModel


@extras_features(
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "webhooks",
)
class ExampleModel(OrganizationalModel):
    STORAGE_TYPE_CHOICES = [
        ("ssd", "SSD"),
        ("hdd", "HDD"),
        ("nvme", "NVMe"),
        ("san", "SAN"),
        ("nas", "NAS"),
    ]
    
    CLUSTER_TYPE_CHOICES = [
        ("vsan", "vSAN"),
        ("ceph", "Ceph"),
        ("gluster", "Gluster"),
        ("nfs", "NFS"),
    ]
    
    DISK_TYPE_CHOICES = [
        ("sas", "SAS"),
        ("sata", "SATA"),
        ("nvme", "NVMe"),
        ("ssd", "SSD"),
    ]

    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH, help_text="The name of this Storage.", unique=True)
    number = models.IntegerField(default=100, help_text="The number of this Storage.")
    size_gb = models.IntegerField(help_text="Size in GB", default=0)
    storage_type = models.CharField(
        max_length=50,
        choices=STORAGE_TYPE_CHOICES,
        default="ssd",
        help_text="Type of storage"
    )
    cluster_type = models.CharField(
        max_length=50,
        choices=CLUSTER_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text="Cluster type"
    )
    disk_type = models.CharField(
        max_length=50,
        choices=DISK_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text="Disk type"
    )
    nodes = models.IntegerField(help_text="Number of nodes", default=1, blank=True, null=True)
    rpm = models.IntegerField(help_text="RPM", default=7200, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Storage Model"
        verbose_name_plural = "Storage Models"

    def __str__(self):
        return f"{self.name} - {self.storage_type} ({self.size_gb}GB)"

    def get_absolute_url(self, api=False):
        if api:
            return None
        return f"/plugins/example-app/models/{self.pk}/"


@extras_features(
    "custom_validators",
    "export_templates",
    # "graphql", Not specified here as we have a custom type for this model, see example_app.graphql.types
    "webhooks",
    "relationships",  # Defined here to ensure no clobbering: https://github.com/nautobot/nautobot/issues/3592
)
class AnotherExampleModel(OrganizationalModel):
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH, unique=True)
    number = models.IntegerField(default=100)

    # by default the natural key would just be "name" since it's a unique field. But we can override it:
    natural_key_field_names = ["name", "number"]

    class Meta:
        ordering = ["name"]
