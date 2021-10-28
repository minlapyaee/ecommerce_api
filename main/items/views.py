from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import Item, Comment, BuyItem, ResponseNotiToBuyer
from .serializers import CommentSerializer, CreateItemSerilizer, ItemSerializer, BoughtItemSerializer, BuyerNotiSerializer
import jwt

# Create your views here.


def checkToken(token):
    if not token:
        return False

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return False

    return payload['id']


class ListItem(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class CreateItem(APIView):
    serializer_class = CreateItemSerilizer

    def post(self, request):
        token = request.data['token']
        userId = checkToken(token)

        if userId == False:
            return Response({
                'message': 'unauthorized'
            })
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            title = serializer.data.get('title')
            description = serializer.data.get('description')
            item_code = serializer.data.get('item_code')
            image = serializer.data.get('image')

            item = Item(title=title, description=description,
                        item_code=item_code, image=image, user_id=userId)

            item.save()

            return Response(ItemSerializer(item).data, status=status.HTTP_201_CREATED)


class ListComment(generics.ListAPIView):

    def get(self, request):
        item_id = self.request.query_params.get('item_id')

        queryset = Comment.objects.filter(
            item_id=item_id).order_by('created_at').reverse()

        serializer_class = CommentSerializer(queryset, many=True)
        return Response(serializer_class.data)


class CreateComment(APIView):

    def post(self, request):
        token = request.data['token']
        userId = checkToken(token)

        if userId == False:
            return Response({
                'message': 'unauthorized'
            })

        content = request.data['content']
        item_id = request.data['item_id']

        comment = Comment(content=content, item_id=item_id, user_id=userId)

        comment.save()
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class BuyItemView(APIView):

    def post(self, request):
        token = request.data['token']
        userId = checkToken(token)
        if userId == False:
            return Response({
                'message': 'unauthorized'
            })

        item_code = request.data['item_code']
        buyer_id = userId
        address = request.data['address']
        ph_no = request.data['ph_no']
        item_id = request.data['item_id']
        vendor_id = request.data['vendor_id']
        buyer_name = request.data['buyer_name']
        print(buyer_id, item_code, address, ph_no, item_id)
        boughtItem = BuyItem(
            buyer_id=buyer_id, item_code=item_code, item_id=item_id, address=address, ph_no=ph_no, vendor_id=vendor_id, buyer_name=buyer_name)
        boughtItem.save()
        return Response(BoughtItemSerializer(boughtItem).data, status=status.HTTP_201_CREATED)


class BoughtItemListToVendorNoti(APIView):
    def get(self, request):

        token = request.headers.get('Token')
        userId = checkToken(token)
        if userId == False:
            return Response({
                'message': 'unauthorized'
            })
        queryset = BuyItem.objects.select_related().filter(
            vendor_id=userId).reverse()

        serializer_class = BoughtItemSerializer(queryset, many=True)
        return Response(serializer_class.data)


class ReadVendorNoti(APIView):
    def post(self, request):
        token = request.data['token']
        userId = checkToken(token)
        if userId == False:
            return Response({
                'message': 'unauthorized'
            })
        read_noti = BuyItem.objects.filter(
            vendor_id=userId, read=False).update(read=True)
        return Response({
            'message': 'success'
        })


class CreateResponseNotiToBuyer(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        userId = checkToken(token)
        if userId == False:
            return Response({
                'message': 'unauthorized'
            })
        vendor_name = request.data['vendor_name']
        item_id = request.data['item_id']
        buyer_id = request.data['buyer_id']
        status = request.data['status']
        description = request.data['description']
        item_code = request.data['item_code']
        vendor_id = userId

        resNoti = ResponseNotiToBuyer(vendor_name=vendor_name, buyer_id=buyer_id,
                                      status=status, description=description, vendor_id=vendor_id, item_id=item_id, item_code=item_code)
        resNoti.save()

        return Response({
            'message': 'success'
        })


class BuyerNoti(APIView):
    def get(self, request):

        token = request.headers.get('Token')
        userId = checkToken(token)

        print(userId)
        if userId == False:
            return Response({
                'message': 'unauthorized'
            })
        queryset = ResponseNotiToBuyer.objects.filter(
            buyer_id=userId).reverse()

        serializer_class = BuyerNotiSerializer(queryset, many=True)
        return Response(serializer_class.data)


class ReadBuyerNoti(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        userId = checkToken(token)
        if userId == False:
            return Response({
                'message': 'unauthorized'
            })
        read_noti = ResponseNotiToBuyer.objects.filter(
            buyer_id=userId, read=False).update(read=True)
        return Response({
            'message': 'success'
        })
