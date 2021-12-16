from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from myapp.models import Comment
from api.serializers import BookSerializer, DetailBookSerializer, CreateBookSerializer
from myapp.models import Book
from django.db.models import Prefetch, Avg, Sum
from django.contrib.auth.models import User


class APIAddLike(APIView):
    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        if request.user in comment.like.all():
            comment.like.remove(request.user)
        else:
            comment.like.add(request.user)
        comment.save()
        return Response({"likes": comment.like.count()})


class APIListBook(ListAPIView):
    serializer_class = BookSerializer
    query_authors = User.objects.all().only("username")
    queryset = Book.objects.all().annotate(avg_rate=Avg("rate_book_user_book__rate")).prefetch_related(
        Prefetch("authors", query_authors)
    )


class APIBookDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = DetailBookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    query_authors = User.objects.all().only("username")
    queryset = Book.objects.all().annotate(
        avg_rate=Avg("rate_book_user_book__rate"),
        total_order_=Sum("order_book_user_book__count")
    ).prefetch_related(
        Prefetch("authors", query_authors)
    )


class APICreateBook(CreateAPIView):
    serializer_class = CreateBookSerializer
    permission_classes = [IsAuthenticated]

