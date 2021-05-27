# coding=utf-8
# !/usr/bin/python

'''
HTML 下载器
'''
import urllib.request
import urllib.parse


class HtmlDownload(object):

    def downloader(self, url, param):
        if url is None:
            return None

        response = urllib.request.urlopen("https://" + urllib.request.quote(url.format(param)))
        print(param + " craw: " + "https://" + urllib.request.quote(url.format(param)))
        if response.getcode() != 200:
            print("response.getcode() =", response.getcode())
            return None

        return response.read()
