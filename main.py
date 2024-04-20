from selenium import webdriver
from selenium.webdriver.common.by import By
import os
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--lang=ja-JP')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=options)
driver.header_overrides = {
    'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8'
}

# driver.get('https://id.moneyforward.com/sign_in/email')
driver.get('https://moneyforward.com')

# ログインボタンをクリックする
# xpathでaタグのhref属性が/sign_inの要素を取得して、clickメソッドでクリックする
driver.find_element(By.XPATH, '//a[@href="/sign_in"]').click()

driver.implicitly_wait(3)

# メールアドレスでログインボタンをクリックする
# xpathでaタグのhref属性に/sign_in/emailが含まれる要素を取得して、clickメソッドでクリックする
driver.find_element(By.XPATH, '//a[contains(@href,"/sign_in/email")]').click()

driver.implicitly_wait(3)


# メールアドレスを入力する
# xpathでinputタグのname属性がmfid_user[email]の要素を取得して、send_keysメソッドでメールアドレスを入力する
driver.find_element(By.XPATH, '//input[@name="mfid_user[email]"]')\
    .send_keys(os.environ['MFID_USER_EMAIL'])

# 同意してログインボタンをクリックする
# xpathでinputタグのvalue属性が同意してログインするの要素を取得して、clickメソッドでクリックする
driver.find_element(By.XPATH, '//input[@value="Agree and sign in"]').click()

# パスワードのテキストボックスが表示されるまで待機する
driver.implicitly_wait(3)

# パスワードを入力する
# xpathでinputタグのname属性がmfid_user[password]の要素を取得して、send_keysメソッドでパスワードを入力する
driver.find_element(By.XPATH, '//input[@name="mfid_user[password]"]')\
    .send_keys(os.environ['MFID_USER_PASSWORD'])

# ログインするボタンをクリックする
# xpathでinputタグのvalue属性がログインするの要素を取得して、clickメソッドでクリックする
driver.find_element(By.XPATH, '//input[@value="Sign in"]').click()
driver.implicitly_wait(3)

# 「ログインしました」というpタグが表示されればログイン成功
# xpathでpタグのテキストがログインしましたの要素を取得して、textメソッドでテキストを取得する
# print(driver.find_element(By.XPATH, '//p[contains(text(),"ログインしました。")]').text)

# マネーフォワードのトップページにアクセスする
# aタグのhref属性がhttps://moneyforward.com/sign_in/の要素を取得して、clickメソッドでクリックする
# driver.find_element(By.XPATH, '//a[@href="https://moneyforward.com/sign_in/"]').click()
# driver.get('https://id.moneyforward.com/account_selector')

# driver.implicitly_wait(3)

# 「このアカウントを使用する」ボタンをクリックする
# xpathでinputタグのvalue属性がこのアカウントを使用するの要素を取得して、clickメソッドでクリックする
# driver.find_element(By.XPATH, '//input[@value="このアカウントを使用する"]').click()

# 確認のためにページをローカルに保存する
with open('moneyforward.html', 'w') as f:
    f.write(driver.page_source)


# 総資産額を取得する
total = driver.find_element(By.XPATH, '//*[@id="user-info"]/section/div[1]').text
print(total)
