#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' main module '            #表示模块的文档注释

__author__ = 'Thr3e'

import time
import sys

import sql_h
import req_h
import cont_h

#搜索数据
def search_data(key):
	tmp_list= sql_h.query_art_by_title(key=key)
	for obj in tmp_list:
		print(obj['title']+obj['url'])
	return tmp_list

#获取所有文章信息
def get_arts():
	next_page=True
	pageIndex=1
	res_list=[]
	while (next_page):
		time.sleep(1)
		print("current page:",pageIndex)
		tmplist=cont_h.get_htmlStr(req_h.art_list_data(pageIndex))
		if(len(tmplist)>0):
			res_list=res_list+tmplist
		else:
			next_page=False
		pageIndex = pageIndex+1
	# print(len(res_list))
	return res_list

#输出更新日志
def commit_update(data):
	log=""
	if(len(data) == 0):
		log="文章没有更新"
	else:
		log="此次更新:\n"
		for obj in data:
			log = log + obj['title'] + '\t' + obj['url'] + "\n"
	print(log)
	return None

#输出md文件
def write_file(file_name,content):
	file=open(file_name,"w+")
	file.write(content)
	print("file has been written")
	file.close()
	return None

#下载文章
def donwload_articles(ids):
	i=0
	for num in ids:
		i = i + 1
		content=req_h.art_content_data(num)
		sql_h.update_contdb({
			'id':int(num),
			'title':cont_h.query_content_title(content),
			'cont':cont_h.query_content_body(content)})
		progress_test(i / len(ids))
		time.sleep(2)
	print('\narticles downloaded')

#显示进度条
def progress_test(rate):
	bar_length=20
	hashes = '#' * int(rate * bar_length)
	spaces = ' ' * (bar_length - len(hashes))
	sys.stdout.write("\rPercent: [%s] %d%%"%(hashes + spaces, rate * 100))
	sys.stdout.flush()
	return None

#测试
def __test__():
	print("test")
	commit_update(sql_h.query_new_art())
	return None

#主入口
def main():
	fo_type = input(
"""
{split}
1=>search(s)
2=>update(u)
3=>output markdown(md)
4=>download articles(d)
{split}
what to do:""".format(split="-"*30)
	).lower()

	if(fo_type == '1' or fo_type == 's'):
		key_world=input("Input the key world(* for all):").lower()
		search_data(key_world)
	elif(fo_type == '2' or fo_type == 'u'):
		print("start updating!")
		sql_h.db_restore(get_arts())
		commit_update(sql_h.query_new_art())
	elif(fo_type == '3' or fo_type == 'md'):
		write_file("web-course.md",cont_h.markdown_format(sql_h.latest_art))
	elif(fo_type == '4' or fo_type =='d'):
		conf=input('input article id(* for all):')
		ids=[]
		if(conf == "*"):
			for obj in sql_h.latest_art:
				ids.append(obj['id'])
		else:
			ids = conf.split(',')
		donwload_articles(ids)
	elif(fo_type == 'test' or fo_type == 't'):
		__test__()
	else:
		pass
	return None

if __name__=='__main__':
	main()