from rest_framework.serializers import ModelSerializer, DecimalField, IntegerField, HyperlinkedModelSerializer, \
    HyperlinkedIdentityField, HiddenField, HyperlinkedRelatedField
from myapp.models import Book, Country
from django.contrib.auth.models import User
from myapp.models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ["name"]


class BookSerializer(HyperlinkedModelSerializer):
    authors = UserSerializer(many=True)
    country = CountrySerializer()
    total_rate = DecimalField(source="avg_rate", max_digits=5, decimal_places=2)
    detail_book = HyperlinkedIdentityField(view_name="Api:detail-book")
    comments = HyperlinkedIdentityField(view_name="Api:view-comment", many=True)

    class Meta:
        model = Book
        fields = ["id", "title", "authors", "price", "country", "total_rate", "detail_book", "comments"]


class DetailBookSerializer(ModelSerializer):
    authors = UserSerializer(many=True)
    country = CountrySerializer()
    total_rate = DecimalField(source="avg_rate", max_digits=5, decimal_places=2)
    total_order = IntegerField(source="total_order_")

    class Meta:
        model = Book
        fields = ["id", "title", "authors", "price", "country", "total_rate", "text", "publish_date", "total_order"]


class CreateBookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "authors", "text", "price", "country"]
