import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def open_pages(driver):
    # setting webpage
    driver.get('https://navi.cnki.net/knavi/degreeunits/GDLLU/detail?uniplatform=NZKPT')#选择对应的学校论文库的网址
    time.sleep(1)
    WebDriverWait(driver, 100 ).until(EC.presence_of_element_located( (By.XPATH ,"/html/body/div[2]/div[2]/dl/dt/div/a[2]") ) ).click()
    time.sleep(1)
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[1]/select/option[6]"))).click()

def start_search(driver,final_list):
    for word in final_list:
        try:
            print(word)
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="J_searchTxt"]'''))).clear()
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="J_searchTxt"]'''))).send_keys(word)
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/a"))).click()
            title_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "nobreak")))
            time.sleep(2)
            if len(title_list) > 1:
                for i in range(1, len(title_list)):
                    author_xpath = f"/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr[{i}]/td[4]"
                    teacher_xpath = f"/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr[{i}]/td[5]"
                    year_xpath = f"/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr[{i}]/td[6]"
                    kreader_xpath = f"/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr[{i}]/td[3]/ul/li[2]/a"
                    author = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, author_xpath))).text
                    teacher = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, teacher_xpath))).text
                    year = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, year_xpath))).text
                    kreader = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, kreader_xpath))).get_attribute('href')
                    res = f"{author}\t{teacher}\t{year}\t{kreader}".replace("\n", "") + "\n"
                    print(res)
                    #要输出的tsv文件，更改‘’单引号间的名字
                    with open(f'CNKI_{"second"}.tsv', 'a', encoding='gbk') as f:
                        f.write(res)
            else:
                author_xpath = f"/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr/td[4]"
                teacher_xpath = f"/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr/td[5]"
                year_xpath = f"/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr/td[6]"
                kreader_xpath = f"/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div/table/tbody/tr/td[3]/ul/li[2]/a"
                author = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, author_xpath))).text
                teacher = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, teacher_xpath))).text
                year = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, year_xpath))).text
                kreader = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, kreader_xpath))).get_attribute('href')
                res = f"{author}\t{teacher}\t{year}\t{kreader}".replace("\n", "") + "\n"
                print(res)
                with open(f'CNKI_{"second"}.tsv', 'a', encoding='gbk') as f:
                    f.write(res)
        except:
            none = "未找到"
            res = f"{word}\t{none}".replace("\n", "") + "\n"
            with open(f'CNKI_{"second"}.tsv', 'a', encoding='gbk') as f:
                f.write(res)
        continue

def main():
    #get直接返回，不再等待界面加载完成
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"

    # 设置谷歌驱动器的环境
    options = webdriver.ChromeOptions()
    # 设置chrome不加载图片，提高速度
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # 设置不显示窗口
    options.add_argument('--headless')
    # 创建一个谷歌驱动器
    driver = webdriver.Chrome(options=options)
    # 读入待搜索名单
    file= open('D:\测试\second.csv', 'r')
    content = file.read()
    final_list = list()
    rows = content.split('\n')
    # 名单转换成list
    for row in rows:
        final_list.append(row.split(','))
    # 开始查询
    open_pages(driver)
    start_search(driver, final_list)

    # 关闭浏览器
    driver.close()

main()

