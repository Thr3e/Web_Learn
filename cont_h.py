#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' content handler module '            #表示模块的文档注释

__author__ = 'Thr3e'

#格式化md文件内容
def format_md(list):
    key_words=['(','之','（']
    replace_words=[' ','学习之路']
    md_dict={"Others":[]}
    for obj in list:
        for word in key_words:
            if(obj['title'].find(word) != -1):
                group_name = obj['title'].partition(word)[0]
                for r_word in replace_words:
                    group_name=group_name.replace(r_word, '')
                if group_name not in md_dict.keys():
                    md_dict[group_name] = [obj]
                else:
                    md_dict[group_name].append(obj)
                break
        else:
            md_dict['Others'].append(obj)
    return md_dict

def markdown_format(content):
    md_cont = format_md(content)
    md_str="\n\n\n"
    for key in md_cont.keys():
        md_str = md_str + "###" + key + '\n'
        for obj in md_cont[key]:
            cur_str = str(obj['likes']).rjust(3,"0") + '票\t[' + obj['title'] + '](' + obj['url'] + ')\t' + obj['update_time'] + '\n'
            md_str = md_str + cur_str
        md_str = md_str + "\n"
    return md_str


#处理获取到的请求文本
def get_htmlStr(html_text):
	s=html_text.find("<div class=\"col-md-10 profile-mine\">")
	e=html_text.find("<div class=\"text-center\">")
	start=html_text.find("<ul class=\"profile-mine__content\">",s,e)
	end=html_text.find("</ul>",s,e)
	tmp_str=html_text[start+len("<ul class=\"profile-mine__content\">"):end]
	str_list=tmp_str.split('<li')
	n=0
	res=[];
	for subStr in str_list:
		if(subStr.find("<a") != -1):
			title_start=subStr.find("<a")
			title_end=subStr.find("</a>")
			a_str=subStr[title_start:title_end]
			title=a_str[a_str.find(">")+1:len(a_str)].replace(" ","")
			id_str=a_str[a_str.find("href=")+9:a_str.find("\">")]
			url_str="https://segmentfault.com/a/"+id_str
			time_s=subStr.find("<span class=\"profile-mine__content--date\">")
			time_e=subStr.rfind('</span>')
			time_str=subStr[time_s+len("<span class=\"profile-mine__content--date\">"):time_e]
			agree_s=subStr.find("<span class=\"label label-warning  \">")
			agree_e=subStr.find('</span>')
			agree_str=subStr[agree_s+len("<span class=\"label label-warning  \">"):agree_e]
			res.append({
				"id":int(id_str),
				"title":title,
				"url":url_str,
				"update_time":time_str,
				"likes":int(agree_str[0:agree_str.find('票')])
				})
		# "https://segmentfault.com/"
	return res

#获取文章标题
def query_content_title(html):
    s_str = "<title>"
    e_str = "</title>"
    res = ''
    if(html.find(s_str) != -1):
        s=html.find(s_str)
        e=html.find(e_str,s)+len(e_str)
        res=html[s:e].replace("- 个人文章 - SegmentFault 思否","").replace(" ","")
    else:
        res="fail"
    return res


#获取文章主体
def query_content_body(html):
    s_str = "<div class=\"article fmt article__content\""
    e_str = "</div>"
    res = ''
    if(html.find(s_str) != -1):
        s=html.find(s_str)
        e=html.find(e_str,s)+len(e_str)
        res=html[s:e]
    else:
        res="fail"
    return res