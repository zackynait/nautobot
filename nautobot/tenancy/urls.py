from django.urls import path
from nautobot.core.views.routers import NautobotUIViewSetRouter

from . import views

app_name = "tenancy"
router = NautobotUIViewSetRouter()
router.register("tenant-groups", views.TenantGroupUIViewSet)
router.register("tenants", views.TenantUIViewSet)

urlpatterns = router.urls
urlpatterns += [
    path("dashboard/", views.TenantDashboardView.as_view(), name="tenant_dashboard"),
]
