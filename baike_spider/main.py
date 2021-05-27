# coding=utf-8
# !/usr/bin/python

from baike_spider import url_manager, html_download, html_parser, html_outputer

import traceback


class SpiderMain(object):

    def __init__(self):
        # URL 管理器
        self.urls = url_manager.UrlManager()
        # URL 下载器
        self.downloader = html_download.HtmlDownload()
        # URL 解析器
        self.parser = html_parser.HtmlParser()
        # URL 输出器
        self.outputer = html_outputer.HtmlOutputer()

    # 爬虫的调度程序
    def craw(self, root_url, params):

        # 获取待爬取的 URL
        new_url = root_url

        for param in params:
            html_content = self.downloader.downloader(new_url, param)
            if html_content is None:
                print("html_content None")
            new_data = {"search": param}
            new_data = self.parser.parse(new_url, html_content, new_data)
            self.outputer.collect_data(new_data)

        self.outputer.output_excel()


if __name__ == '__main__':
    with open("search.txt", 'r', encoding='utf-8') as fr:
        # params = {"牙周炎", "种植体周围炎", "龋病", "牙髓病", "口腔溃疡", "扁平苔藓", "牙体缺损", "牙列缺损",
        #           "牙列拥挤", "阻生齿", "口腔肿瘤", "颞下颌关节病", "儿童口腔疾病"}
        params = fr.readlines()
        params = [line.strip("\n") for line in params]
        print(params)
    root_url = "baike.baidu.com/item/{}"
    obj_spider = SpiderMain()
    # 启动爬虫
    obj_spider.craw(root_url, params)
