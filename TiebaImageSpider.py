import os
import random
from lxml import etree
from urllib import request, parse


class TiebaImageSpider:
    def __init__(self, name, start=1, end=1):
        self.name = name
        self.__start = start
        self.__end = end

    def loadmainpage(self):
        page = self.__start

        # UA_list = [
        #     'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
        #     'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
        #     'Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11'
        # ]

        for i in range(self.__end - self.__start + 1):
            page += i
            url = 'http://tieba.baidu.com/f?' + parse.urlencode({'kw': self.name}) + '&pn=' + str((page - 1) * 50)
            req = request.Request(url)
            response = request.urlopen(req)
            html = response.read().decode('utf-8')
            self.xhtml(html)

    def xhtml(self, html):
        """
        提取loadmainpage()请求到的HTML页面中的帖子地址
        """
        content = etree.HTML(html)
        list = content.xpath('//div[@class="threadlist_lz clearfix"]//a[@class="j_th_tit "]/@href')
        for i in list:
            self.loadsecpage(i)

    def loadsecpage(self, page):
        """
        收到xhtml解析出来的帖子地址，构造url，请求帖子页面
        """
        url = 'http://tieba.baidu.com' + page
        response = request.urlopen(url)
        html = response.read().decode('utf-8')
        self.ximage(html)

    def ximage(self, html):
        """
        解析loadsecpage()传递的html页面，提取页面中图片地址
        :return:
        """
        content = etree.HTML(html)
        title = str(content.xpath('//h3/@title')[0])
        list = content.xpath('//img[@class="BDE_Image"]/@src')
        self.downloadimage(title, list)

    def downloadimage(self, title, list):
        """
        下载图片到已该贴为名的文件夹
        """
        if os.path.exists(title):
            title = title + str(random.randint(0, 100))
            os.mkdir(title)
        else:
            os.mkdir(title)
        for i in list:
            response = request.urlopen(str(i))
            image = response.read()
            name = i[-10:]
            f = open('./' + title + '/' + name, 'wb')
            f.write(image)
            f.close()
        print('----%s--下载完成----' % title)


def main():
    name = input('输入贴吧名：')
    start = int(input('输入起始页：'))
    end = int(input('输入终止页：'))

    if start < 0 or start > end:
        print('输入有误。')

    L = TiebaImageSpider(name, start, end)
    L.loadmainpage()
    print('----全部下载完毕----')


if __name__ == "__main__":
    main()
