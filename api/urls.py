from django.urls import path
from . import views
from .views import CreateUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns=[
    path('',views.geturls,name='urls'),
    path('home/',views.api_home,name='home_api'),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api_signup/', CreateUserView.as_view(), name="api_signup"),
    path('api_login/', views.login_view, name="api_login"),
    path('api_logout/', views.logout_view, name="api_logout"),
    path('api_user/', views.user_detail_view, name="api_user_detail"),
    


    path('addfav/',views.api_fav_page,name='addfev_api'),
    path('favviewpage/',views.api_favviewpage,name='favviewpage_api'),
    path('removefav/<str:fid>',views.api_remove_fav,name='removefav_api'),


    path('addcart/',views.api_add_to_cart,name='addcart_api'),
    path('cart/',views.api_cart_page,name='cart_api'),
    path('removecart/<str:cid>/',views.api_remove_cart,name='removecart_api'),
    
     
    path('collections/',views.collection,name='collections_api'),
    path('collections/<str:name>/',views.collectionsview,name='item_api'),
    path('collections/<str:cname>/<str:pname>',views.product_details,name='api_product_details')
]