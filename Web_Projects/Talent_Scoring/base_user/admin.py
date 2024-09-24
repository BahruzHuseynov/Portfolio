from django.contrib import admin
from base_user import models as bm
# Register your models here.

admin.site.register(bm.MyUser)



class ResultAnswersModelAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'question_name', 'answer_name', 'weight_number' ,'weight_type']


admin.site.register(bm.ResultAnswersModel, ResultAnswersModelAdmin)