# study-record

## 概要
- 勉強やタイピングの記録をグラフや表にする
- Excelのデータを一括でインポートする（管理者側（admin））
- 今回はサーバーではなく、ローカルの実行を想定

## 目的
- djangoのお試し
- 記録の入力、グラフと表にできる

## 使い方(ターミナル)
- /venv/Scripts/Activate
- cd myproject
- python manage.py runserver

## 管理者ページのパスワード
- ユーザー名： "python2024" #記号はいらない
- パスワード： "studyrecord"

## 使用
- 言語：Python 3.13.3
- ライブラリ：pandas, numpy, matplotlib
- フレームワーク：django

## 機能
- スコアの計算、スコア、順位、統計を表にする
- グラフはスコアと正打率を作る

## 工夫
- excelからデータをインポートできる（管理者のみ）
- スコアの計算を統一して、スコア、順位、統計を表
- グラフはスコアと正打率
- djangoを初めて使ったため、できるだけ簡素化した
