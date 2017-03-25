#-*- coding: utf-8 -*-
import re
import urllib
import urllib2
import json
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

from django.http import Http404
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render_to_response

from .models import Blog, Comment
from .forms import CommentForm


def get_blogs(request):
    ctx = {
        'blogs': Blog.objects.all().order_by('-created')
    }
    return render(request, 'blog-list.html', ctx)


def get_detail(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['blog'] = blog
            Comment.objects.create(**cleaned_data)

    ctx = {
        'blog': blog,
        'comments': blog.comment_set.all().order_by('-created'),
        'form': form
    }
    return render(request, 'blog-detail.html', ctx)



def getImg(url, imgType):
    page = urllib.urlopen(url)
    html = page.read()
    # re_key = r'<img.*?src="(.*?\.'+imgType+')".*?>'
    # re_key = r'<img.*?src=[\'|"](.*?\.'+imgType+')[\'|\"].*?>'
    re_key = r'<img.*?[src|data-original|data-imgurl]=[\'|\"]([http://|https://].*?\.'+imgType+')[\'|\"].*?>'
    # re_key = r'<img.*?[src]=[\'|\"](.*?\.'+imgType+')[\'|\"].*?>'
    imgre = re.compile(re_key,re.S)
    imgList = re.findall(imgre, html)
    return imgList

def mm(request):
    query = request.GET.get('q','')
    if query:
        imglist = getImg(query, 'jpg')
    else:
        imglist = []
    return render_to_response('crawler.html', {'query': query, 'results': imglist})


def zs(request):
    if request.GET:
        key = request.GET.get('key')
        url = 'http://openbox.mobilem.360.cn/app/getTagAppList?s_stream_app=1&cid='+key+'&order=download&prepage=recommend_category&page=1'
        html = urllib2.urlopen(url).read()
        data = json.loads(html)
        data1 = data['data']
        # data1 = json.loads(data['data'])
        return render_to_response("zs.html",{"url": url, "danny": data1 })
    else:
        url = 'http://openbox.mobilem.360.cn/app/getTagAppList?s_stream_app=1&cid=1&order=download&prepage=recommend_category&page=1'
        html = urllib2.urlopen(url).read()
        data = json.loads(html)
        data1 = data['data']
        # data1 = json.loads(data['data'])
        return render_to_response("zs.html",{"url": url, "danny": data1 })


# https://www.toutiao.com/search/?keyword=smap  
# 抓取今日头条搜索页内容分类整理
#https://www.toutiao.com/search_content/?offset=0&format=json&keyword=smap&autoload=true&count=20&cur_tab=1

def toutiao(request):
	# me = "jinritoutiao"
	if request.GET:
		key = request.GET.get('q')
		page = request.GET.get('page')
		url = 'https://www.toutiao.com/search_content/?offset=0&format=json&keyword='+str(key)+'&autoload=true&count=20&cur_tab='+str(page)
		html = urllib2.urlopen(url).read()
		data = json.loads(html)
		data1 = data['data']
		return render_to_response('toutiao.html', {'me':data1})
	else:
		return render_to_response('toutiao.html')
		
		
		
def resume(request):
    return render_to_response('resume.html')
