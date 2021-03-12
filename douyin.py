from appium import webdriver
import time

# 初始化配置，设置Desired Capabilities参数
desired_caps = {
    'platformName': 'Android',
    'deviceName': 'MI 9',
    'appPackage': 'com.ss.android.ugc.aweme',
    'appActivity': '.main.MainActivity'
}

# desired_caps = {
#     "platformName": "Android",
#     "platformVersion": "7.1.2",
#     "deviceName": "MI 9",
#     "appPackage": "cmccwm.mobilemusic",
#     "appActivity": ".ui.base.MainActivity"
# }
# 指定Appium Server
server = 'http://localhost:4723/wd/hub'
# 新建一个driver
driver = webdriver.Remote(server, desired_caps)
# 获取模拟器/手机的分辨率(px)
size = driver.get_window_size()
print('width:', size)
width = size['width']
height = size['height']
print(width, height)

print('sleep 10s')
time.sleep(10)
print("start click")
# 点击同意
driver.find_element_by_id('b6l').click()

time.sleep(5)
print('点击同意抖音拨打电话')
# 点击同意抖音拨打电话
# a = driver.find_element_by_id('permission_allow_button')
a = driver.find_element_by_xpath(
    '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button')
print("我要点了")
print(a.id, a.text)
a.click()

time.sleep(5)
print('点击同意抖音获取地理位置')
# 点击同意抖音获取地理位置
# b = driver.find_element_by_id('permission_allow_button').click()
b = driver.find_element_by_xpath(
    '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button[1]')
b.click()

start_x = width // 2  # 滑动的起始点的x坐标，屏幕宽度中心点
start_y = height // 3 * 2  # 滑动的起始点的y坐标，屏幕高度从上开始到下三分之二处
distance = height // 2  # y轴滑动距离：屏幕高度一半的距离
end_x = start_x  # 滑动的终点的x坐标
end_y = start_y - distance  # 滑动的终点的y坐标
# 滑动
driver.swipe(start_x, start_y, end_x, end_y)

# 滑动
for i in range(100):
    time.sleep(2)
    print("滑动第%d个视频" % i)
    driver.swipe(start_x, start_y, end_x, end_y)
