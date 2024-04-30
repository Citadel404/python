from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys
import pandas as pd


def get_element_by_js_path(driver, js_path):
    """
    使用JavaScript执行DOM查询，返回查询到的元素。
    """
    return driver.execute_script(f"return document.querySelector('{js_path}')")

def extract_div_text(url, delay_seconds=0.05):
    """
    使用Selenium打开网页，执行JavaScript定位指定div，然后使用BeautifulSoup提取文本。
    """
    # option = webdriver.EdgeOptions()
    # option.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    # driver = webdriver.Edge(option)
    #driver = webdriver.Chrome()
    global frame
    driver = webdriver.Edge()

    try:
        print("开始获取数据...")
        driver.get(url)
        data = {'   双色球期数': [],#初始化DataFrame
                '红1': [], '红2': [],
                '红3': [], '红4': [],
                '红5': [], '红6': [],
                '蓝球': []}
        frame = pd.DataFrame(data)
        for i in range(1, 31):  # 循环30次获取当前的开奖结果
            j = 1
            red = []#初始化双色球的列表
            blue = []
            # print("第" + str(2024041-i) + "期开奖号码：" + "最近第" + str(i) +"期")
            for _ in range(6):  # 循环6次获取当前红球的号码
                target_div = get_element_by_js_path(driver, js_path.format(i, j))
                soup = BeautifulSoup(target_div.get_attribute('outerHTML'), 'html.parser')
                div_text = soup.get_text(strip=True)
                red.append(eval("{}".format(div_text)))#将获取到的红球号码添加到列表中
                #print(red)#测试列表获取信息
                #print(f"红球（第{_ + 1}次获取）：{div_text}")
                time.sleep(delay_seconds)  # 延迟一段时间，确保页面有足够时间更新
                j = j + 1
            #获取蓝球号码
            target_div_blue = get_element_by_js_path(driver, js_path_blue.format(i))
            soup_blue = BeautifulSoup(target_div_blue.get_attribute('outerHTML'), 'html.parser')
            div_text_blue = soup_blue.get_text(strip=True)
            blue.append(eval("{}".format(div_text_blue)))#将获取到的蓝球号码添加到列表中
            # print(f"蓝球：{div_text_blue}")
            time.sleep(delay_seconds)
            #在dataframe中添加一行数据
            frame.loc[len(frame)] = [2024041-i, red[0], red[1], red[2], red[3], red[4], red[5], blue[0]]
        progress_bar()
        print()
    except:
        print("程序出现异常，请检查网络连接或重新运行程序")
        exit(1)
    finally:
        driver.quit()
        #设置输出对齐
        pd.set_option('display.unicode.east_asian_width', True)
        print(frame)#输出dataframe到console
        try:
            frame.to_excel('双色球.xlsx', index=False)#将dataframe写入excel
        except:
            print("写入excel失败")
            exit(1)
        finally:
            print("写入excel成功")
def progress_bar():
    """
    进度条
    """
    for i in range(1,101):
        print("\r", end="")
        print("正在写入数据:{}%:".format(i),"-" * (i // 2), end="")
        sys.stdout.flush()
        time.sleep(0.05)

if __name__ == '__main__':
    url = 'https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/'
    #最近一期第一个红球的js路径：body > div.main > div > div > div.ygkj_wqkjgg > div > div.body-content-item > div.table.ssq > table > tbody > tr:nth-child(1) > td:nth-child(3) > div > div:nth-child(1)
    #第二期的第一个红球的JS路径：body > div.main > div > div > div.ygkj_wqkjgg > div > div.body-content-item > div.table.ssq > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div:nth-child(1)
    #最近第一期的蓝球的JS路径： body > div.main > div > div > div.ygkj_wqkjgg > div > div.body-content-item > div.table.ssq > table > tbody > tr:nth-child(1) > td:nth-child(3) > div > div.qiu-item.qiu-item-small.qiu-item-wqgg-zjhm-blue
    js_path = "body > div.main > div > div > div.ygkj_wqkjgg > div > div.body-content-item > div.table.ssq > table > " \
              "tbody > tr:nth-child({}) > td:nth-child(3) > div > div:nth-child({})"
    js_path_blue = "body > div.main > div > div > div.ygkj_wqkjgg > div > div.body-content-item > div.table.ssq > " \
                   "table > tbody > tr:nth-child({}) > td:nth-child(3) > div > " \
                   "div.qiu-item.qiu-item-small.qiu-item-wqgg-zjhm-blue"
    extract_div_text(url)
    exit(0)

