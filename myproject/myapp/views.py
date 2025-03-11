from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import urllib, base64
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
    
    #グラフをファイルに保存
    image_path = os.path.join(settings.MEDIA_ROOT, 'chart.png')
    canvas = FigureCanvas(fig)
    canvas.print_png(open(image_path, 'wb'))
    
    #画像ファイルをレスポンスとして返す
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
    
    