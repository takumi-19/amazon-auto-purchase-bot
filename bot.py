from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

CHROMEDRIVER = "/opt/chrome/chromedriver"
URL = "https://www.amazon.co.jp"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

chrome_service = fs.Service(executable_path=CHROMEDRIVER)
# ドライバの起動
driver = webdriver.Chrome(service=chrome_service, options=options)
# 要素検索時のデフォルト待機時間(最大)
driver.implicitly_wait(0.5)
# 明示的な待機時間(最大)
wait = WebDriverWait(driver, 5)

# ===========================================
# 設定する項目
# ===========================================
# Amazonのログイン用メールアドレス
email = "takumi.uyama19@icloud.com"
# Amazonのログイン用パスワード
password = "432wer54"
# 商品ページのURL
purchaseUrl = "https://www.amazon.co.jp/gp/offer-listing/B0BFPL66LS/ref=dp_olp_unknown_mbc"
listPriceLow = "4,078"
listPriceHigh = "4,752"

# ===========================================
# ログイン処理
# ===========================================
# Amazonにアクセス
driver.get(URL)
# ログインボタンの要素を取得
loggingButton = driver.find_element(by=By.CSS_SELECTOR, value=".a-button-inner > a")
# ログインボタンのhref値を取得
loginHref = loggingButton.get_attribute("href")

# ログイン画面にアクセス
driver.get(loginHref)
# メールアドレスを入力
driver.find_element(by=By.ID, value="ap_email").send_keys(email)
# 「次に進む」ボタンをクリック
wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
# パスワードを入力
driver.find_element(by=By.ID, value="ap_password").send_keys(password)
# ログインボタンをクリック
wait.until(EC.element_to_be_clickable((By.ID, "signInSubmit"))).click()

# 電話番号の確認が出た場合「スキップ」をクリック
try :
    driver.find_element(by=By.ID, value="ap-account-fixup-phone-skip-link").click()
except :
    pass

# ===========================================
# 商品の監視
# ===========================================
# 商品ページにアクセス
driver.get(purchaseUrl)

# 監視処理のループ
price = driver.find_elements(by=By.CSS_SELECTOR, value="div#aod-price-1 span.a-price-whole")[0].text
while True:
    try:
        if price >= listPriceLow and price <= listPriceHigh and driver.find_element(By.ID, value='a-autoid-2-offer-1'):
            break
        # なければ例外処理へ進む
        else:
            raise Exception
    except:
        # 入荷なし、もしくは何らかのエラーが発生した場合
        # 3秒待機して商品ページに移動
        sleep(3)
        driver.get(purchaseUrl)

# ===========================================
# 購入処理
# ===========================================
# 「カートに追加する」ボタンが表示されるまで待機してクリック
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span#a-autoid-2-offer-1 input[name="submit.addToCart"]'))).click()
# 「数量」ボタンが表示されるまで待機
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span#aod-offer-qty-button-1-announce')))
# カートページのURL
cartUrl = 'https://www.amazon.co.jp/gp/cart/view.html?ref_=nav_cart'
# カートページにアクセス
driver.get(cartUrl)
# 「レジに進む」をクリック
driver.find_element(by=By.NAME, value='proceedToRetailCheckout').click()
# 「注文を確定」をクリック
driver.find_element(by=By.NAME, value='placeYourOrder1').click()

print("処理を完了しました！")

# ブラウザの終了
driver.quit()
