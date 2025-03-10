from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Studyrecord
from .resourse import StudyrecordResource

# Register your models here.
@admin.register(Studyrecord)
class StudyRecordAdmin(ImportExportModelAdmin):
    resource_class = StudyrecordResource
    list_display = ('date', 'study_time')
    
    #検索
    search_fields = ('date', 'study_time')
    list_filter = ('date', 'study_time')