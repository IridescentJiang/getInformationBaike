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
        res_data['treat'] = "未找到相关内容"
        res_data['prevention'] = "未找到相关内容"

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
            if re.search("群体", name.get_text()):
                res_data['people'] = values[index].get_text()
            if re.search("病因", name.get_text()):
                res_data['reason'] = values[index].get_text()
            if re.search("症状", name.get_text()):
                res_data['symptom'] = values[index].get_text()
            if re.search("科室", name.get_text()):
                res_data['department'] = values[index].get_text()

        # 治疗 和 预防 的内容，通过次级标题查找
        sub_titles = soup.find_all('h2', class_='title-text')
        for sub_title in sub_titles:
            if re.search("治疗", sub_title.get_text()):
                treat_title = sub_title
                res_data['treat'] = ""
                while treat_title:
                    # 如果是div并且class不是para则退出
                    if (re.search("<div", str(treat_title)) and not re.search('class="para"', str(treat_title))) or \
                            (re.search("<dl", str(treat_title)) and not re.search('class="para"', str(treat_title))):
                        break
                    # 如果切换标签，则换行
                    if re.search('class="para"', str(treat_title)):
                        res_data['treat'] += "\n"
                    # 如果不是元素并且不是换行，则存入
                    if not re.search("<", str(treat_title)) and not re.search("\n", str(treat_title)):
                        # 去除次级标题中 治疗 和 疾病名 的字样
                        if str(treat_title).strip() != "治疗" and str(treat_title).strip() != res_data['title']:
                            res_data['treat'] += str(treat_title)
                    treat_title = treat_title.next_element
            if re.search("预防", sub_title.get_text()):
                prevention_title = sub_title
                res_data['prevention'] = ""
                while prevention_title:
                    if (re.search("<div", str(prevention_title)) and not re.search('class="para"', str(prevention_title)))\
                            or (re.search("<dl", str(prevention_title)) and not re.search('class="para"', str(prevention_title))):
                        break
                    if re.search('class="para"', str(prevention_title)):
                        res_data['prevention'] += "\n"
                    if not re.search("<", str(prevention_title)) and not re.search("\n", str(prevention_title)):
                        if str(prevention_title).strip() != "预防" and str(prevention_title).strip() != res_data['title']:
                            res_data['prevention'] += str(prevention_title)
                    prevention_title = prevention_title.next_element
        return res_data

    def parse(self, page_url, html_content, data):
        if page_url is None or html_content is None:
            return

        soup = BeautifulSoup(
            html_content, 'html.parser', from_encoding='utf-8')

        new_data = self._get_new_data(page_url, soup, data)

        return new_data
