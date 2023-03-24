from django.shortcuts import render,redirect
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from .serializers import ProductSerializer,CatagorySerializers,FavouriteSerializer,CartSerializer,UserSerializer
from dukan.models import Product,Cart,Catagory,Favourite
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.
@api_view(['GET'])
def geturls(request):
    urls=[
        {'GET':'api/'},
        {'GET':'api/home/'},

        {'POST':'api/users/token'},
        {'POST':'api/user/token/refresh'},
        {'POST':'api/api_login'},
        {'POST':'api/api_logout'},
        {'POST':'api/api_signup'},
        {'GET':'api/api_user/'},

        {'DELETE':'/api/remove_cart/<str:cid>'},
        {'GET':'/api/cart'},
        {'POST':'/api/addcart'},

        {'POST': '/api/addfav',},
        {'GET': '/api/favviewpage'},
        {'DELETE':'/api/remove_fav/<str:fid>'},
        
        {'GET':'/api/collections'},
        {'GET':'/api/collections/<str:name>'},
        {'GET':'/api/collections/<str:cname>/<str:pname>'},
        
    ]

    return Response(urls)



class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"success": "Logged out successfully"})

@api_view(['POST'])
@csrf_exempt
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # token= AuthToken.objects.create(user)[1]
        return Response("Login Successful")
    else:
        return Response({"error": "Invalid credentials"})

@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def user_detail_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
def     api_home(request):
    products = Product.objects.all()
    lst=[]
    for product in products:
        serializer=ProductSerializer(product)
        lst.append(serializer.data)
    return Response({"All Products":lst})
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_favviewpage(request):
    # if request.user.is_authenticated:
        favs = Favourite.objects.filter(user=request.user)
        fav_list=[]
        for fav in favs:
            serializers=FavouriteSerializer(fav)
            fav_list.append(serializers.data)
        return Response(fav_list)
    # else:
    #     return Response({"message": "User not authenticated."})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_remove_fav(request, fid):
    item = get_object_or_404(Favourite, id=fid)
    item.delete()
    return Response({"message": "Favorite item removed."})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_cart_page(request):
    
        carts = Cart.objects.filter(user=request.user)
        
        cart_list=[]
        for cart in carts: 
            serializer=CartSerializer(cart)
            cart_list.append(serializer.data)
        return Response(cart_list)
    
     



@api_view(['DELETE'])
def api_remove_cart(request, cid):
    cartitem = get_object_or_404(Cart, id=cid)
    cartitem.delete()
    return Response({"message": "Cart item removed."})



@api_view(['POST'])
def api_fav_page(request):
    if request.user.is_authenticated:
        product_id = request.data.get('pid')
        product_status = Product.objects.filter(id=product_id).exists()
        if product_status:
            if Favourite.objects.filter(user=request.user.id, product_id=product_id).exists():
                return Response({"message": "Product already in favorite."})
            else:
                Favourite.objects.create(user=request.user, product_id=product_id)
                return Response({"message": "Product added to favorite."})
        else:
            return Response({"message": "Product does not exist."})
    else:
        return Response({"message": "User not authenticated."})



@api_view(['POST'])
def api_add_to_cart(request):
    if request.user.is_authenticated:
        product_qty = request.data.get('product_qty')
        product_id = request.data.get('pid')
        product_status = Product.objects.filter(id=product_id).exists()
        if product_status:
            if Cart.objects.filter(user=request.user.id, product_id=product_id).exists():
                return Response({"message": "Product already in cart."})
            else:
                if Product.objects.get(id=product_id).quantity >= product_qty:
                    Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                    return Response({"message": "Product added to cart."})
                else:
                    return Response({"message": "Product stock not available."})
        else:
            return Response({"message": "Product does not exist."})
    else:
        return Response({"message": "User not authenticated."})



@api_view(['GET'])
def collection(request):
    collections=Catagory.objects.all()
    serializer=CatagorySerializers(collections,many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collectionsview(request,name):
  if(Catagory.objects.filter(name=name,status=0)):
      products=Product.objects.filter(category__name=name)
      product_list=[]
      for product in products:
          serializer=ProductSerializer(product)
          product_list.append(serializer.data)
      return Response(product_list)
  else:
    return Response("category not found ")

def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        product_list=[]
        for product in products:
            serializer=ProductSerializer(product)
            product_list.append(serializer.data)
        return Response(product_list)
      else:
        return Response("Product not Found")
        
    else:
      return Response("category not found")