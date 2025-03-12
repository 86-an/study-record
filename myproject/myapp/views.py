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
from .models import Studyrecord

# Create your views here.
def home(request):
    return render(request, 'myapp/home.html')

def study_time_chart(request):
    return render(request, 'myapp/study_time_chart.html')
    
def chart_image(request):
    #データの取得と準備
    study_data = Studyrecord.objects.all()
    dates = [record.date for record in study_data]
    study_times = [record.study_time for record in study_data]
    
    #グラフの描画
    fig, ax = plt.subplots()
    ax.plot(dates, study_times)
    
    ax.set(xlabel='Date', ylabel='Study Time (hours)',
           title='Study Time Chart')
    ax.grid()
    
    #x軸ラベルをカスタマイズ
   # x軸ラベルの間隔を設定
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    
    #グラフをファイルに保存
    image_path = os.path.join(settings.MEDIA_ROOT, 'chart.png')
    canvas = FigureCanvas(fig)
    canvas.print_png(open(image_path, 'wb'))
    
    #画像ファイルをレスポンスとして返す
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
    
logger = logging.getLogger(__name__)
def study_time_stats(request):
    # データの取得
    study_data = Studyrecord.objects.all()
    
    #デバック用
    logger.debug(f'Study data: {list(study_data)}')
    print(f'Study data: {list(study_data)}')
    if not study_data:
        return render(request, 'myapp/study_time_chart.html', {'stats': None})
    
    # リストからnumpy配列に変換
    study_times = np.array([record['study_time'] for record in study_data])
    dates = np.array([record['date'] for record in study_data])
    
    # 勉強時間の統計量計算（最大、最小、平均、中央値、合計、カウント）
    max_study_time = float(np.max(study_times))
    min_study_time = float(np.min(study_times))
    avg_study_time = float(np.mean(study_times))
    median_study_time = float(np.median(study_times))
    total_study_time = float(np.sum(study_times))
    count_study_time = int(len(study_times))

    # 今日の日付
    today = timezone.now().date()

    # 今日の勉強時間の順位を計算
    today_study_records = Studyrecord.objects.filter(date=today).order_by('-study_time')
    if today_study_records.exists():
        today_study_times = np.array(today_study_records.values_list('study_time', flat=True))
        today_rank_times = study_times[dates == today]
        rank = list(today_study_times).index(today_rank_times[0]) + 1 if len(today_rank_times) > 0 else 'No Data'
    else:
        rank = 'No Data'  # 今日のデータが存在しない場合

    stats = {
        '最大': max_study_time,
        '最小': min_study_time,
        '平均': avg_study_time,
        '中央値': median_study_time,
        '合計': total_study_time,
        'カウント': count_study_time,
        '今日の順位': rank
    }

    return render(request, 'myapp/study_time_chart.html', {'stats': stats})
