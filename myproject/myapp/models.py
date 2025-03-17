from django.db import models
import pandas as pd 
import os 

#rank.xlsxのパスと読み込み
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rank_file_path = os.path.join(BASE_DIR, 'myapp', 'data', 'rank.xlsx')
df_rank = pd.read_excel(rank_file_path)

def determine_rank(score):
    for threshold, rank in df_rank.itertuples(index = False):
        if score >= threshold:
            return rank 
    return 'G'

# Create your models here.
#勉強時間
class Studyrecord(models.Model):
    date = models.DateField(verbose_name='日付')
    study_time = models.FloatField(verbose_name='勉強時間')
    
 #mytypingの記録
class MyTypingRecord(models.Model):
    date = models.DateField(verbose_name="日付")  # 日付
    accuracy_rate = models.FloatField(verbose_name="正打率")  # 正打率
    score = models.IntegerField(verbose_name="スコア")  # スコア
    rank = models.CharField(max_length=10, blank=True, verbose_name="ランク")  # ランク

class Sushida5000Record(models.Model):
    date = models.DateField(verbose_name="日付")  # 日付
    accuracy_rate = models.FloatField(verbose_name="正打率")  # 正打率
    score = models.IntegerField(verbose_name="スコア")  # スコア
    rank = models.CharField(max_length=10, blank=True, verbose_name="ランク")  # ランク
    correct_key = models.IntegerField(default=0)
    mistake_key = models.IntegerField(default=0)
    
class Sushida10000Record(models.Model):
    date = models.DateField(verbose_name="日付")  # 日付
    accuracy_rate = models.FloatField(verbose_name="正打率")  # 正打率
    score = models.IntegerField(verbose_name="スコア")  # スコア
    rank = models.CharField(max_length=10, blank=True, verbose_name="ランク")  # ランク