from rest_framework import serializers
from .models import Item, Comment, BuyItem, ResponseNotiToBuyer
from django.apps import apps

UserModel = apps.get_model('users', 'User')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['id', 'name', 'role', 'item_code']


class ItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Item
        doc_title = serializers.StringRelatedField(many=True)

        fields = ('id', 'title', 'description',
                  'item_code', 'image', 'user_id', 'user')


class CreateItemSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'description', 'item_code', 'image')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        doc_title = serializers.StringRelatedField(many=True)

        fields = "__all__"


class BoughtItemSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=True)

    class Meta:
        model = BuyItem
        doc_title = serializers.StringRelatedField(many=True)
        fields = "__all__"
        # fields = ('buyer_id', 'item_code', 'address',
        #           'status', 'vendor_id', 'created_at')


class BuyerNotiSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=True)

    class Meta:
        model = ResponseNotiToBuyer
        doc_title = serializers.StringRelatedField(many=True)
        fields = "__all__"
