#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' request handler module '            #表示模块的文档注释

__author__ = 'Thr3e'

import requests



header={
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
	"cookie": "gsScrollPos-2=0; PHPSESSID=web1~a7bd31l7j6oh5fshmmfsoc2ft1",
	"upgrade-insecure-requests": "1",
	"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}


def __art_url__(pageNum):
	return "https://segmentfault.com/u/guchengshaonian_5a56fe95f2c32/articles?page={}".format(pageNum)

def __content_url__(id):
    return "https://segmentfault.com/a/{}".format(str(id))

def __get_respons__(url):
    return requests.get(url,headers=header).text

def art_list_data(p):
    return __get_respons__(__art_url__(p))

def art_content_data(id_str):
    return __get_respons__(__content_url__(id_str))