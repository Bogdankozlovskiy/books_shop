from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, BasePermission
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from myapp.models import Comment
from api.serializers import BookSerializer, DetailBookSerializer, CreateBookSerializer
from myapp.models import Book
from django.db.models import Prefetch, Avg, Sum
from django.contrib.auth.models import User
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from guardian.shortcuts import assign_perm, get_perms, remove_perm, get_objects_for_user
from guardian.utils import get_40x_or_None


# class HasPermission(BasePermission):
#     def has_permission(self, request, view):
#         if request.method == "GET":
#             return request.user.has_perm("myapp.view_book")
#         if request.method == "DELETE":
#             return request.user.has_perm("myapp.delete_book")
#         if request.method == "POST":
#             request.user.has_perm("myapp.add_book")
#         if request.method in ("PUT", "PATCH"):
#             request.user.has_perm("myapp.change_book")

class HasPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return request.user.has_perm("myapp.view_book", obj)
        if request.method == "DELETE":
            return request.user.has_perm("myapp.delete_book", obj)
        if request.method in ("PUT", "PATCH"):
            return request.user.has_perm("myapp.change_book", obj)
        return False


class APIAddLike(APIView):
    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        if request.user in comment.like.all():
            comment.like.remove(request.user)
        else:
            comment.like.add(request.user)
        comment.save()
        return Response({"likes": comment.like.count()})


class MyPageNumberPagination(PageNumberPagination):
    page_size = 3


class APIListBook(ListAPIView):
    # pagination_class = MyPageNumberPagination
    serializer_class = BookSerializer
    # filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    queryset = Book.objects.annotate(
        avg_rate=Avg("rate_book_user_book__rate")
    ).prefetch_related(
        Prefetch("authors", User.objects.only("username"))
    ).select_related("country")
    # ordering_fields = ["id", "title", "price", "country", "avg_rate"]
    # ordering = ['id']
    # search_fields = ["id", "$title", "authors__username", "price"]
    # filterset_fields = {
    #     "price": ["gte", "lte"],
    #     "publish_date": ["gte", "lte"]
    # }
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     if self.request.user.has_perm("myapp.view_book"):
    #         return self.queryset
    #     return self.queryset.none()
    # def get_queryset(self):
    #     return get_objects_for_user(self.request.user, "myapp.view_book", self.queryset)
    def get(self, request, *args, **kwargs):
        queryset = get_objects_for_user(request.user, "myapp.view_book", self.queryset.all())
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=200)


class APIBookDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = DetailBookSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    query_authors = User.objects.all().only("username")
    queryset = Book.objects.all().annotate(
        avg_rate=Avg("rate_book_user_book__rate"),
        total_order_=Sum("order_book_user_book__count")
    ).prefetch_related(
        Prefetch("authors", query_authors)
    )
    # permission_classes = [IsAuthenticated, HasPermission]
    authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        obj = self.queryset.get(pk=kwargs['pk'])
        result = get_40x_or_None(request, ["myapp.view_book"], obj, login_url="MyApp:login")
        if result is None:
            return Response(self.serializer_class(obj).data)
        return result


    # def put(self, request, *args, **kwargs):
    #     if request.user.has_perm("myapp.change_book"):
    #         return super().put(request, *args, **kwargs)
    #     return Response({}, status=status.HTTP_403_FORBIDDEN)
    #
    # def patch(self, request, *args, **kwargs):
    #     if request.user.has_perm("myapp.change_book"):
    #         return super().patch(request, *args, **kwargs)
    #     return Response({}, status=status.HTTP_403_FORBIDDEN)
    #
    # def delete(self, request, *args, **kwargs):
    #     if request.user.has_perm("myapp.delete_book"):
    #         return super().delete(request, *args, **kwargs)
    #     return Response({}, status=status.HTTP_403_FORBIDDEN)


class APICreateBook(CreateAPIView):
    serializer_class = CreateBookSerializer
    permission_classes = [IsAuthenticated]

    # def create(self, request, *args, **kwargs):
    #     if request.user.has_perm("myapp.add_book"):
    #         return super().create(request, *args, **kwargs)
    #     return Response({}, status=status.HTTP_403_FORBIDDEN)


class APiViewBook(ModelViewSet):
    queryset = Book.objects.annotate(
        avg_rate=Avg("rate_book_user_book__rate"),
        total_order_=Sum("order_book_user_book__count")
    ).prefetch_related(
        Prefetch("authors", User.objects.only("username"))
    )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DetailBookSerializer
        return BookSerializer

