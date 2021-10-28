from django.urls import path
from . import views

urlpatterns = [
    # create Item role - vendor
    path('create_item', views.CreateItem.as_view()),
    # create comment both role
    path('create_comment', views.CreateComment.as_view()),
    # get list both role
    path('list_item', views.ListItem.as_view()),
    # get list both role
    path('list_comment', views.ListComment.as_view()),
    # buy item buyer role
    # After buyer buy item use this api, it'll send noti to vendor (role - buyer )
    path('buy_item', views.BuyItemView.as_view()),
    # Noti List
    path('bought_item_noti_vendor', views.BoughtItemListToVendorNoti.as_view()),
    path('buyer_noti', views.BuyerNoti.as_view()),
    path('read_item_noti_vendor', views.ReadVendorNoti.as_view()),
    path('read_item_noti_buyer', views.ReadBuyerNoti.as_view()),
    # after got noti from buyer, reply to buyer (role - vendor)
    path('create_noti_for_buyer', views.CreateResponseNotiToBuyer.as_view())
]
