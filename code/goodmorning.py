from PIL import Image, ImageFont, ImageDraw
import requests
import json
import re
import datetime
import locale
import tweepy
import io

locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
dt_now = datetime.datetime.now()

#取得したい県のページを拾ってくる
response = requests.get("http://www.jma.go.jp/jp/yoho/327.html")

#バイバイ、改行
source = re.sub('\n', '', response.text)

#正規表現を用いて東部の明日の天気の部分だけを適宜抜き出す
source = (re.search(r'東部</div></th>[\s\S]*?>西部</div></th>', source)).group()
#source = re.sub('東部[\s\S]*?<th class="weather">\n明日', '', source)
#source = re.sub('明後日.*[\s\S]*?', '', source)
source = (re.search(r'今日[\s\S]*?明日', source)).group()

#天気アイコンのファイル名(番号)を取得
imgnum = re.sub('.png', '', (re.search(r'\d{3}\.png', source)).group())

#最高気温を正規表現を2重にかけて抽出
maxtemp = (re.search(r'\d{1,2}|-\d{1,2}', (re.search(r'<td class="max">.*</td>', source)).group())).group()

#午前午後の降水確率を正規表現を2重にかけて抽出、%を除去
rainam = ((re.search(r'\d{1,3}%', (re.search(r'<td align="left">06-12</td><td align="right">\d{1,2}%</td>', source)).group())).group()).replace('%', '')
rainpm = ((re.search(r'\d{1,3}%', (re.search(r'<td align="left">12-18</td><td align="right">\d{1,2}%</td>', source)).group())).group()).replace('%', '')

#事前に準備したJSONファイルの読み取り、辞書化
with open('../assets/weathername.json', 'r') as f:
    weatherdic = json.loads(f.read())
#ファイル番号から天気状態を取得
weather = weatherdic[imgnum]


#-----
#ここから画像
#-----

def center_text(img, font, text, color, x, y):
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(text, font)
    position = ((img.width - text_width) / 2 + x, y)
    draw.text(position, text, color, font = font)
    return img



if 'のち' in weather or '時々' in weather:

    #左側天気を取得
    if '晴れ' == weather[:2]:
        left_icon_img = Image.open('assets/icons/sunny.png').convert('RGBA')
        bg = Image.open('assets/backgrounds/bg_sunny.png').convert('RGBA')
    elif '曇り' == weather[:2]:
        left_icon_img = Image.open('assets/icons/cloudy.png').convert('RGBA')
        bg = Image.open('assets/backgrounds/bg_cloudy.png').convert('RGBA')
    elif '雨' == weather[:1]:
        left_icon_img = Image.open('assets/icons/rainy.png').convert('RGBA')
        bg = Image.open('assets/backgrounds/bg_rainy.png').convert('RGBA')
    elif '雪' == weather[:1]:
        left_icon_img = Image.open('assets/icons/snowy.png').convert('RGBA')
        bg = Image.open('assets/backgrounds/bg_snowy.png').convert('RGBA')
    
    #右側天気を取得
    if '晴れ' == weather[-2:]:
        right_icon_img = Image.open('assets/icons/sunny.png').convert('RGBA')
    elif '曇り' == weather[-2:]:
        right_icon_img = Image.open('assets/icons/cloudy.png').convert('RGBA')
    elif '雨' == weather[-1:]:
        right_icon_img = Image.open('assets/icons/rainy.png').convert('RGBA')
    elif '雪' == weather[-1:]:
        right_icon_img = Image.open('assets/icons/snowy.png').convert('RGBA')

    #フラグを設定
    if 'のち' in weather:
        #矢印マークを取得
        arrow_icon_img = Image.open('assets/icons/arrow.png').convert('RGBA')
        weather_flag = 'のち'
    elif '時々' in weather:
        weather_flag = '時々'
    
else:

    #天気を取得
    if '晴れ' == weather[:2]:
        left_icon_img = Image.open('assets/icons/sunny.png').convert('RGBA')
        bg = Image.open('assets/backgrounds/bg_sunny.png').convert('RGBA')
    elif '曇り' == weather[:2]:
        left_icon_img = Image.open('assets/icons/cloudy.png').convert('RGBA')
        bg = Image.open('assets/backgrounds/bg_cloudy.png').convert('RGBA')
    elif '雨' in weather:
        left_icon_img = Image.open('assets/icons/iconsrainy.png').convert('RGBA')
        bg = Image.open('assets/backgrounds/bg_rainy.png').convert('RGBA')
    elif '雪' in weather:
        left_icon_img = Image.open('assets/icons/snowy.png').convert('RGBA')
        bg = Image.open('assets/backgrounds/bg_snowy.png').convert('RGBA')
    
    #フラグを設定
    weather_flag = '通常'

gradation = Image.open('assets/backgrounds/gradation.png').convert('RGBA')
bg = Image.alpha_composite(bg, gradation)

# --------------------------
# アイコンの中心のX座標: 484
# アイコンの中心のX座標: 398
# 最高気温の中心のX座標: 236
# --------------------------
if weather_flag == 'のち':

    #レイヤーの新規設定
    left_icon_layor = Image.new('RGBA', bg.size, (255, 255, 255, 0))
    right_icon_layor = Image.new('RGBA', bg.size, (255, 255, 255, 0))
    arrow_icon_layor = Image.new('RGBA', bg.size, (255, 255, 255, 0))

    #アイコンのリサイズ
    left_icon_img = left_icon_img.resize((96, 96))
    right_icon_img = right_icon_img.resize((96, 96))
    arrow_icon_img = arrow_icon_img.resize((72, 72))

    #アイコンのペースト
    left_icon_layor.paste(left_icon_img, (388, 340))
    right_icon_layor.paste(right_icon_img, (484, 340))
    arrow_icon_layor.paste(arrow_icon_img, (448, 390))

    #合成
    bg = Image.alpha_composite(bg, left_icon_layor)
    bg = Image.alpha_composite(bg, right_icon_layor)
    bg = Image.alpha_composite(bg, arrow_icon_layor)

# --------------------------
# アイコンの中心のX座標: 484
# アイコンの中心のY座標: 398
# 最高気温の中心のX座標: 236
# --------------------------
if weather_flag == '時々':

    #レイヤーの新規設定
    left_icon_layor = Image.new('RGBA', bg.size, (255, 255, 255, 0))
    right_icon_layor = Image.new('RGBA', bg.size, (255, 255, 255, 0))

    #アイコンのリサイズ
    right_icon_img = right_icon_img.resize((72, 72))
    left_icon_img = left_icon_img.resize((150, 150))
    
    #アイコンのペースト
    right_icon_layor.paste(right_icon_img, (508, 370))
    left_icon_layor.paste(left_icon_img, (388, 323))

    #合成
    bg = Image.alpha_composite(bg, right_icon_layor)
    bg = Image.alpha_composite(bg, left_icon_layor)

if weather_flag == '通常':

    #レイヤーの新規設定
    left_icon_layor = Image.new('RGBA', bg.size, (255, 255, 255, 0))

    #アイコンのリサイズ
    left_icon_img = left_icon_img.resize((150, 150))
    
    #アイコンのペースト
    left_icon_layor.paste(left_icon_img, (411, 323))

    #合成
    bg = Image.alpha_composite(bg, left_icon_layor)


#日付情報
font_size = 40
font = ImageFont.truetype('assets/fonts/medium.ttf', font_size)
disp_date = Image.new('RGBA', bg.size, (255, 255, 255, 0))
day_list = ['月', '火', '水', '木', '金', '土', '日', '月']
message = (str)(dt_now.month) + '月' + (str)(dt_now.day) + '日(' + day_list[dt_now.weekday()] + ') の天気'
disp_date = center_text(disp_date, font, message, (255, 255, 255), 0, 200)
bg = Image.alpha_composite(bg, disp_date)

#最高気温
font_size = 140
font = ImageFont.truetype('assets/fonts/light.ttf', font_size)
disp_temp = Image.new('RGBA', bg.size, (255, 255, 255, 0))
message = maxtemp + '°'
disp_temp = center_text(disp_temp, font, message, (255, 255, 255), -124, 295)
bg = Image.alpha_composite(bg, disp_temp)

#天気名
font_size = 40
font = ImageFont.truetype('assets/fonts/normal.ttf', font_size)
disp_weather = Image.new('RGBA', bg.size, (255, 255, 255, 0))
disp_weather = center_text(disp_weather, font, weather, (255, 255, 255), 0, 700)
bg = Image.alpha_composite(bg, disp_weather)

#降水確率
font_size = 30
font = ImageFont.truetype('assets/fonts/medium.ttf', font_size)
disp_rain = Image.new('RGBA', bg.size, (255, 255, 255, 0))
message = '降水確率'
disp_rain = center_text(disp_rain, font, message, (255, 255, 255), 0, 820)
bg = Image.alpha_composite(bg, disp_rain)
font_size = 40
font = ImageFont.truetype('assets/fonts/medium.ttf', font_size)
disp_rain = Image.new('RGBA', bg.size, (255, 255, 255, 0))
message = rainam + '% / ' + rainpm + '%'
disp_rain = center_text(disp_rain, font, message, (255, 255, 255), 0, 855)
bg = Image.alpha_composite(bg, disp_rain)

result = io.BytesIO()
bg.save(result, "PNG")

