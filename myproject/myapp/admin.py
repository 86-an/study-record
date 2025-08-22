from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Studyrecord, MyTypingRecord, Sushida5000Record, Sushida10000Record
from .resourse import StudyrecordResource, MyTypingRecordResource, Sushida5000RecordResource, Sushida10000RecordResource
import pandas as pd
import os 


# Register your models here.
@admin.register(Studyrecord)
class StudyRecordAdmin(ImportExportModelAdmin):
    resource_class = StudyrecordResource
    list_display = ('date', 'study_time')
    
    #検索
    search_fields = ('date', 'study_time')
    list_filter = ('date', 'study_time')

# rank.xlsxのパス
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rank_file_path = os.path.join(BASE_DIR, 'myapp', 'data', 'rank.xlsx')

# rank.xlsxファイルの読み込み
df_rank = pd.read_excel(rank_file_path)

def determine_rank(score):
    """スコアに基づいてランクを判定"""
    for threshold, rank in df_rank.itertuples(index=False):
        if score >= threshold:
            return rank
    return 'G'

@admin.register(MyTypingRecord)
class TypingRecordAdmin(ImportExportModelAdmin):
    resource_class = MyTypingRecordResource
    list_display = ('date', 'accuracy_rate', 'score', 'rank')
    def save_model(self, request, obj, form, change):
        # スコアに基づいてランクを設定
        if not obj.rank:
            obj.rank = determine_rank(obj.score)
        super().save_model(request, obj, form, change)
    
        #検索
    search_fields = ('date', 'accuracy_rate', 'score', 'rank')
    list_filter = ('date', 'accuracy_rate', 'score', 'rank')

@admin.register(Sushida5000Record)
class Sushida5000RecordAdmin(ImportExportModelAdmin):
    resource_class = Sushida5000RecordResource
    list_display = ('date', 'accuracy_rate', 'score', 'rank')

    def save_model(self, request, obj, form, change):
        # correct_key と mistake_key が入力された場合に自動計算
        if obj.correct_key is not None and obj.mistake_key is not None:
            # 正打率の計算
            if (obj.correct_key + obj.mistake_key) > 0:  # 分母がゼロでないことを確認
                obj.accuracy_rate = round(
                    (obj.correct_key / (obj.correct_key + obj.mistake_key)) * 100, 1
                )
            else:
                obj.accuracy_rate = 0  # 分母がゼロの場合は正打率を0に設定

            # スコアの計算（秒数を90秒とする）
            obj.score = round(
                ((obj.correct_key - obj.mistake_key) / 90 * 1000), 0
            )

            # スコアに基づいてランクを設定
            obj.rank = determine_rank(obj.score)  # `determine_rank`はカスタム関数

        # データを保存
        super().save_model(request, obj, form, change)

    # 検索フィールド
    search_fields = ('date', 'accuracy_rate', 'score', 'rank')
    
    # フィルタフィールド
    list_filter = ('date', 'accuracy_rate', 'score', 'rank')


@admin.register(Sushida10000Record)
class Sushida10000RecordAdmin(ImportExportModelAdmin):
    resource_class = Sushida10000RecordResource
    list_display = ('date', 'accuracy_rate', 'score', 'rank')

    def save_model(self, request, obj, form, change):
        # correct_key と mistake_key が入力された場合に自動計算
        if obj.correct_key is not None and obj.mistake_key is not None:
            # 正打率の計算
            if (obj.correct_key + obj.mistake_key) > 0:  # 分母がゼロでないことを確認
                obj.accuracy_rate = round(
                    (obj.correct_key / (obj.correct_key + obj.mistake_key)) * 100, 1
                )
            else:
                obj.accuracy_rate = 0  # 分母がゼロの場合は正打率を0に設定

            # スコアの計算（秒数を90秒とする）
            obj.score = round(
                ((obj.correct_key - obj.mistake_key) / 120 * 1000), 0
            )

            # スコアに基づいてランクを設定
            obj.rank = determine_rank(obj.score)  # `determine_rank`はカスタム関数

        # データを保存
        super().save_model(request, obj, form, change)

    # 検索フィールド
    search_fields = ('date', 'accuracy_rate', 'score', 'rank')
    
    # フィルタフィールド
    list_filter = ('date', 'accuracy_rate', 'score', 'rank')