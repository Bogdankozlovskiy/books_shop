from django.contrib import admin
from myapp.models import Book, Country, Comment
from guardian.admin import GuardedModelAdmin


class InlineCommentAdmin(admin.StackedInline):
    model = Comment
    extra = 2
    readonly_fields = ["my_custom_like"]


class BookAdmin(GuardedModelAdmin):
    inlines = [InlineCommentAdmin]
    list_display = ["title", "id"]


admin.site.register(Book, BookAdmin)
admin.site.register(Country)
# Register your models here.
# add something
# task 1
# task 2
