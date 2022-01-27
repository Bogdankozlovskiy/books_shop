from django.core import validators
from django.db import models
from django.contrib.auth.models import User
# from functools import partial
from django.dispatch import receiver, Signal


# my_signal = Signal(providing_args=["a", "b"], use_caching=True)


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
    country = models.ForeignKey("Country", on_delete=models.SET_DEFAULT, default=1)

    objects = models.Manager()

    def __str__(self):
        return self.title


class AuthorsStatistic(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_book_user_user")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="order_book_user_book")


class Country(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Comment(models.Model):
    class Meta:
        order_with_respect_to = 'book'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    # like = models.ManyToManyField(User)
    new_like = models.ManyToManyField(User, through="CommentBookLike", related_name="test_name_comment")
    my_custom_like = models.IntegerField(default=0)

    objects = models.Manager()

    def save(self, **kwargs):
        # my_signal.send(sender=self.__class__, a=5, b=6)
        data = super().save(**kwargs)
        return data


class CommentBookLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


def add_like(*args, **kwargs):
    instance = kwargs['instance']
    instance.comment.my_custom_like += 1
    instance.comment.save()


def sub_like(*args, **kwargs):
    instance = kwargs['instance']
    instance.comment.my_custom_like -= 1
    instance.comment.save()


models.signals.post_save.connect(add_like, sender=CommentBookLike)
models.signals.post_delete.connect(sub_like, sender=CommentBookLike)


def count_authors(sender, instance, **kwargs):
    action = kwargs['action']
    if action == "post_add":
        pk_set = kwargs['pk_set']
        for author_id in pk_set:
            author_set = AuthorsStatistic.objects.filter(author_id=author_id)
            if author_set.exists():
                author = author_set.first()
                author.count += 1
                author.save()
            else:
                AuthorsStatistic.objects.create(author_id=author_id, count=1)


models.signals.m2m_changed.connect(count_authors, sender=Book.authors.through)
