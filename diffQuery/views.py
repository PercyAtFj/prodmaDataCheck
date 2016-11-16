#coding:utf-8
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from io import BytesIO
from pyexcel_xlsxw import save_data
import sqlite3
import json
import test

def index(request):
    str = "index"
    return render(request, 'index.html',{'page':str})

def fund(request):
    str = "fund"
    return render(request, 'fund.html',{'page':str})

#def diffFundRecordsPage(request):
#    return render(request, 'fundDiffRecords.html')

def home(request):
    return render(request, 'home.html')

def export(request):
    dataList = queryDiffRecord_internal()
    type = ["seccode","unitnv","accumulatedUnitnv","manageFee","trustFee"]
    resultList = [[u'交易代码',u'单位净值',u'累计净值',u'管理费率',u'托管费率']]
    for item in dataList:
        if (item.get('fromProdma') == None and not item.get('fromEastmoney')):
            resultList.append([item['fromEastmoney']['seccode'],item['fromEastmoney']['trustFee'],item['fromEastmoney']['manageFee'],item['fromEastmoney']['accumulatedUnitnv'],item['fromEastmoney']['unitnv']])
        elif (item.get('fromEastmoney') == None and not item.get('fromProdma')):
            resultList.append([item['fromEastmoney']['seccode'],item['fromProdma']['trustFee'],item['fromProdma']['manageFee'],item['fromProdma']['accumulatedUnitnv'],item['fromProdma']['unitnv']])
        else:
            record = []
            for j in type:
                if item['fromProdma'][j] != item['fromEastmoney'][j]:
                    aa = item['fromProdma'][j] if item['fromProdma'][j] else "no value"
                    bb = item['fromEastmoney'][j] if item['fromEastmoney'][j] else "no value"
                    record.append(aa + " | " + bb)
                else:
                    record.append(item['fromProdma'][j])
            resultList.append(record)
    #data = {"Sheet 1": [[1, 2, 3], [4, 5, 6]], "Sheet 2": [[7, 8, 9], [10, 11, 12]]}
    data = {"Sheet 1": resultList}
    io = BytesIO()
    save_data(io,data)
    response = HttpResponse(io.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="foo.xlsx"'

    return response

def queryDiffRecord_internal():
    conn = sqlite3.connect('/home/vagrant/lixc/tutorial/tutorial/db.sqlite')
    cursor = conn.execute("SELECT s.seccode,s.trustFee,s.manageFee,s.accumulatedUnitnv,s.unitnv,s.comeFrom,s1.trustFee,s1.manageFee,s1.accumulatedUnitnv,s1.unitnv,s1.comeFrom from product as s left join product as s1 on s.seccode = s1.seccode where s.comeFrom='1' and s1.comeFrom='2' order by s.seccode")
    resultJson = []
    for row in cursor:
        dict = {}
        flag = False
        for i in range(4):
            x = i + 1
            y = i + 5
            if y == 8 and y == 9:
                temp = ("0" + row[x]) if row[x].startswith('.') else row[x]
                if row[y] and (row[y].endswith('%') or row[y].endswith('--')):
                    flag = True
                    break
                if float(temp) != float(str(row[y])):
                    flag = True
                    break
            elif row[x] != row[y]:
                    flag = True
        if flag:
            dict['fromProdma'] = {'seccode':row[0],'trustFee':row[1],'manageFee':row[2],'accumulatedUnitnv':row[3],'unitnv':row[4]}
            dict['fromEastmoney'] = {'seccode':row[0],'trustFee':row[6],'manageFee':row[7],'accumulatedUnitnv':row[8],'unitnv':row[9]}
            resultJson.append(dict)

    return resultJson

def queryDiffFundRecords(request):
#    with open(r"/home/vagrant/lixc/tutorial/tutorial/mylog.txt", encoding="utf-8") as fh:
#        a = json.load(fh)
    return HttpResponse(test.queryDiffFundRecords(), content_type='application/json')

def queryFun(request,funtionName):
    fun = getattr(test,funtionName)
    return HttpResponse(fun(), content_type='application/json')

def queryFundDiff(request):

    return HttpResponse(test.queryFundData(), content_type='application/json')

def queryDiffRecords(request):
    #    with open(r"/home/vagrant/lixc/tutorial/tutorial/mylog.txt", encoding="utf-8") as fh:
    #        a = json.load(fh)
        return HttpResponse(json.dumps(queryDiffRecord_internal()), content_type='application/json')

