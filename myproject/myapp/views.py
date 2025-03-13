from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import urllib, base64
import numpy as np
import pandas as pd
import logging
import io  # 追加
from .models import Studyrecord

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
        avg_study_time = df['study_time'].mean()
        median_study_time = df['study_time'].median()
        total_study_time = df['study_time'].sum()
        count_study_time = df['study_time'].count()

        # 今日の日付
        today = timezone.now().date()

        # 今日の勉強時間の順位を計算
        today_study_records = df[df['date'] == today].sort_values(by='study_time', ascending=False)
        rank = today_study_records.index[0] + 1 if not today_study_records.empty else 'No Data'  # 今日のデータが存在しない場合

        stats = {
            'max': max_study_time,
            'min': min_study_time,
            'mean': avg_study_time,
            'median': median_study_time,
            'sum': total_study_time,
            'count': count_study_time,
            'rank_today': rank
        }

    # グラフの作成
    if not df.empty:
        fig, ax = plt.subplots()
        ax.plot(df['date'], df['study_time'], marker='o')
        ax.set(xlabel='Date', ylabel='Study Time (hours)', title='Study Time Chart')
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
