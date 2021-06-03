# coding=utf-8
#!/usr/bin/python

'''
Html 输出器
'''

import xlsxwriter


class HtmlOutputer(object):

    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is not None:
            self.datas.append(data)

    def output_html(self):
        fout = open('output.html', 'w', encoding='utf-8')

        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')

        for data in self.datas:
            fout.write('<tr>')
            fout.write("<td>%s</td>" % data['search'])
            # fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'])
            # fout.write("<td>%s</td>" % data['summary'])
            fout.write("<td>%s</td>" % data['department'])
            fout.write("<td>%s</td>" % data['people'])
            fout.write("<td>%s</td>" % data['reason'])
            fout.write("<td>%s</td>" % data['symptom'])
            fout.write('</tr>')

        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')

        fout.close()

    def output_excel(self):
        excel = xlsxwriter.Workbook('output_baike.xlsx')
        excelsheet = excel.add_worksheet()
        title = ['搜索疾病名称', '百度百科疾病名称', '所属科室', '多发人群', '主要病因', '主要症状', '治疗方式', '预防措施']
        # title = ['搜索疾病名称', '主要病因', '主要症状', '治疗方式', '预防措施']
        excelsheet.write_row(u'A1', title)
        for index, data in enumerate(self.datas):
            excelsheet.write_row(u'A'+str(index+2), data.values())

        excel.close()