from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.db.models import OuterRef


class Book(models.Model):
    class Meta:
        db_table = "book"
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    title = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    authors = models.ManyToManyField(User, related_name="books", verbose_name="Авторы")
    publish_date = models.DateField(auto_now=True)
    text = models.TextField(verbose_name="Содержание")
    rate = models.ManyToManyField(User, related_name="rated_books", through="myapp.RateBookUser")
    order = models.ManyToManyField(User, related_name="ordered_books", through="myapp.OrderBookUser")
    price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="цена", validators=[validators.MinValueValidator(0)])

    def get_rate(self):
        arr = list(RateBookUser.objects.filter(book=self).values_list("rate", flat=True))
        if arr:
            return sum(arr) / len(arr)

    def get_total_order(self):
        arr = list(OrderBookUser.objects.filter(book=self).values_list("count", flat=True))
        if arr:
            return sum(arr)
        return 0

    def __str__(self):
        return self.title


class RateBookUser(models.Model):
    class Meta:
        unique_together = ("user", "book")

    rate = models.PositiveIntegerField(
        default=1,
        validators=[validators.MaxValueValidator(5), validators.MinValueValidator(1)]
        )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rate_book_user_user")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="rate_book_user_book")


class OrderBookUser(models.Model):
    count = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
