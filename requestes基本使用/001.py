#首先我们先导入requests这个包
import requests

#我们来吧百度的index页面的html源码抓取到本地，并用r变量保存
#注意这里，网页前面的 http://一定要写出来，它并不能像真正的浏览器一样帮我们补全http协议
r = requests.get("http://www.baidu.com")


#将下载到的内容打印一下：
#print(r.text)

'''
OUT:

<!DOCTYPE html>
<!--STATUS OK--><html> <head><meta http-equiv=content-type content=text/html;charset=utf-8><meta htt
p-equiv=X-UA-Compatible content=IE=Edge><meta content=always name=referrer><link rel=stylesheet type
=text/css href=http://s1.bdstatic.com/r/www/cache/bdorz/baidu.min.css><title>ç¾åº¦ä¸ä¸ï¼ä½ å°±ç¥é</t
itle></head> <body link=#0000cc> <div id=wrapper> <div id=head> <div class=head_wrapper> <div class=
s_form> <div class=s_form_wrapper> <div id=lg> <img hidefocus=true src=//www.baidu.com/img/bd_logo1.
png width=270 height=129> </div> <form id=form name=f action=//www.baidu.com/s class=fm> <input type
=hidden name=bdorz_come value=1> <input type=hidden name=ie value=utf-8> <input type=hidden name=f v
alue=8> <input type=hidden name=rsv_bp value=1> <input type=hidden name=rsv_idx value=1> <input type
=hidden name=tn value=baidu><span class="bg s_ipt_wr"><input id=kw name=wd class=s_ipt value maxleng
th=255 autocomplete=off autofocus></span><span class="bg s_btn_wr"><input type=submit id=su value=ç¾
åº¦ä¸ä¸ class="bg s_btn"></span> </form> </div> </div> <div id=u1> <a href=http://news.baidu.com nam
e=tj_trnews class=mnav>æ°é»</a> <a href=http://www.hao123.com name=tj_trhao123 class=mnav>hao123</a>
 <a href=http://map.baidu.com name=tj_trmap class=mnav>å°å¾</a> <a href=http://v.baidu.com name=tj_t
rvideo class=mnav>è§é¢</a> <a href=http://tieba.baidu.com name=tj_trtieba class=mnav>è´´å§</a> <nosc
ript> <a href=http://www.baidu.com/bdorz/login.gif?login&amp;tpl=mn&amp;u=http%3A%2F%2Fwww.baidu.com
%2f%3fbdorz_come%3d1 name=tj_login class=lb>ç»å½</a> </noscript> <script>document.write('<a href="ht
tp://www.baidu.com/bdorz/login.gif?login&tpl=mn&u='+ encodeURIComponent(window.location.href+ (windo
w.location.search === "" ? "?" : "&")+ "bdorz_come=1")+ '" name="tj_login" class="lb">ç»å½</a>');</s
cript> <a href=//www.baidu.com/more/ name=tj_briicon class=bri style="display: block;">æ´å¤äº§å</a>
</div> </div> </div> <div id=ftCon> <div id=ftConw> <p id=lh> <a href=http://home.baidu.com>å³äºç¾åº
¦</a> <a href=http://ir.baidu.com>About Baidu</a> </p> <p id=cp>&copy;2017&nbsp;Baidu&nbsp;<a href=h
ttp://www.baidu.com/duty/>ä½¿ç¨ç¾åº¦åå¿è¯»</a>&nbsp; <a href=http://jianyi.baidu.com/ class=cp-feedb
ack>æè§åé¦</a>&nbsp;äº¬ICPè¯030173å·&nbsp; <img src=//www.baidu.com/img/gs.gif> </p> </div> </div> <
/div> </body> </html>
'''

'''
Response(self)

The :class:Response <Response> object, which contains a server's response to an HTTP request.

'''
#HTTP请求的返回状态，比如，200表示成功，404表示失败
print (r.status_code)
#HTTP请求中的headers
print (r.headers)
#从header中猜测的响应的内容编码方式 
print (r.encoding)
#从内容中分析的编码方式（慢）
print (r.apparent_encoding)
#响应内容的二进制形式
#print (r.content)

'''
200

{'Server': 'bfe/1.0.8.18', 'Date': 'Tue, 02 May 2017 12:01:47 GMT', 'Content-Type': 'text/html', 'La
st-Modified': 'Mon, 23 Jan 2017 13:28:27 GMT', 'Transfer-Encoding': 'chunked', 'Connection': 'Keep-A
live', 'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Pragma': 'no
-cache', 'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Content-Encoding':
'gzip'}

ISO-8859-1

utf-8
'''