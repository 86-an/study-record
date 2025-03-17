from import_export import resources, fields
from .models import Studyrecord, MyTypingRecord, Sushida5000Record, Sushida10000Record
#勉強時間
class StudyrecordResource(resources.ModelResource):
    date = fields.Field(attribute='date', column_name='日付')
    study_time = fields.Field(attribute='study_time', column_name='勉強時間')

    class Meta:
        model = Studyrecord
        fields = ('date', 'study_time')  # インポートするフィールドを指定
        import_id_fields = ('date',)

#mytyping
class MyTypingRecordResource(resources.ModelResource):
    date = fields.Field(attribute='date', column_name='日付')
    accuracy_rate = fields.Field(attribute='accuracy_rate', column_name='正打率')
    score = fields.Field(attribute='score', column_name='スコア')
    rank = fields.Field(attribute='rank', column_name='ランク')

    class Meta:
        model = MyTypingRecord
        fields = ('date', 'accuracy_rate', 'score', 'rank')  # 必要なフィールド
        import_id_fields = ('date', )  # 一意性のキーを指定（例：日付）

#sushida5000
class Sushida5000RecordResource(resources.ModelResource):
    date = fields.Field(attribute='date', column_name='日付')
    accuracy_rate = fields.Field(attribute='accuracy_rate', column_name='正打率')
    score = fields.Field(attribute='score', column_name='スコア')
    rank = fields.Field(attribute='rank', column_name='ランク')
    correct_key = fields.Field(attribute='correct_key', column_name='正しく打ったキー')  # 正しく打ったキー
    mistake_key = fields.Field(attribute='mistake_key', column_name='ミス')  # ミス

    class Meta:
        model = Sushida5000Record
        fields = ('date', 'correct_key', 'mistake_key', 'accuracy_rate', 'score', 'rank')
        export_order = ('date', 'correct_key', 'mistake_key', 'accuracy_rate', 'score', 'rank')

        
#sushida10000
class Sushida10000RecordResource(resources.ModelResource):
    date = fields.Field(attribute='date', column_name='日付')
    accuracy_rate = fields.Field(attribute='accuracy_rate', column_name='正打率')
    score = fields.Field(attribute='score', column_name='スコア')
    rank = fields.Field(attribute='rank', column_name='ランク')

    class Meta:
        model = Sushida10000Record
        fields = ('date', 'accuracy_rate', 'score', 'rank')  # 必要なフィールド
        import_id_fields = ('date', )  # 一意性のキーを指定（例：日付）