from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

tsv_path = 'suica.tsv'
driver_path = 'c:/driver/chromedriver.exe'
login_path = "https://ssnb.x.moneyforward.com/"
wallet_path = 'https://ssnb.x.moneyforward.com/accounts/show_manual/xxxxxx'
user_email = 'canada@example.com'

f = open(tsv_path, 'r')
tsv = csv.reader(f, delimiter = '\t')
f.close

options = webdriver.ChromeOptions()

# ログイン
driver = webdriver.Chrome(options=options, executable_path=driver_path)
driver.get(login_path)
driver.find_element_by_partial_link_text('ログイン').click()
driver.find_element_by_id('sign_in_session_service_email').send_keys(user_email)

# ホーム画面を待つ
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "home")))

# SuiCa用ページへ
driver.get(wallet_path)


for row in tsv:
    # 入金は記録しない
    if int(row[3]) > 0:
        continue

    WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.ID , "update-at")))
    driver.implicitly_wait(1)
    # 入力ボタンクリック
    driver.find_element_by_css_selector('.cf-new-btn > img').click()
    
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "updated-at")))
    driver.implicitly_wait(1)
    # 日付入力
    driver.execute_script('document.getElementById( "updated-at" ).value = "{}";'.format(row[0]))

    # 金額入力
    driver.find_element_by_id('appendedPrependedInput').send_keys(abs(int(row[3])))

    # '入'で始まっている場合は交通費（電車）として入力する
    if row[1][0] == '入':
        driver.execute_script('document.getElementById( "user_asset_act_large_category_id" ).value = "20";')
        driver.execute_script('document.getElementById( "user_asset_act_middle_category_id" ).value = "96";')
        
    # 摘要を入力する
    driver.find_element_by_id('js-content-field').send_keys(row[1])
    # Submitボタン押下
    driver.find_element_by_id('submit-button').click()

