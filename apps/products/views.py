from django_filters.rest_framework import DjangoFilterBackend
from products.models import (
    Branches,
    Cart,
    CartItem,
    Category,
    Highlight,
    Order,
    OrderItem,
    Product,
)
from products.serializers import (
    BranchesModelSerializer,
    CartItemModelSerializer,
    CartModelSerializer,
    CategoryModelSerializer,
    HighlightModelSerializer,
    OrderItemModelSerializer,
    ProductDetailModelSerializer,
    ProductModelSerializer,
)
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from shared.paginations import CustomPageNumberPagination


class BranchesListCreateAPIView(ListCreateAPIView):
    queryset = Branches.objects.all()
    serializer_class = BranchesModelSerializer


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ('price', '-price', 'created_at', '-created_at')
    ordering = ('-created_at',)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializer


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPageNumberPagination


class HighlightListAPIView(ListCreateAPIView):
    queryset = Highlight.objects.filter().order_by('-created_at')
    serializer_class = HighlightModelSerializer


class CartListAPIView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer


class CartRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer


class CartItemListCreateAPIView(ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(cart__user=self.request.user)


class OrderListCreateAPIView(ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(cart__user=self.request.user)


class CartConfirmApiView(APIView):
    queryset = Cart.objects.all()
    serializer_class = CartItemModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

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
        order.save()
        return Response({"message": "Order created successfully"}, status.HTTP_201_CREATED)
