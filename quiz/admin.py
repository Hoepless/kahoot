from django.contrib import admin
import nested_admin

from .models import Quiz, Question, Answer, QuizTaker, QuizTakerResponse


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 4
    max_num = 4

    def has_delete_permission(self, request, obj=None):
        return False


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInline,]
    extra = 1


class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline, ]


    def has_delete_permission(self, request, obj=None):
        return False


class QuizTakerResponseInline(admin.TabularInline):
    model = QuizTakerResponse


class QuizTakerAdmin(admin.ModelAdmin):
    inlines = [QuizTakerResponseInline,]



admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizTaker, QuizTakerAdmin)
admin.site.register(QuizTakerResponse)
