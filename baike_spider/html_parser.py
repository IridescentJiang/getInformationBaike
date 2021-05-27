# coding=utf-8
#!/usr/bin/python

'''
Html 解析器

传入 url 解析新的url列表（title 和 summary）
'''
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from urllib.parse import urljoin
import urllib.parse


class HtmlParser(object):

    def _get_new_urls(self, page_url, soup):
        new_urls = set()

        # 获取所有的链接，例如a 标签
        '''
        <a class="lock-lemma" target="_blank" href="/view/10812319.htm" 
        '''
        links = soup.find_all('a', href=re.compile(r"/item/"))

        for link in links:
            new_url = link['href']
            # 拼接 url
            # python 2x
            # new_full_url = urlparse.urljoin(page_url, new_url)
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)

        return new_urls

    def _get_new_data(self, page_url, soup, res_data):
        #res_data['summary'] = "未找到相关内容"
        res_data['title'] = "未找到相关内容"
        res_data['department'] = "未找到相关内容"
        res_data['people'] = "未找到相关内容"
        res_data['reason'] = "未找到相关内容"
        res_data['symptom'] = "未找到相关内容"

        # Url
        #res_data['url'] = page_url

        # title
        if soup.find('dd', class_='lemmaWgt-lemmaTitle-title') is not None:
            title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find("h1")
            res_data['title'] = title_node.get_text()

        # summary
        #summary_node = soup.find('div', class_="lemma-summary")
        #if summary_node is not None:
        #    res_data['summary'] = summary_node.get_text()

        # items
        names = soup.find_all('dt', class_='basicInfo-item name')
        values = soup.find_all('dd', class_='basicInfo-item value')
        for index, name in enumerate(names):
            if(re.search("群体", name.get_text())):
                res_data['people'] = values[index].get_text()
            if (re.search("病因", name.get_text())):
                res_data['reason'] = values[index].get_text()
            if (re.search("症状", name.get_text())):
                res_data['symptom'] = values[index].get_text()
            if (re.search("科室", name.get_text())):
                res_data['department'] = values[index].get_text()
        return res_data

    def parse(self, page_url, html_content, data):
        if page_url is None or html_content is None:
            return

        soup = BeautifulSoup(
            html_content, 'html.parser', from_encoding='utf-8')

        new_data = self._get_new_data(page_url, soup, data)

        return new_data
