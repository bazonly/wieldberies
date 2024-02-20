from rest_framework import serializers
from rest_framework import validators

from api.models import ApiUser, Warehouse, Product, Transaction


class UserSerializer(serializers.Serializer):
    USER_TYPES = (
        ('Поставщик', 'Поставщик'),
        ('Потребитель', 'Потребитель'),
    )
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=128, validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    email = serializers.EmailField(validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    password = serializers.CharField(min_length=6, max_length=20, write_only=True)
    user_type = serializers.ChoiceField(choices=USER_TYPES)

    def update(self, instance, validated_data):
        if email := validated_data.get("email"):
            instance.email = email
            instance.save(update_fields=["email"])

        if user_type := validated_data.get("user_type"):
            instance.user_type = user_type
            instance.save(update_fields=["user_type"])

        if password := validated_data.get("password"):
            instance.set_password(password)
            instance.save(update_fields=["password"])
        return instance

    def create(self, validated_data):
        user = ApiUser.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            user_type=validated_data["user_type"]
        )
        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])
        return user


class WarehouseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128, validators=[
        validators.UniqueValidator(Warehouse.objects.all())
    ])

    def update(self, instance, validated_data):
        if name := validated_data.get("name"):
            instance.name = name
            instance.save(update_fields=["name"])
        return instance

    def create(self, validated_data):
        warehouse = Warehouse.objects.create(
            name=validated_data["name"],
        )
        return warehouse

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'