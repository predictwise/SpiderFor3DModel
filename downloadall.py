# coding=utf-8
__author__ = 'zcq'

from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
import time, urllib, sqlite3, socket
import os, sys

# kmzfile = "/home/zcq/datas/wh3d_kmzs/"
# imgfile = "/home/zcq/datas/wh3d_imgs/"

def makedir():
    t = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if os.path.exists('/home/zcq/datas/'+t):
        pass
    else:
        os.makedirs('/home/zcq/datas/'+t+'/wh3d_kmzs/')
        os.makedirs('/home/zcq/datas/'+t+'/wh3d_imgs/')

    kmzfile = '/home/zcq/datas/'+t+'/wh3d_kmzs/'
    imgfile = '/home/zcq/datas/'+t+'/wh3d_imgs/'
    return kmzfile, imgfile

def download(conn, browser):
    cur = conn.cursor()
    cur.execute("select url from downjudgeurl where isdowned='no' and haskmz='yes'")
    rows = cur.fetchall()
    i = 1
    for row in rows:
        id = ''
        try:
            # 创建存放图片和kmz的目录
            kmzfile, imgfile = makedir()

            # 设置网络连接超时
            socket.setdefaulttimeout(120)

            print 'start %s' % i
            browser.get(row)
            time.sleep(8.0)

            templist = str(browser.current_url).split('=')
            urllist = str(templist[1]).split('#')
            id = urllist[0]
            # print 'id: ', id

            browser.find_element_by_id("button-download-text").click()

            title = browser.find_element_by_xpath("//h1[@id='title']")
            # print 'title: ', title.text

            author = browser.find_element_by_xpath("//div[@class='metadata-section-title user-thumb-name']")
            # print 'author: ', author.text

            tagstmp = ''
            tagslist = browser.find_elements_by_xpath("//div[@class='display-field tags-content']")
            for item in tagslist:
                tagstmp = tagstmp + ',' + item.text
            tags = tagstmp[1:]
            # print 'tags: ', tags

            desc = browser.find_element_by_xpath("//div[@id='description']")
            # print 'desc: ', desc.text

            try:
                browser.find_element_by_xpath("//a[@id='download-option-ks']")
                flag = 'ks'
            except:
                try:
                    browser.find_element_by_xpath("//a[@id='download-option-zip']")
                    flag = 'zip'
                except:
                    print 'finish %s: not found kmz' % i
                    i += 1
                    cur.execute("update downjudgeurl set haskmz='no' where id=?", (id,))
                    conn.commit()
                    continue

            kmzurl = ''
            if flag == 'ks':
                kmzurl = browser.find_element_by_xpath("//a[@id='download-option-ks']").get_attribute("href")
                # print 'kmzurl: ', kmzurl
                try:
                    # 下载kmz
                    urllib.urlretrieve(kmzurl, kmzfile+'%s.kmz' % id)
                except socket.error:
                    errno, errstr = sys.exc_info()[:2]
                    if errno == socket.timeout:
                        print 'download kmz timeout'
                        # urllib.urlretrieve(kmzurl, kmzfile+'%s.kmz' % id)
                    else:
                        print "kmz:other socket error: ", errstr

                    browser.quit()

            elif flag == 'zip':
                kmzurl = browser.find_element_by_xpath("//a[@id='download-option-zip']").get_attribute("href")
                # print 'kmzurl: ', kmzurl
                try:
                    # 下载collada
                    urllib.urlretrieve(kmzurl, kmzfile+'%s.zip' % id)
                except socket.error:
                    errno, errstr = sys.exc_info()[:2]
                    if errno == socket.timeout:
                        print 'download collada timeout'
                        # urllib.urlretrieve(colladaurl, kmzfile+'%s.zip' % id)
                    else:
                        print "collada:other socket error: ", errstr

                    browser.quit()

            imgurl = browser.find_element_by_xpath("//div[@class='slideshow-slide-image']/img").get_attribute("src")
            # print 'imgurl: ', imgurl
            # 下载image
            urllib.urlretrieve(imgurl, imgfile+'%s.jpg' % id)

            otherkeyslist = browser.find_elements_by_xpath("//div[@class='metadata-left-cell']")
            list1 = []
            for key in otherkeyslist:
                list1.append(key.text)

            othervalueslist = browser.find_elements_by_xpath("//div[@class='metadata-right-cell']")
            list2 = []
            for value in othervalueslist:
                list2.append(value.text)

            otherdict = dict(zip(list1, list2))
            other = str(otherdict)

            conn.execute("insert into building values (?,?,?,?,?,?,?,?,?,?)", (id, title.text, author.text, tags, desc.text, imgurl, kmzurl, imgfile, kmzfile, other))
            conn.commit()

            cur.execute("update downjudgeurl set isdowned='yes' where id=?", (id,))
            conn.commit()

            print 'finish %s: found kmz' % i
            i += 1

            time.sleep(2.0)

        except ElementNotVisibleException as enve:
            # model被从网站中删除
            print 'model is deleted from web: ', enve
            cur.execute("delete from downjudgeurl where id=?", (id,))
            conn.commit()
            continue
        except NoSuchElementException as nse:
            print 'exception: ', nse
            cur.execute("delete from downjudgeurl where id=?", (id,))
            conn.commit()
            continue
        except Exception as ex:
            print 'other exception: ', ex
            browser.quit()


if __name__ == '__main__':
    browser = webdriver.Firefox()  # Get local session of firefox
    conn = sqlite3.connect("/home/zcq/PycharmProjects/PyTest/building.db")
    download(conn, browser)