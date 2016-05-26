# coding=utf-8
__author__ = 'zcq'

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time, os, sqlite3, socket, sys
import downloadall


def spiderUrl(browser, start, end, page):
    try:
        # 设置页面加载超时
        # browser.set_page_load_timeout(180)
        # 设置网络连接超时
        socket.setdefaulttimeout(180)
        # Load page
        browser.get("https://3dwarehouse.sketchup.com/search.html?q=building&backendclass=entity&usepagination=true&fetchsize=60#sr"+str(start)+"_er"+str(end)+"_cp"+str(page))
        time.sleep(8.0)

        # page = 1

        conn = sqlite3.connect("/home/zcq/PycharmProjects/PyTest/building.db")
        cur = conn.cursor()
        while True:
            for link_elem in browser.find_elements_by_xpath("//a[@class='results-entity-link']"):
                each_url = link_elem.get_attribute("href")
                cur.execute("select count(*) from downjudgeurl where url=?", (each_url,))
                n = cur.fetchone()[0]
                if n == 0:
                    # print each_url
                    templist = str(each_url).split('=')
                    urllist = str(templist[1]).split('#')
                    id = urllist[0]

                    conn.execute("insert into downjudgeurl values (?,?,?,?)", (id, each_url, 'no', 'yes'))
                    conn.commit()
                elif n == 1:
                    print 'url exists'

            print 'page: ', page
            os.system("echo %s > /home/zcq/PycharmProjects/PyTest/urlout.txt" % page)

            # 6952
            if page == 6952:
                break
            else:
                page += 1
                browser.find_element_by_xpath("//div[@class='next-button']").click()
                time.sleep(8.0)

        # downloadall.download(conn, browser)

    # except TimeoutException:
        # print 'load web timeout'
        # browser.quit()
    except socket.error:
        errno, errstr = sys.exc_info()[:2]
        if errno == socket.timeout:
            print 'download url timeout'
        else:
            print "other socket error: ", errstr

        browser.quit()
    except Exception as ex:
        print ex.message
        browser.quit()


if __name__ == '__main__':
    res = open('/home/zcq/PycharmProjects/PyTest/urlout.txt', 'r')
    page = res.read()
    # 下载下一页的数据
    page = int(page) + 1
    end = page * 60
    start = end - 60 + 1
    # Get local session of firefox
    browser = webdriver.Firefox()
    spiderUrl(browser, start, end, page)