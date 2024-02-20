from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import ApiUser, Warehouse, Product, Transaction
from api.serializers import UserSerializer, WarehouseSerializer, ProductSerializer, TransactionSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = UserSerializer

    authentication_classes = []
    permission_classes = []


class WarehouseModelViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    def create(self, request, *args, **kwargs):
        if request.user.user_type == 'Поставщик':
            return super().create(request, *args, **kwargs)
        else:
            return Response({'ошибка': 'доступно только для поставщиков'}, status=403)

    def update(self, request, *args, **kwargs):
        if request.user.user_type == 'Поставщик':
            return super().update(request, *args, **kwargs)
        else:
            return Response({'ошибка': 'доступно только для поставщиков'}, status=403)

class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        if request.user.user_type == 'Поставщик':
            return super().create(request, *args, **kwargs)
        else:
            return Response({'ошибка': 'доступно только для поставщиков'}, status=403)


    def update(self, request, *args, **kwargs):
        if request.user.user_type == 'Поставщик':
            return super().update(request, *args, **kwargs)
        else:
            return Response({'ошибка': 'доступно только для поставщиков'}, status=403)


class TransactionModelViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request_data = request.data
        user = request.user
        if user.user_type != 'Потребитель':
            return Response({'ошибка': 'доступно только для потребителя'}, status=403)

        product_id = request_data.get('product')
        quantity = int(request_data.get('quantity'))

        product = Product.objects.get(pk=product_id)
        if product.quantity < quantity:
            return Response({'ошибка': 'На складе нет необходимого количества.'},
                            status=400)

        product.quantity -= quantity
        product.save()

        transaction = Transaction.objects.create(product=product, user=user, quantity=quantity)
        transaction.save()

        return Response({'успех': 'Продукт был взят со склада.'}, status=201)