import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import Template, TemplateDoesNotExist
from django.template.context import RequestContext
from django_tables2 import RequestConfig

from nautobot.circuits.models import Circuit
from nautobot.core.ui.breadcrumbs import (
    Breadcrumbs,
    InstanceParentBreadcrumbItem,
    ModelBreadcrumbItem,
)
from nautobot.core.ui.choices import SectionChoices
from nautobot.core.ui.object_detail import ObjectDetailContent, ObjectFieldsPanel, ObjectsTablePanel, StatsPanel
from nautobot.core.views.paginator import EnhancedPaginator, get_paginate_count
from nautobot.core.views.viewsets import NautobotUIViewSet
from nautobot.dcim.models import Controller, ControllerManagedDeviceGroup, Device, Location, Rack, RackReservation
from nautobot.extras.models import DynamicGroup
from nautobot.ipam.models import IPAddress, Namespace, Prefix, VLAN, VRF
from nautobot.tenancy.api import serializers
from nautobot.virtualization.models import Cluster, VirtualMachine

from . import filters, forms, tables
from .models import Tenant, TenantGroup

#
# Tenant groups
#


class TenantGroupUIViewSet(NautobotUIViewSet):
    bulk_update_form_class = forms.TenantGroupBulkEditForm
    filterset_class = filters.TenantGroupFilterSet
    filterset_form_class = forms.TenantGroupFilterForm
    form_class = forms.TenantGroupForm
    queryset = TenantGroup.objects.all()
    serializer_class = serializers.TenantGroupSerializer
    table_class = tables.TenantGroupTable
    object_detail_content = ObjectDetailContent(
        panels=(
            ObjectFieldsPanel(
                section=SectionChoices.LEFT_HALF,
                weight=100,
                fields="__all__",
            ),
            ObjectsTablePanel(
                weight=100,
                section=SectionChoices.RIGHT_HALF,
                exclude_columns=["tenant_group"],
                context_table_key="tenant_table",
                related_field_name="tenant_group",
            ),
        )
    )

    def get_extra_context(self, request, instance):
        # Tenants
        context = super().get_extra_context(request, instance)
        if self.action == "retrieve":
            # ObjectsTablePanel usually handles the generation of this table, this is an exception here
            # Because we are filtering on its tenant_group as well as the tenant group's descendants
            # i.e. `instance.descendants(include_self=True)`
            tenants = Tenant.objects.restrict(request.user, "view").filter(
                tenant_group__in=instance.cacheable_descendants_pks(include_self=True)
            )

            tenant_table = tables.TenantTable(tenants, configurable=True)
            tenant_table.columns.hide("tenant_group")

            paginate = {
                "paginator_class": EnhancedPaginator,
                "per_page": get_paginate_count(request),
            }
            RequestConfig(request, paginate).configure(tenant_table)
            context["tenant_table"] = tenant_table
        return context


#
#  Tenants
#


class TenantUIViewSet(NautobotUIViewSet):
    bulk_update_form_class = forms.TenantBulkEditForm
    filterset_class = filters.TenantFilterSet
    filterset_form_class = forms.TenantFilterForm
    form_class = forms.TenantForm
    queryset = Tenant.objects.all()
    serializer_class = serializers.TenantSerializer
    table_class = tables.TenantTable
    object_detail_content = ObjectDetailContent(
        panels=(
            ObjectFieldsPanel(
                section=SectionChoices.LEFT_HALF,
                weight=100,
                fields="__all__",
            ),
            StatsPanel(
                label="Stats",
                filter_name="tenant",
                related_models=[
                    Circuit,
                    Cluster,
                    Controller,
                    ControllerManagedDeviceGroup,
                    Device,
                    DynamicGroup,
                    IPAddress,
                    # TODO: Should we include child locations of the filtered locations in the location_count below?
                    Location,
                    Namespace,
                    Prefix,
                    Rack,
                    RackReservation,
                    VirtualMachine,
                    VLAN,
                    VRF,
                ],
                section=SectionChoices.RIGHT_HALF,
                weight=100,
            ),
        )
    )
    breadcrumbs = Breadcrumbs(
        items={
            "detail": [
                ModelBreadcrumbItem(),
                InstanceParentBreadcrumbItem(parent_key="tenant_group", parent_lookup_key="name"),
            ]
        }
    )


#
# Tenant Dashboard
#


from django.views.generic import TemplateView
from nautobot.core.apps import registry


class TenantDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "tenancy/tenant_dashboard.html"

    def render_additional_content(self, request, context, details):
        # Collect all custom data using callback functions.
        for key, data in details.get("custom_data", {}).items():
            if callable(data):
                context[key] = data(request)
            else:
                context[key] = data

        # Create standalone template
        path = f"{details['template_path']}{details['custom_template']}"
        if os.path.isfile(path):
            with open(path, "r") as f:
                html = f.read()
        else:
            raise TemplateDoesNotExist(path)

        template = Template(html)

        additional_context = RequestContext(request, context)
        return template.render(additional_context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant_id = self.request.GET.get("tenant")
        selected_tenant = None
        tenant_filter = {}

        if tenant_id:
            try:
                selected_tenant = Tenant.objects.get(id=tenant_id)
                tenant_filter = {"tenant": selected_tenant}
            except (Tenant.DoesNotExist, ValueError):
                try:
                    selected_tenant = Tenant.objects.get(name=tenant_id)
                    tenant_filter = {"tenant": selected_tenant}
                except Tenant.DoesNotExist:
                    pass

        context["selected_tenant"] = selected_tenant
        context["tenants"] = Tenant.objects.all()

        # DEBUG: Print registry structure to understand panel/item names
        import pprint
        print("DEBUG: Registry homepage_layout structure:")
        print(f"Keys: {registry['homepage_layout'].keys()}")
        print(f"Panels keys: {registry['homepage_layout']['panels'].keys()}")
        for panel_key, panel_details in registry['homepage_layout']['panels'].items():
            print(f"\nPanel key: {panel_key}")
            print(f"Panel details keys: {panel_details.keys()}")
            if 'items' in panel_details:
                print(f"Panel items keys: {panel_details['items'].keys()}")
                for item_key, item_details in panel_details['items'].items():
                    print(f"  Item key: {item_key}")
                    print(f"  Item details keys: {item_details.keys()}")
                    # Print first item details for debugging
                    break
                break

        # Get homepage layout and filter counts - use the same structure as HomeView
        for panel_details in registry["homepage_layout"]["panels"].values():
            if panel_details.get("custom_template"):
                panel_details["rendered_html"] = self.render_additional_content(self.request, context, panel_details)

            else:
                for item_details in panel_details["items"].values():
                    if item_details.get("custom_template"):
                        item_details["rendered_html"] = self.render_additional_content(self.request, context, item_details)

                    elif item_details.get("model"):
                        # If there is a model attached collect object count.
                        queryset = item_details["model"].objects.restrict(self.request.user, "view")
                        # Apply tenant filter if model has tenant field and tenant is selected
                        if tenant_filter and hasattr(item_details["model"], "tenant"):
                            queryset = queryset.filter(**tenant_filter)
                        item_details["count"] = queryset.count()

                    elif item_details.get("items"):
                        # Collect count for grouped objects.
                        for group_item_details in item_details["items"].values():
                            if group_item_details.get("custom_template"):
                                group_item_details["rendered_html"] = self.render_additional_content(
                                    self.request, context, group_item_details
                                )
                            elif group_item_details.get("model"):
                                queryset = group_item_details["model"].objects.restrict(self.request.user, "view")
                                # Apply tenant filter if model has tenant field and tenant is selected
                                if tenant_filter and hasattr(group_item_details["model"], "tenant"):
                                    queryset = queryset.filter(**tenant_filter)
                                group_item_details["count"] = queryset.count()

        context["homepage_layout"] = registry["homepage_layout"]
        return context
