import epaper
from PIL import Image,ImageDraw,ImageFont
import datetime
import os

epd2in7 = epaper.epaper('epd2in7')

history_dir = './history/'
# 前日の総資産額を読み込む
# param: today_date_str 今日の日付(YYYYMMDD)
def read_yesterday_total_assets(today_date_str) -> int:
    # 前日の日付を取得
    yesterday_date_str = (datetime.datetime.strptime(today_date_str, '%Y%m%d') - datetime.timedelta(days=1)).strftime('%Y%m%d')
    with open(os.path.join(history_dir, '{}.txt'.format(yesterday_date_str)), 'r') as f:
        return int(f.readline())

def display_on_epaper(total_assets: int, yesterday_total_assets: int):
    epd = epd2in7.EPD()
    epd.init()
    # 電子ペーパーの表示をクリア
    epd.Clear()

    # フォントの設定
    font24 = ImageFont.truetype('/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf', 24)
    font16 = ImageFont.truetype('/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf', 16)
    font12 = ImageFont.truetype('/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf', 12)

    # 画像の作成
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    # 総資産額3桁区切りにする
    formated_total_assets = '{:,}'.format(total_assets)
    total_assets_text = formated_total_assets + ' 円'

    # 差額を計算
    diff_total_assets = total_assets - yesterday_total_assets
    diff_total_assets_text = '{:,}'.format(diff_total_assets) + ' 円'
    # 差額がプラスの場合は+を付ける
    if diff_total_assets >= 0:
        diff_total_assets_text = '+' + diff_total_assets_text
    else:
        diff_total_assets_text = diff_total_assets_text

    # 前日比のパーセンテージを計算
    # 前日の総資産額が0の場合は'-'を設定
    if yesterday_total_assets != 0:
        diff_percentage = diff_total_assets / yesterday_total_assets * 100
        diff_percentage_text = '{:.2f}'.format(diff_percentage) + '%'

        # 前日比がプラスの場合は+を付ける
        if diff_total_assets >= 0:
            diff_percentage_text = '+' + diff_percentage_text
        else:
            diff_percentage_text = diff_percentage_text
    else:
        diff_percentage_text = '-'

    # 上部右側にYYYY年M月D日（曜日）形式で日付を表示
    today_date = datetime.datetime.today()
    today_date_text = today_date.strftime('%Y年%-m月%-d日(%a)')
    today_date_text_width, today_date_text_height = draw.textsize(today_date_text, font=font12)
    draw.text((epd.height - today_date_text_width, 0), today_date_text, font=font12, fill=0)



    # 中央に総資産額を表示
    total_assets_text_width, total_assets_text_height = draw.textsize(total_assets_text, font=font24)
    draw.text(((epd.height - total_assets_text_width)/2,(epd.width - total_assets_text_height)/2), total_assets_text, font=font24, fill=0)

    # 総資産額の下に右揃えで前日比を「前日差額（前日比のパーセンテージ）」の形式で表示
    yesterday_text = '{}({})'.format(diff_total_assets_text,diff_percentage_text)
    diff_total_assets_text_width, diff_total_assets_text_height = draw.textsize(yesterday_text, font=font16)
    draw.text(((epd.height - diff_total_assets_text_width)/2, (epd.width - total_assets_text_height)/2 + total_assets_text_height), yesterday_text,font=font16, fill=0)



    # 画像を電子ペーパーに描画
    epd.display(epd.getbuffer(image))

if __name__ == '__main__':
    # 動作確認用
    yesterday_total_assets = 0
    try:
        yesterday_total_assets = read_yesterday_total_assets('20210101')
    except FileNotFoundError as e:
        print('昨日の総資産額のファイルが存在しませんでした。')
        print(e)
        # ファイルが存在しない場合は0を設定
        yesterday_total_assets = 0

    display_on_epaper(300000, yesterday_total_assets)
