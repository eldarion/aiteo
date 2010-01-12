from django.contrib import admin

from aiteo.models import Question, Response



class ResponseInline(admin.StackedInline):
    model = Response


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ResponseInline,
    ]



admin.site.register(Question, QuestionAdmin)