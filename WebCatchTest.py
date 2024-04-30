from selenium import webdriver
from bs4 import BeautifulSoup
import time

def get_element_by_js_path(driver, js_path):
    """
    使用JavaScript执行DOM查询，返回查询到的元素。
    """
    return driver.execute_script(f"return document.querySelector('{js_path}')")

def extract_div_text(url, delay_seconds=0.5):
    """
    使用Selenium打开网页，执行JavaScript定位指定div，然后使用BeautifulSoup提取文本。
    """
    # option = webdriver.EdgeOptions()
    # option.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    # driver = webdriver.Edge(option)
    #driver = webdriver.Chrome()
    driver = webdriver.Edge()
    try:
        driver.get(url)
        # term = eval(get_element_by_js_path(driver, js_path_term))
        for i in range(1, 31):  # 循环30次获取当前的开奖结果
            j = 1
            # print("第" + str(term-i) + "期开奖号码：" + "最近第" + str(i) +"期")
            for _ in range(6):  # 循环6次获取当前红球的号码
                target_div = get_element_by_js_path(driver, js_path.format(i, j))
                soup = BeautifulSoup(target_div.get_attribute('outerHTML'), 'html.parser')
                div_text = soup.get_text(strip=True)

                print(f"红球（第{_ + 1}次获取）：{div_text}")

                time.sleep(delay_seconds)  # 延迟一段时间，确保页面有足够时间更新
                j = j + 1
            #获取蓝球号码
            target_div_blue = get_element_by_js_path(driver, js_path_blue.format(i))
            soup_blue = BeautifulSoup(target_div_blue.get_attribute('outerHTML'), 'html.parser')
            div_text_blue = soup_blue.get_text(strip=True)
            print(f"蓝球：{div_text_blue}")
            time.sleep(delay_seconds)

    finally:
        driver.quit()

if __name__ == '__main__':
    url = 'https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/'
    #最近一期第一个红球的js路径：body > div.main > div > div > div.ygkj_wqkjgg > div > div.body-content-item > div.table.ssq > table > tbody > tr:nth-child(1) > td:nth-child(3) > div > div:nth-child(1)
    #第二期的第一个红球的JS路径：body > div.main > div > div > div.ygkj_wqkjgg > div > div.body-content-item > div.table.ssq > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div:nth-child(1)
    #最近第一期的蓝球的JS路径： body > div.main > div > div > div.ygkj_wqkjgg > div > div.body-content-item > div.table.ssq > table > tbody > tr:nth-child(1) > td:nth-child(3) > div > div.qiu-item.qiu-item-small.qiu-item-wqgg-zjhm-blue
    # js_path_term = "body > div.main > div > div > div.ygkj_wqkjgg > div > div.body-content-item > div.table.ssq > table > tbody > tr:nth-child(1) > td:nth-child(1)"
    js_path = "body > div.main > div > div > div.ygkj_wqkjgg > div > div.body-content-item > div.table.ssq > table > tbody > tr:nth-child({}) > td:nth-child(3) > div > div:nth-child({})"
    js_path_blue = "body > div.main > div > div > div.ygkj_wqkjgg > div > div.body-content-item > div.table.ssq > table > tbody > tr:nth-child({}) > td:nth-child(3) > div > div.qiu-item.qiu-item-small.qiu-item-wqgg-zjhm-blue"
    extract_div_text(url)
    exit(0)
