from django.urls import path
from api import views
# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register("view_book", views.APiViewBook)

app_name = 'Api'
urlpatterns = [
    path("add_like_to_comment_ajax/<int:comment_id>/", views.APIAddLike.as_view(), name="add-like-to-comment"),
    path("books/", views.APIListBook.as_view(), name="list-book"),
    path("books/<int:pk>/", views.APIBookDetail.as_view(), name="detail-book"),
    path("create_book/", views.APICreateBook.as_view(), name="create-book"),
    path("view_book/", views.APiViewBook.as_view({"get": "list"}), name="view-book-list"),
    path("view_book/<int:pk>/", views.APiViewBook.as_view({"get": "retrieve", "delete": "destroy"}), name="view-book-retrieve"),
    path("view_comment/<int:pk>/", views.APIVIEWComment.as_view(), name="view-comment"),
    path("create_message/", views.APICreateMessage.as_view())
]  # + router.urls
