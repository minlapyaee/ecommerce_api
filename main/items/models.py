from django.db import models
from django.conf import settings


# Create your models here.


class Item(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    item_code = models.CharField(max_length=8)
    image = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='item_user_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comment_user_id'
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='comment_item_id')
    created_at = models.DateTimeField(auto_now_add=True)


class BuyItem(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="buyer_id"
    )
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vendor_id"
    )
    buyer_name = models.CharField(max_length=250)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='buy_item_id')

    item_code = models.CharField(max_length=8)
    address = models.CharField(max_length=100)
    ph_no = models.CharField(max_length=20)
    status = models.CharField(max_length=20, null=False, default="pending")
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ResponseNotiToBuyer(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="response_buyer_id"
    )
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="response_vendor_id"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='response_item_id')

    item_code = models.CharField(max_length=8)
    vendor_name = models.CharField(max_length=250)
    status = models.CharField(max_length=20)
    description = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
