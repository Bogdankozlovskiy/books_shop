from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Avg, Sum, Prefetch, Count, F
from django.http import JsonResponse
from django.core.cache import cache

from myapp.models import Book, RateBookUser, OrderBookUser, Comment
from myapp.tasks import nlp_process


def hello(request):
    all_books = cache.get("all_books")
    if all_books is not None:
        return render(request, "index.html", {"books": all_books})
    query_1 = Comment.objects.annotate(likes=F("my_custom_like")).select_related("user")
    query_2 = Book.objects.annotate(
        avg_rate=Avg("rate_book_user_book__rate"),
        total_order=Sum("order_book_user_book__count")
    ).prefetch_related("authors", Prefetch("comments", query_1)).select_related("country").all()
    cache.set("all_books", query_2, 10)
    return render(request, "index.html", {"books": query_2})


@login_required(login_url="MyApp:login")
def add_rate(request, rate, book_id):
    RateBookUser.objects.update_or_create(user_id=request.user.id, book_id=book_id, defaults={"rate": rate})
    return redirect("MyApp:main-page")


@login_required(login_url="MyApp:login")
def order_book(request, book_id):
    OrderBookUser.objects.create(
        count=request.POST.get("count"),
        user_id=request.user.id,
        book_id=book_id
    )
    return redirect("MyApp:main-page")


@login_required(login_url="MyApp:login")
def add_comment(request, book_id):
    Comment.objects.create(
        user_id=request.user.id,
        text=request.POST.get("comment"),
        book_id=book_id
    )
    # nlp_process(request.POST.get("comment"))
    nlp_process.delay(request.POST.get("comment"))
    return redirect("MyApp:main-page")


@login_required(login_url="MyApp:login")
def delete_comment(request, comment_id):
    query_set = Comment.objects.filter(id=comment_id)
    if query_set.exists():
        if query_set.first().user.id == request.user.id:
            query_set.delete()
    return redirect("MyApp:main-page")


@login_required(login_url="MyApp:login")
def update_comment(request, comment_id):
    comment_query = Comment.objects.filter(id=comment_id)
    if comment_query.exists():
        if request.method == "GET":
            return render(request, "comment_form.html", {"comment": comment_query.first()})
        if request.method == "POST":
            comment_query.update(text=request.POST.get("comment"))
    return redirect("MyApp:main-page")


@login_required(login_url="MyApp:login")
def my_account(request):
    ordered_book_query_set = OrderBookUser.objects.filter(user_id=request.user.id).select_related("book").order_by("book__title")
    ordered_book_query_set = ordered_book_query_set.annotate(total_price=F("book__price") * F("count"))
    ordered_book_query_set = ordered_book_query_set.only("count", "date", "book__title", "book__price")
    tt_price = ordered_book_query_set.aggregate(tt_sum=Sum("total_price"))
    context = {"ordered_book": ordered_book_query_set}
    context.update(tt_price)
    return render(request, "ordered_book.html", context)


@login_required(login_url="MyApp:login")
def logout_view(request):
    logout(request)
    return redirect("MyApp:main-page")


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("login"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
        else:
            return redirect("MyApp:login")
    return redirect("MyApp:main-page")


@login_required(login_url="MyApp:login")
def add_like_to_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user in comment.like.all():
        comment.like.remove(request.user)
    else:
        comment.like.add(request.user)
    comment.save()
    return redirect("MyApp:main-page")


def add_like_to_comment_ajax(request, comment_id):
    print(request.GET)
    comment = Comment.objects.get(id=comment_id)
    if request.user in comment.like.all():
        comment.like.remove(request.user)
        Comment.like.through
    else:
        comment.like.add(request.user)
    comment.save()
    return JsonResponse({"likes": comment.like.count()})

# API Application programm interface
# REST API
