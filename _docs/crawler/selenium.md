---
title: selenium
description: selenium
---

# selenium

```py
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def main():
    # 打开浏览器(无界面)
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    
    # 打开浏览器(有界面)
    browser = webdriver.Chrome()

    # 访问网址
    browser.get('https://www.baidu.com')

    # 按ID取节点
    input = browser.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    
    # 显式等待：满足条件即返回
    wait = WebDriverWait(browser, timeout=10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))

    # 增删cookies
    browser.delete_all_cookies()
    browser.add_cookie({'name': 'name', 'domain': 'www.baidu.com', 'value': 'tom'})

    # 当前页面信息
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)

    # 按class_name取节点
    soutu_btn = browser.find_element_by_class_name('soutu-btn')
    soutu_btn.click()

    # 按xpath取节点
    logo = browser.find_element_by_xpath('//*[@id="result_logo"]/img[2]')
    
    # 按css_selector取节点：当class包含空格时，可用css_selector取节点
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='soutu-icon soutu-drop-icon']")))
    soutu_drop_icon = browser.find_element_by_css_selector("[class='soutu-icon soutu-drop-icon']")
    print(logo, soutu_drop_icon)


    input = browser.find_element_by_id('soutu-url-kw')

    # 好像不生效？？？
    actions = ActionChains(browser)
    # actions.drag_and_drop(source=logo, target=soutu_drop_icon)
    actions.drag_and_drop(source=logo, target=input)
    # actions.move_to_element(logo)
    # actions.click_and_hold(logo)
    # actions.move_to_element(input)
    # actions.release(input)
    actions.perform()

    # 滚动事件
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    # browser.execute_script('alert("Hello")')

    time.sleep(3)

    # 页面回退与前进
    browser.back()
    time.sleep(1)
    browser.forward()

    # 异常处理
    try:
        browser.find_element_by_id('xxxyyy')
    except NoSuchElementException:
        print('No such element.')

    time.sleep(5)

    # 关闭浏览器，另外，程序退出也会自动关闭
    browser.close()

if __name__ == '__main__':
    main()
```