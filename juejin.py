# -*-coding:utf-8 -*-
import urllib.request
import json
import datetime
from db.mongodb import mongodb


def getURLDatas(beforeDate):
    url = "https://timeline-merger-ms.juejin.im/v1/get_entry_by_timeline?src=web&before=" + beforeDate + "T00%3A01%3A00.175Z&limit=200&type=post&category=5562b415e4b00c57d9b94ac8"
    res = urllib.request.urlopen(url)
    datas = res.read()
    jsonObj = json.loads(datas)
    list = []
    set = {}
    articles = mongodb.initCollection('articles')
    for item in jsonObj['d']["entrylist"]:
        result = articles.find({"id": item["objectId"]})
        # print(item["createdAt"])
        # print(result.count())
        if result.count() == 0:
            articles.insert({"columnid": "BJcTbyZoW", "brief": item["summaryInfo"],
                             "title": item["title"],
                             "link": item["originalUrl"],
                             "id": item["objectId"],
                             "publishtime":datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"),
                             "author":"crawler"})


now = datetime.datetime.now()
dstr = "2017-01-01"
dtime = datetime.datetime.strptime(dstr, "%Y-%m-%d")
while dtime < now:
    print(dstr)
    getURLDatas(dstr)
    dtime = datetime.datetime.strptime(dstr, "%Y-%m-%d")
    dtime = dtime + datetime.timedelta(days=1)
    dstr = datetime.datetime.strftime(dtime, "%Y-%m-%d")
