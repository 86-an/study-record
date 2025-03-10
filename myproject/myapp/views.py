from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import urllib, base64
from .models import Studyrecord

# Create your views here.
def home(request):
    return render(request, 'myapp/home.html')

def study_time_chart(request):
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
    
    #グラフをバイナリーデータとして保存
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    
    #テンプレートにデータを渡す
    context = {'data': uri}
    return render(request, 'myapp/study_time_chart.html',
                  context)
    