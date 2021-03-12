from appium import webdriver
import time
# from load_xls import read_excel
from pykeyboard import PyKeyboard
import xlrd
import xlwt


# 启动appium
def android_driver():
    # 初始化配置，设置Desired Capabilities参数
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "7.1.2",
        "deviceName": "MI 9",
        "appPackage": "cmccwm.mobilemusic",
        "appActivity": ".ui.base.MainActivity"
    }
    # 指定Appium Server
    server = 'http://localhost:4723/wd/hub'
    # 新建一个driver
    driver = webdriver.Remote(server, desired_caps)
    driver.implicitly_wait(5)
    return driver


# 切换环境,change_list = ['*#testrs#*', '*#prs#*', '*#rs#*', '*#devrs#*'],输入：0：测试环境；1：预生产环境；2：生产环境；3：开发环境
def chage_env(driver, num):
    xianchang_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup[3]/android.widget.ImageView'
    yanchanghui_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.ImageView'
    # 查找‘现场’标签
    xianchang_tag = driver.find_element_by_xpath(xianchang_xpath)
    xianchang_tag.click()
    time.sleep(1)
    # 查找‘演唱会’标签
    yanchanghui_tag = driver.find_element_by_xpath(yanchanghui_xpath)
    yanchanghui_tag.click()
    time.sleep(1)
    # 查找‘搜索’标签
    driver.find_element_by_id('uikit_topbar_right_view').click()
    # 键入环境接环字符，回车
    change_list = ['*#testrs#*', '*#prs#*', '*#rs#*', '*#devrs#*']
    change_key = change_list[num]
    driver.find_element_by_id('edit_txt_search_bar_input').send_keys(change_key)
    print('start change env ...')
    '''
    # driver.keyevent(66)
    #driver.press_keycode(66)
    '''
    # 以上两个appium自带键入无法生效，用下方法实现回车
    k = PyKeyboard()
    time.sleep(1)
    k.tap_key(k.enter_key)
    print('end change env ...')
    # 退出当前应用，启动当前应用
    time.sleep(2)
    driver.close_app()

    time.sleep(5)
    driver.launch_app()
    return driver


# 读取excel数据
def read_excel():
    work_book = xlrd.open_workbook('./咪咕音乐效果测试.xls')
    sheet = work_book.sheet_by_name('test1')
    print('sheet_name:{},sheet_rows:{},sheet_cols:{}'.format(sheet.name, sheet.nrows, sheet.ncols))
    rows_num = sheet.nrows
    cols_num = sheet.ncols
    type_list = sheet.col_values(2)[1::]
    song_list = sheet.col_values(3)[1::]
    # print(type_list)
    # print(song_list)
    # 获取要查询的类型和查询串
    search_list = []
    for i in range(len(song_list)):
        search_list.append((type_list[i], song_list[i]))
    # print(search_list)

    # 第二种获取要查询的类型和查询串
    search_list1 = []
    for i in range(1, rows_num):
        search_list1.append((sheet.cell_value(i, 2), sheet.cell_value(i, 3)))
    # print(search_list1)
    return search_list


# 数据查找、截图
def search_song(driver):
    search_list = read_excel()
    print(search_list)
    try:
        for i, data in enumerate(search_list):
            category = str(data[0]).strip()
            if category.startswith('歌曲') or category.startswith('组合') or '歌曲别名' in data[0] or category.startswith('语义'):
                # 找到咪咕音乐搜索框并点击
                driver.find_element_by_id('music_homepage_search_ll_v7').click()
                time.sleep(2)
                search_name = data[1]
                if type(search_name) is float:
                    search_name = str(int(search_name)).strip()
                else:
                    search_name = str(search_name).strip()
                # 搜索框键入搜索词，按下回车键
                driver.find_element_by_id('edt_search_input').send_keys(search_name)
                driver.keyevent(66)
                print('保存图片：%d,%s,%s' % (i + 2, data[0], data[1]))
                time.sleep(3)
                # 截图并保存
                driver.get_screenshot_as_file('./picture/' + str(i + 2) + '.' + category + '.' + search_name + '.png')

                # 返回
                driver.find_element_by_id('iv_search_input_back').click()
                time.sleep(1)

            elif category.startswith('专辑') or '专辑别名' in data[0] or '歌手+专辑' in data[0]:
                # 找到咪咕音乐搜索框并点击
                driver.find_element_by_id('music_homepage_search_ll_v7').click()
                time.sleep(2)
                search_name = data[1]
                if type(search_name) is float:
                    search_name = str(int(search_name)).strip()
                else:
                    search_name = str(search_name).strip()
                # 搜索框键入搜索词，按下回车键
                driver.find_element_by_id('edt_search_input').send_keys(search_name)
                driver.keyevent(66)
                # 找到专辑页，点击
                zhuanji_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[2]/android.widget.TextView'
                driver.find_element_by_xpath(zhuanji_xpath).click()
                print('保存图片：%d,%s,%s' % (i + 2, data[0], data[1]))
                time.sleep(3)
                # 截图并保存
                driver.get_screenshot_as_file('./picture/' + str(i + 2) + '.' + category + '.' + search_name + '.png')

                # 返回
                driver.find_element_by_id('iv_search_input_back').click()
                time.sleep(1)

            elif category.startswith('MV') or category.startswith('mv') or '视频' == data[0] or 'mv别名' in data[0] or 'MV别名' in data[0]:
                # 找到咪咕音乐搜索框并点击
                driver.find_element_by_id('music_homepage_search_ll_v7').click()
                time.sleep(2)
                search_name = data[1]
                if type(search_name) is float:
                    search_name = str(int(search_name)).strip()
                else:
                    search_name = str(search_name).strip()
                # 搜索框键入搜索词，按下回车键
                driver.find_element_by_id('edt_search_input').send_keys(search_name)
                driver.keyevent(66)
                # 找到视频页，点击
                shipin_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[3]/android.widget.TextView'

                driver.find_element_by_xpath(shipin_xpath).click()
                print('保存图片：%d,%s,%s' % (i + 2, data[0], data[1]))
                time.sleep(3)
                # 截图并保存
                driver.get_screenshot_as_file('./picture/' + str(i + 2) + '.' + category + '.' + search_name + '.png')

                # 返回
                driver.find_element_by_id('iv_search_input_back').click()
                time.sleep(1)
            elif category.startswith('歌单'):
                # 找到咪咕音乐搜索框并点击
                driver.find_element_by_id('music_homepage_search_ll_v7').click()
                time.sleep(2)
                search_name = data[1]
                if type(search_name) is float:
                    search_name = str(int(search_name)).strip()
                else:
                    search_name = str(search_name).strip()
                # 搜索框键入搜索词，按下回车键
                driver.find_element_by_id('edt_search_input').send_keys(search_name)
                driver.keyevent(66)
                # 找到歌单页，点击
                gedan_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[4]/android.widget.TextView'
                driver.find_element_by_xpath(gedan_xpath).click()
                print('保存图片：%d,%s,%s' % (i + 2, data[0], data[1]))
                time.sleep(3)
                # 截图并保存
                driver.get_screenshot_as_file('./picture/' + str(i + 2) + '.' + category + '.' + search_name + '.png')

                # 返回
                driver.find_element_by_id('iv_search_input_back').click()
                time.sleep(1)

            elif category.startswith('歌词'):
                # 找到咪咕音乐搜索框并点击
                driver.find_element_by_id('music_homepage_search_ll_v7').click()
                time.sleep(2)
                search_name = data[1]
                if type(search_name) is float:
                    search_name = str(int(search_name)).strip()
                else:
                    search_name = str(search_name).strip()
                # 搜索框键入搜索词，按下回车键
                driver.find_element_by_id('edt_search_input').send_keys(search_name)
                driver.keyevent(66)
                # 找到歌词页，点击
                geci_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[5]/android.widget.TextView'
                driver.find_element_by_xpath(geci_xpath).click()
                print('保存图片：%d,%s,%s' % (i + 2, data[0], data[1]))
                time.sleep(3)
                # 截图并保存
                driver.get_screenshot_as_file('./picture/' + str(i + 2) + '.' + category + '.' + search_name + '.png')

                # 返回
                driver.find_element_by_id('iv_search_input_back').click()
                time.sleep(1)
            elif (category.startswith('歌手') or category.endswith('歌手')) and '歌手+' not in data[0]:
                # 找到咪咕音乐搜索框并点击
                driver.find_element_by_id('music_homepage_search_ll_v7').click()
                time.sleep(2)
                search_name = data[1]
                if type(search_name) is float:
                    search_name = str(int(search_name)).strip()
                else:
                    search_name = str(search_name).strip()
                # 搜索框键入搜索词，按下回车键
                driver.find_element_by_id('edt_search_input').send_keys(search_name)
                driver.keyevent(66)
                # 找到歌手页，点击
                geshou_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[6]/android.widget.TextView'
                driver.find_element_by_xpath(geshou_xpath).click()
                print('保存图片：%d,%s,%s' % (i + 2, data[0], data[1]))
                time.sleep(3)
                # 截图并保存
                driver.get_screenshot_as_file('./picture/' + str(i + 2) + '.' + category + '.' + search_name + '.png')

                # 返回
                driver.find_element_by_id('iv_search_input_back').click()
                time.sleep(1)
            elif category.startswith('演唱会'):
                # 找到咪咕音乐搜索框并点击
                driver.find_element_by_id('music_homepage_search_ll_v7').click()
                time.sleep(2)
                search_name = data[1]
                if type(search_name) is float:
                    search_name = str(int(search_name)).strip()
                else:
                    search_name = str(search_name).strip()
                # 搜索框键入搜索词，按下回车键
                driver.find_element_by_id('edt_search_input').send_keys(search_name)
                driver.keyevent(66)
                # 找到歌词页，点击
                geci_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[5]/android.widget.TextView'
                driver.find_element_by_xpath(geci_xpath).click()
                # 滑动
                width = driver.get_window_size()['width']
                height = driver.get_window_size()['height']
                time.sleep(0.2)
                start_x = width // 4 * 3
                start_y = height // 2
                distance = width // 2
                end_x = start_x - distance
                end_y = start_y
                for _ in range(2):
                    time.sleep(1)
                    driver.swipe(start_x, start_y, end_x, end_y)
                print('保存图片：%d,%s,%s' % (i + 2, data[0], data[1]))
                time.sleep(3)
                # 截图并保存
                driver.get_screenshot_as_file('./picture/' + str(i + 2) + '.' + category + '.' + search_name + '.png')

                # 返回
                driver.find_element_by_id('iv_search_input_back').click()
                time.sleep(1)
            elif category.startswith('票务'):
                # 找到咪咕音乐搜索框并点击
                driver.find_element_by_id('music_homepage_search_ll_v7').click()
                time.sleep(2)
                search_name = data[1]
                if type(search_name) is float:
                    search_name = str(int(search_name)).strip()
                else:
                    search_name = str(search_name).strip()
                # 搜索框键入搜索词，按下回车键
                driver.find_element_by_id('edt_search_input').send_keys(search_name)
                driver.keyevent(66)
                # 找到歌词页，点击
                geci_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[5]/android.widget.TextView'
                driver.find_element_by_xpath(geci_xpath).click()
                # 滑动3次
                width = driver.get_window_size()['width']
                height = driver.get_window_size()['height']
                time.sleep(0.2)
                start_x = width // 4 * 3
                start_y = height // 2
                distance = width // 2
                end_x = start_x - distance
                end_y = start_y
                for _ in range(3):
                    time.sleep(1)
                    driver.swipe(start_x, start_y, end_x, end_y)
                print('保存图片：%d,%s,%s' % (i + 2, data[0], data[1]))
                time.sleep(3)
                # 截图并保存
                driver.get_screenshot_as_file('./picture/' + str(i + 2) + '.' + category + '.' + search_name + '.png')

                # 返回
                driver.find_element_by_id('iv_search_input_back').click()
                time.sleep(1)
            elif '视频彩铃' in data[0]:
                print('没法搞：%d,%s,%s' % (i + 2, data[0], data[1]))

            elif (category.endswith('提示') or category.startswith('提示')) and len(category) < 11:
                # 找到咪咕音乐搜索框并点击
                driver.find_element_by_id('music_homepage_search_ll_v7').click()
                time.sleep(2)
                search_name = data[1]
                if type(search_name) is float:
                    search_name = str(int(search_name)).strip()
                else:
                    search_name = str(search_name).strip()
                # 搜索框键入搜索词
                driver.find_element_by_id('edt_search_input').send_keys(search_name)
                print('保存图片：%d,%s,%s' % (i + 2, data[0], data[1]))
                time.sleep(3)
                # 截图并保存
                driver.get_screenshot_as_file('./picture/' + str(i + 2) + '.' + search_name + '.png')

                # 返回
                driver.find_element_by_id('iv_search_input_back').click()
                time.sleep(1)
            elif len(category) == 0:
                pass
            else:
                # 找到咪咕音乐搜索框并点击
                driver.find_element_by_id('music_homepage_search_ll_v7').click()
                time.sleep(2)
                search_name = data[1]
                if type(search_name) is float:
                    search_name = str(int(search_name)).strip()
                else:
                    search_name = str(search_name).strip()
                # 搜索框键入搜索词，按下回车键
                driver.find_element_by_id('edt_search_input').send_keys(search_name)
                driver.keyevent(66)
                print('保存图片：%d,%s,%s' % (i + 2, data[0], data[1]))
                time.sleep(3)
                # 截图并保存
                driver.get_screenshot_as_file('./picture/' + str(i + 2) + '.' + category + '.' + search_name + '.png')

                # 返回
                driver.find_element_by_id('iv_search_input_back').click()
                time.sleep(1)

    finally:
        driver.close_app()


if __name__ == '__main__':
    start_time = time.time()
    driver = android_driver()
    # 输入：0：测试环境；1：预生产环境；2：生产环境；3：开发环境
    driver = chage_env(driver, 2)
    time.sleep(5)
    search_song(driver)
    end_time = time.time()
    cast_time = end_time - start_time
    print('cast time :%s' % cast_time)
