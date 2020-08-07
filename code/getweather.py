from PIL import Image, ImageFont, ImageDraw
import requests
import json
import re
import datetime
import locale

locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
dt_now = datetime.datetime.now()

#取得したい県のページを拾ってくる
response = requests.get("http://www.jma.go.jp/jp/yoho/327.html")

#バイバイ、改行
source = re.sub('\n', '', response.text)

if dt_now.hour == 7:
    source = (re.search(r'東部</div></th>[\s\S]*?>西部</div></th>', source)).group()
    source = (re.search(r'今日[\s\S]*?明日', source)).group()
elif dt_now.hour == 22:
    source = (re.search(r'東部</div></th>[\s\S]*?>西部</div></th>', source)).group()
    source = (re.search(r'明日[\s\S]*?明後日', source)).group()

#天気アイコンのファイル名(番号)を取得
imgnum = re.sub('.png', '', (re.search(r'\d{3}\.png', source)).group())

#最高気温を正規表現を2重にかけて抽出
maxtemp = (re.search(r'\d{1,2}|-\d{1,2}', (re.search(r'<td class="max">.*</td>', source)).group())).group()

#午前午後の降水確率を正規表現を2重にかけて抽出、%を除去
if dt_now.hour == 7:
    rainam = ((re.search(r'\d{1,3}%', (re.search(r'<td align="left">06-12</td><td align="right">\d{1,2}%</td>', source)).group())).group()).replace('%', '')
    rainpm = ((re.search(r'\d{1,3}%', (re.search(r'<td align="left">12-18</td><td align="right">\d{1,2}%</td>', source)).group())).group()).replace('%', '')
if dt_now.hour == 22:
    rainam = ((re.search(r'\d{1,3}%', (re.search(r'<td align="left" nowrap>06-12</td><td align="right">\d{1,2}%</td>', source)).group())).group()).replace('%', '')
    rainpm = ((re.search(r'\d{1,3}%', (re.search(r'<td align="left" nowrap>12-18</td><td align="right">\d{1,2}%</td>', source)).group())).group()).replace('%', '')

#事前に準備したJSONファイルの読み取り、辞書化
with open('../assets/weathername.json', 'r') as f:
    weatherdic = json.loads(f.read())
#ファイル番号から天気状態を取得
weather = weatherdic[imgnum]


if dt_now.hour == 7:
    print('【静岡県東部の今日の天気】\n' + weather + '\n\n最高気温: ' + maxtemp + '℃\n\n降水確率\n午前: ' + rainam + '%\n午後: ' + rainpm + '%')
if dt_now.hour == 22:
    print('【静岡県東部の明日の天気】\n' + weather + '\n\n最高気温: ' + maxtemp + '℃\n\n降水確率\n午前: ' + rainam + '%\n午後: ' + rainpm + '%')