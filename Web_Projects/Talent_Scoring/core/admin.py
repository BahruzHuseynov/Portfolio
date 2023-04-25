from django.contrib import admin
from core import models


# Register your models here.


class AnswerTabularInline(admin.TabularInline):
    model = models.Answers
    fields = ('answer_title', 'answer_weight', 'related_question',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title','order_by',)
    inlines = [AnswerTabularInline, ]
    search_fields = ('question_title',)


admin.site.register(models.Questions, QuestionAdmin)
admin.site.register(models.StageModel)
admin.site.register(models.AboutUs)
admin.site.register(models.Contact)
