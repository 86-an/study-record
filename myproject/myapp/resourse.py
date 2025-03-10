from import_export import resources, fields
from .models import Studyrecord

class StudyrecordResource(resources.ModelResource):
    date = fields.Field(attribute='date', column_name='日付')
    study_time = fields.Field(attribute='study_time', column_name='勉強時間')

    class Meta:
        model = Studyrecord
        fields = ('date', 'study_time')  # インポートするフィールドを指定
        import_id_fields = ('date',)
