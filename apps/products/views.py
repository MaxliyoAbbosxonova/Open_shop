from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import (
    Branches,
    Cart,
    CartItem,
    Category,
    Highlight,
    Order,
    OrderItem,
    Product, Region, District,
)
from products.serializers import (
    BranchesModelSerializer,
    CartItemModelSerializer,
    CartModelSerializer,
    CategoryModelSerializer,
    HighlightModelSerializer,
    ProductDetailModelSerializer,
    ProductModelSerializer, RegionModelSerializer, DistrictModelSerializer,
)
from shared.paginations import CustomPageNumberPagination
from shared.permissions import UserPermission


@extend_schema(tags=['Branches'])
class BranchesListCreateAPIView(ListCreateAPIView):
    authentication_classes = ()
    queryset = Branches.objects.all()
    serializer_class = BranchesModelSerializer
    permission_classes = [UserPermission]
    ordering_fields = ["created_at"]


# @extend_schema(tags=['Products'])
# class ProductListAPIView(ListCreateAPIView):
#     queryset = Product.objects.order_by('-created_at')
#     serializer_class = ProductModelSerializer
#     pagination_class = CustomPageNumberPagination
#     permission_classes = (UserPermission,)
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     ordering_fields = 'price', 'created_at'
#     ordering = ('-created_at',)


@extend_schema(tags=['Products'])
class ProductListAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
              permission_classes = [AllowAny,]  # Anyone can view
        elif self.request.method == 'POST':
              permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductModelSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request,format=None):
        serializer = ProductModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # queryset = Product.objects.order_by('-created_at')
    # serializer_class = ProductModelSerializer
    # pagination_class = CustomPageNumberPagination
    # permission_classes = (UserPermission,)
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # ordering_fields = 'price', 'created_at'
    # ordering = ('-created_at',)



@extend_schema(tags=['Products'])
class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializer
    permission_classes = (IsAdminUser,)


@extend_schema(tags=['Category'])
class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [UserPermission, ]
    authentication_classes = ()
    pagination_class = CustomPageNumberPagination


@extend_schema(tags=['Highlight'])
class HighlightListAPIView(ListCreateAPIView):
    queryset = Highlight.objects.order_by('-created_at')
    serializer_class = HighlightModelSerializer
    permission_classes = [UserPermission, ]
    authentication_classes = ()


@extend_schema(tags=['Order'])
class CartListAPIView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer
    permission_classes = [UserPermission, ]


@extend_schema(tags=['Order'])
class CartRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer
    permission_classes = [UserPermission, ]


@extend_schema(tags=['Order'])
class CartItemListAPIView(ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemModelSerializer
    permission_classes = [UserPermission, ]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(cart__user=self.request.user)


@extend_schema(tags=['Order'])
class OrderCreateApiView(APIView):
    queryset = Cart.objects.all()
    serializer_class = CartItemModelSerializer
    permission_classes = [UserPermission, ]

    def post(self, request, *args, **kwargs):
        user = request.user
        order = Order.objects.create(user=user, total_amount=0)
        order_items_list = []
        total_amount = 0

        for cart_item in user.cart.items.all():
            _quantity = cart_item.quantity
            _price = cart_item.product.price
            total_amount += _quantity * _price
            order_items_list.append(OrderItem(
                product=cart_item.product,
                quantity=_quantity,
                price=_price,
                order=order,
            ))

        OrderItem.objects.bulk_create(order_items_list)
        order.total_amount = total_amount
        order.save(update_fields=['total_amount'])
        return Response({"message": "Order created successfully"}, status.HTTP_201_CREATED)


class RegionListCreateAPIView(ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionModelSerializer

class DistrictListCreateAPIView(ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictModelSerializer
