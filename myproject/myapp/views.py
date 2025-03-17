from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os
import urllib, base64
import numpy as np
import pandas as pd
import logging
import io  # 追加
from .models import Studyrecord, MyTypingRecord, Sushida5000Record, Sushida10000Record

# Create your views here.
def home(request):
    return render(request, 'myapp/home.html')

def study_time(request):
    # データの取得
    study_data = Studyrecord.objects.all().values('date', 'study_time')
    
    # pandasのDataFrameに変換
    df = pd.DataFrame(list(study_data))
    
    stats = None
    if not df.empty:
        # 勉強時間の統計量計算（最大、最小、平均、中央値、合計、カウント）
        max_study_time = df['study_time'].max()
        min_study_time = df['study_time'].min()
        avg_study_time = (df['study_time'].mean()).round(1)
        median_study_time = df['study_time'].median()
        total_study_time = df['study_time'].sum()
        count_study_time = (df['study_time'] > 0).sum()

        # 今日の日付
        today = timezone.now().date()

        # 今日の勉強時間の順位を計算
        today_study_records = df[df['date'] == today].sort_values(by='study_time', ascending=False)
        rank = today_study_records.index[0] + 1 if not today_study_records.empty else 'No Data'  # 今日のデータが存在しない場合

        stats = {
            '最大値': max_study_time,
            '最小値': min_study_time,
            '平均': avg_study_time,
            '中央値': median_study_time,
            '合計': total_study_time,
            'カウント': count_study_time,
            '今日の順位': rank
        }

    # グラフの作成
    rcParams['font.family'] = 'Meiryo'
    if not df.empty:
        fig, ax = plt.subplots()
        ax.plot(df['date'], df['study_time'])
        ax.set(xlabel='日付', ylabel='勉強時間 (hours)', title='勉強時間のグラフ')
        ax.grid()

        # x軸ラベルをカスタマイズ
        import matplotlib.dates as mdates
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        # グラフを画像として保存
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        image_base64 = base64.b64encode(image_png).decode('utf-8')
    else:
        image_base64 = None

    return render(request, 'myapp/study_time_chart.html', {'stats': stats, 'chart_image': image_base64})

def typing(request):
    # mytypingのデータの取得
    mytyping = MyTypingRecord.objects.all().values('date', 'accuracy_rate', 'score', 'rank')
    
    # pandasのDataFrameに変換
    df_mytyping = pd.DataFrame(list(mytyping))
    
    if not df_mytyping.empty:
        # mytypingの統計量計算（最大、最小、平均、中央値、合計、カウント）
        max_mytyping_score = df_mytyping['score'].max()
        min_mytyping_score = df_mytyping['score'].min()
        avg_mytyping_score = (df_mytyping['score'].mean()).round(1)
        median_mytyping_score = df_mytyping['score'].median()
        count_mytyping_score = len(df_mytyping)
        # 最新の順位
        latest_mytyping_score = df_mytyping['score'].iloc[-1]
        df_mytypig_score_sorted = df_mytyping.sort_values(by='score', ascending=False).reset_index(drop=True)
        latest_mytyping_score_rank = df_mytypig_score_sorted[df_mytypig_score_sorted['score'] ==latest_mytyping_score].index[0] + 1  # インデックスは0から始まるため+1

        mytyping_score_stats = {
            '最大値': max_mytyping_score,
            '最小値': min_mytyping_score,
            '平均': avg_mytyping_score,
            '中央値': median_mytyping_score,
            'カウント': count_mytyping_score,
            '最新の順位': latest_mytyping_score_rank,
        }
        
        # mytypingの統計量計算（最大、最小、平均、中央値、合計、カウント）
        max_mytyping_accuracy_rate = df_mytyping['accuracy_rate'].max()
        min_mytyping_accuracy_rate = df_mytyping['accuracy_rate'].min()
        avg_mytyping_accuracy_rate = (df_mytyping['accuracy_rate'].mean()).round(1)
        median_mytyping_accuracy_rate = df_mytyping['accuracy_rate'].median()
        count_mytyping_accuracy_rate = len(df_mytyping)
        # 最新の順位
        latest_mytyping_accuracy_rate = df_mytyping['accuracy_rate'].iloc[-1]
        df_mytypig_accuracy_rate_sorted = df_mytyping.sort_values(by='accuracy_rate', ascending=False).reset_index(drop=True)
        latest_mytyping_accuracy_rate_rank = df_mytypig_accuracy_rate_sorted[df_mytypig_accuracy_rate_sorted['accuracy_rate'] ==latest_mytyping_accuracy_rate].index[0] + 1  # インデックスは0から始まるため+1

        mytyping_accuracy_rate_stats = {
            '最大値': max_mytyping_accuracy_rate,
            '最小値': min_mytyping_accuracy_rate,
            '平均': avg_mytyping_accuracy_rate,
            '中央値': median_mytyping_accuracy_rate,
            'カウント': count_mytyping_accuracy_rate,
            '最新の順位': latest_mytyping_accuracy_rate_rank,
        }
        
    # sushida5000のデータの取得
    sushida5000 = Sushida5000Record.objects.all().values('date', 'accuracy_rate', 'score', 'rank')
    
    # pandasのDataFrameに変換
    df_sushida5000 = pd.DataFrame(list(sushida5000))
    
    if not df_sushida5000.empty:
        max_sushida5000_score = df_sushida5000['score'].max()
        min_sushida5000_score = df_sushida5000['score'].min()
        avg_sushida5000_score = (df_sushida5000['score'].mean()).round(1)
        median_sushida5000_score = df_sushida5000['score'].median()
        count_sushida5000_score = len(df_sushida5000)
        # 最新の順位
        latest_sushida5000_score = df_sushida5000['score'].iloc[-1]
        df_sushida5000_score_sorted = df_sushida5000.sort_values(by='score', ascending=False).reset_index(drop=True)
        latest_sushida5000_score_rank = df_sushida5000_score_sorted[df_sushida5000_score_sorted['score'] == latest_sushida5000_score].index[0] + 1

        sushida5000_score_stats = {
            '最大値': max_sushida5000_score,
            '最小値': min_sushida5000_score,
            '平均': avg_sushida5000_score,
            '中央値': median_sushida5000_score,
            'カウント': count_sushida5000_score,
            '最新の順位': latest_sushida5000_score_rank,
        }

        # sushida5000の統計量計算（最大、最小、平均、中央値、合計、カウント）
        max_sushida5000_accuracy_rate = df_sushida5000['accuracy_rate'].max()
        min_sushida5000_accuracy_rate = df_sushida5000['accuracy_rate'].min()
        avg_sushida5000_accuracy_rate = (df_sushida5000['accuracy_rate'].mean()).round(1)
        median_sushida5000_accuracy_rate = df_sushida5000['accuracy_rate'].median()
        count_sushida5000_accuracy_rate = len(df_sushida5000)
        # 最新の順位
        latest_sushida5000_accuracy_rate = df_sushida5000['accuracy_rate'].iloc[-1]
        df_sushida5000_accuracy_rate_sorted = df_sushida5000.sort_values(by='accuracy_rate', ascending=False).reset_index(drop=True)
        latest_sushida5000_accuracy_rate_rank = df_sushida5000_accuracy_rate_sorted[df_sushida5000_accuracy_rate_sorted['accuracy_rate'] == latest_sushida5000_accuracy_rate].index[0] + 1

        sushida5000_accuracy_rate_stats = {
            '最大値': max_sushida5000_accuracy_rate,
            '最小値': min_sushida5000_accuracy_rate,
            '平均': avg_sushida5000_accuracy_rate,
            '中央値': median_sushida5000_accuracy_rate,
            'カウント': count_sushida5000_accuracy_rate,
            '最新の順位': latest_sushida5000_accuracy_rate_rank,
        }

    # データの取得
    sushida10000 = Sushida10000Record.objects.all().values('date', 'accuracy_rate', 'score', 'rank')

    # pandasのDataFrameに変換
    df_sushida10000 = pd.DataFrame(list(sushida10000))

    if not df_sushida10000.empty:
        max_sushida10000_score = df_sushida10000['score'].max()
        min_sushida10000_score = df_sushida10000['score'].min()
        avg_sushida10000_score = (df_sushida10000['score'].mean()).round(1)
        median_sushida10000_score = df_sushida10000['score'].median()
        count_sushida10000_score = len(df_sushida10000)
        # 最新の順位
        latest_sushida10000_score = df_sushida10000['score'].iloc[-1]
        df_sushida10000_score_sorted = df_sushida10000.sort_values(by='score', ascending=False).reset_index(drop=True)
        latest_sushida10000_score_rank = df_sushida10000_score_sorted[df_sushida10000_score_sorted['score'] == latest_sushida10000_score].index[0] + 1

        sushida10000_score_stats = {
            '最大値': max_sushida10000_score,
            '最小値': min_sushida10000_score,
            '平均': avg_sushida10000_score,
            '中央値': median_sushida10000_score,
            'カウント': count_sushida10000_score,
            '最新の順位': latest_sushida10000_score_rank,
        }

        # sushida10000の統計量計算（最大、最小、平均、中央値、合計、カウント）
        max_sushida10000_accuracy_rate = df_sushida10000['accuracy_rate'].max()
        min_sushida10000_accuracy_rate = df_sushida10000['accuracy_rate'].min()
        avg_sushida10000_accuracy_rate = (df_sushida10000['accuracy_rate'].mean()).round(1)
        median_sushida10000_accuracy_rate = df_sushida10000['accuracy_rate'].median()
        count_sushida10000_accuracy_rate = len(df_sushida10000)
        # 最新の順位
        latest_sushida10000_accuracy_rate = df_sushida10000['accuracy_rate'].iloc[-1]
        df_sushida10000_accuracy_rate_sorted = df_sushida10000.sort_values(by='accuracy_rate', ascending=False).reset_index(drop=True)
        latest_sushida10000_accuracy_rate_rank = df_sushida10000_accuracy_rate_sorted[df_sushida10000_accuracy_rate_sorted['accuracy_rate'] == latest_sushida10000_accuracy_rate].index[0] + 1

        sushida10000_accuracy_rate_stats = {
            '最大値': max_sushida10000_accuracy_rate,
            '最小値': min_sushida10000_accuracy_rate,
            '平均': avg_sushida10000_accuracy_rate,
            '中央値': median_sushida10000_accuracy_rate,
            'カウント': count_sushida10000_accuracy_rate,
            '最新の順位': latest_sushida10000_accuracy_rate_rank,
        }

    # グラフ作成
    if not df_mytyping.empty and not df_sushida5000.empty and not df_sushida10000.empty:
        rcParams['font.family'] = 'Meiryo'  # 日本語フォント対応
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))  # 2行2列のグラフ

        # mytypingのスコアグラフ
        axes[0, 0].plot(df_mytyping['date'], df_mytyping['score'], color='blue', label='mytyping スコア')
        axes[0, 0].set_title('mytypingのスコア推移', fontsize=14)
        axes[0, 0].set_xlabel('日付')
        axes[0, 0].set_ylabel('スコア')
        axes[0, 0].legend(loc='upper left')
        axes[0, 0].grid()

        # mytypingの正打率グラフ
        axes[0, 1].plot(df_mytyping['date'], df_mytyping['accuracy_rate'], color='blue', label='mytyping 正打率')
        axes[0, 1].set_title('mytypingの正打率推移', fontsize=14)
        axes[0, 1].set_xlabel('日付')
        axes[0, 1].set_ylabel('正打率 (%)')
        axes[0, 1].legend(loc='upper left')
        axes[0, 1].grid()

        # sushida5000とsushida10000のスコア比較グラフ
        axes[1, 0].plot(df_sushida5000['date'], df_sushida5000['score'], color='green', label='sushida5000 スコア')
        axes[1, 0].plot(df_sushida10000['date'], df_sushida10000['score'], color='orange', label='sushida10000 スコア')
        axes[1, 0].set_title('sushida5000とsushida10000のスコア比較', fontsize=14)
        axes[1, 0].set_xlabel('日付')
        axes[1, 0].set_ylabel('スコア')
        axes[1, 0].legend(loc='upper left')
        axes[1, 0].grid()

        # sushida5000とsushida10000の正打率比較グラフ
        axes[1, 1].plot(df_sushida5000['date'], df_sushida5000['accuracy_rate'], color='green', label='sushida5000 正打率')
        axes[1, 1].plot(df_sushida10000['date'], df_sushida10000['accuracy_rate'], color='orange', label='sushida10000 正打率')
        axes[1, 1].set_title('sushida5000とsushida10000の正打率比較', fontsize=14)
        axes[1, 1].set_xlabel('日付')
        axes[1, 1].set_ylabel('正打率 (%)')
        axes[1, 1].legend(loc='upper left')
        axes[1, 1].grid()

        # グラフを画像として保存
        buffer = io.BytesIO()
        plt.tight_layout()  # レイアウト調整
        plt.savefig(buffer, format='png')  # PNG形式で保存
        buffer.seek(0)
        combined_image_png = buffer.getvalue()
        buffer.close()
        typing_image_base64 = base64.b64encode(combined_image_png).decode('utf-8')  # Base64にエンコード
    else:
        typing_image_base64 = None
        
    return render(request, 'myapp/typing_chart.html', {
'mytyping_score_stats': mytyping_score_stats,
'mytyping_accuracy_rate_stats': mytyping_accuracy_rate_stats,
'sushida5000_score_stats': sushida5000_score_stats,
'sushida5000_accuracy_rate_stats': sushida5000_accuracy_rate_stats,
'sushida10000_score_stats': sushida10000_score_stats,
'sushida10000_accuracy_rate_stats': sushida10000_accuracy_rate_stats,
'typing_chart_image': typing_image_base64
})