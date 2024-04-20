from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
import os
import re
import logging
from typing import List
import json
from display import display_on_epaper, read_yesterday_total_assets
import datetime
import time

# ログのレベルは環境変数LOG_LEVELに設定があればその値を、なければINFOを設定
log_level = os.environ.get('LOG_LEVEL', 'INFO')
# ログの出力先を標準出力に設定
logging.basicConfig(level=log_level, format='[%(asctime)s][%(levelname)s]%(message)s')


def fetch() -> str:
    # Chromeを起動してマネーフォワードのログインページにアクセス
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--lang=ja-JP')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    chrome_service = service.Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(options=options, service=chrome_service)
    driver.header_overrides = {
        'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8'
    }

    driver.implicitly_wait(10)

    #driver.get('https://id.moneyforward.com/sign_in')
    driver.get('https://moneyforward.com/login')

    # ログインボタンをクリックする
    #driver.find_element(By.XPATH, '//*[@id="before-login-corporate"]/header/div[1]/div[2]/nav/ul/li[1]/p').click()

    # xpathでaタグのhref属性が/sign_inの要素を取得して、clickメソッドでクリックする
    #driver.find_element(By.XPATH, '//a[@href="/sign_in"]').click()
    #driver.find_element(By.XPATH, '//*[@id="side-menu-container"]/div[1]/div/div[1]/a').click()

    #time.sleep(3)

    # メールアドレスでログインボタンをクリックする
    # xpathでaタグのhref属性に/sign_in/emailが含まれる要素を取得して、clickメソッドでクリックする
    #driver.find_element(By.XPATH, '//a[contains(@href,"/sign_in/email")]').click()

    #time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="login"]/div/div/div[3]/a').click()
    time.sleep(3)

    # メールアドレスを入力する
    # xpathでinputタグのname属性がmfid_user[email]の要素を取得して、send_keysメソッドでメールアドレスを入力する
    driver.find_element(By.XPATH, '//input[@name="mfid_user[email]"]')\
        .send_keys(os.environ['MFID_USER_EMAIL'])

    # 同意してログインボタンをクリックする
    # xpathでinputタグのvalue属性が同意してログインするの要素を取得して、clickメソッドでクリックする
    driver.find_element(By.XPATH, '//button[@id="submitto"]').click()

    # パスワードを入力する
    # xpathでinputタグのname属性がmfid_user[password]の要素を取得して、send_keysメソッドでパスワードを入力する
    driver.find_element(By.XPATH, '//input[@name="mfid_user[password]"]')\
        .send_keys(os.environ['MFID_USER_PASSWORD'])

    # ログインするボタンをクリックする
    # xpathでinputタグのvalue属性がログインするの要素を取得して、clickメソッドでクリックする
    driver.find_element(By.XPATH, '//button[@id="submitto"]').click()

    time.sleep(3)

    # 総資産額を取得する
    total = driver.find_element(By.XPATH, '//*[@id="user-info"]/section/div[1]').text
    logging.info(total)

    # 数字以外の文字を削除する
    total = re.sub(r'\D', '', total)

    return total


if __name__ == '__main__':
    sleep_seconds = 3600
    while True:
        # フェッチ前の時間を取得する
        before_fetch = datetime.datetime.now()
        total_assets = fetch()
        # フェッチ後の時間を取得する
        after_fetch = datetime.datetime.now()

        today = datetime.date.today().strftime('%Y%m%d')
        # 日付のファイル名で総資産額を保存する
        # すでにファイルが存在する場合は上書きする
        with open(f'./history/{today}.txt', 'w') as f:
            f.write(total_assets)

        # 昨日の総資産額を取得する
        yesterday_total_assets = 0
        try:
            yesterday_total_assets = read_yesterday_total_assets(today)
        except FileNotFoundError:
            logging.warning('昨日の総資産額が存在しません、0を設定します')

        # 表示処理を呼び出す
        display_on_epaper(int(total_assets), int(yesterday_total_assets))

        # フェッチ後の時間からフェッチ前の時間を引いて、スリープする秒数を計算する
        sleep_seconds = sleep_seconds - (after_fetch - before_fetch).seconds

        # スリープする
        logging.info(f'sleep {sleep_seconds} seconds')
        time.sleep(sleep_seconds)
