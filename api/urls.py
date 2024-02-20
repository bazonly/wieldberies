from rest_framework.routers import DefaultRouter

from api.views import UserModelViewSet, WarehouseModelViewSet, ProductModelViewSet, TransactionModelViewSet

router = DefaultRouter()
router.register('users', UserModelViewSet)
router.register('warehouse', WarehouseModelViewSet)
router.register('product', ProductModelViewSet)
router.register('transaction', TransactionModelViewSet)


urlpatterns = [

]

urlpatterns.extend(router.urls)