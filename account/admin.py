from django.contrib import admin
from django.contrib.auth import get_user_model
import nested_admin

from quiz.models import QuizTakerResponse, QuizTaker
from .models import User, MyUser


class QuizTakerResult(admin.StackedInline):
    model = QuizTaker
    fields = ('quiz', 'questions', 'answers', )
    readonly_fields = ('quiz', 'questions', 'answers')

    def has_delete_permission(self, request, obj=None):
        return False


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'group',
        'phone',
        'email',
        'final_score',
        'rating_place',
        'group_rating_place',
    )
    search_fields = ('first_name', 'last_name', 'phone')
    list_filter = ('group', )


class LeaderAdmin(admin.ModelAdmin):
    model = User
    list_display = (
        'first_name',
        'last_name',
        'group',
        'phone',
        'email',
        'final_score',
        'rating_place',
        'group_rating_place',
        'tests_passed',
    )
    search_fields = ('first_name', 'last_name', 'phone')
    list_filter = ('group',)
    inlines = [QuizTakerResult,]


admin.site.register(User, UserAdmin)
admin.site.register(MyUser, LeaderAdmin)

