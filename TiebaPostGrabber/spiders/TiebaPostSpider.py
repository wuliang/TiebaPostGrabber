# -*- coding: utf8 -*-
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.http import FormRequest
from scrapy.utils.url import urljoin_rfc, url_query_cleaner 
from scrapy.conf import settings
from scrapy.item import Item
from scrapy.spider import BaseSpider
from scrapy import log
from TiebaPostGrabber.items import PostItem
import urllib
import copy
import string
import json
    
class PostSpider(BaseSpider):
    name = 'tieba'
    allowed_domains = ["tieba.baidu.com"]
    forum_page = "http://tieba.baidu.com/f?kw=$KW&pn=$PN"
    post_page = "http://tieba.baidu.com/p/$POST?pn=$PN"
    call_backs = {'forum' : '_forum_callback',  'post' : '_post_callback' }
    start_urls = ['http://tieba.baidu.com/index.html']
    
    def thead_task_num(self):
        return len(self.thread_task)
        
    def clear_thread_store(self,  url):
        key = self._modify_url(url,  0)
        del self.thread_task[key]
        
    def fetch_thread_store(self,  url):
        # use 0 for post in thread
        key = self._modify_url(url,  0)
        thread = self.thread_task.setdefault(key,  {'title': "",'spagenum' : 0, 'lpagenum' :0 , 'floors': {} } )
        return thread

    def full_thread_process(self,  thread):
        print "\n\n"
        print "+" * 80
        print "Download finished : %s" % thread['title']
        for k, v in thread['floors'].iteritems():
            
            infos = self.jcoder.decode(v['info'])
            author = infos['author']
            
            floor = v.setdefault('name', "?")
            name = author.setdefault('name', "?")
            gender = author.setdefault('gender', 0)

            if gender == 1:
                gname = u'(男)'
            elif gender == 2:
                gname = u'(女)'
            else:
                gname = u'(＊)'
            
            has_grade = author.setdefault('has_grade', False)
            if has_grade:
                llevel = author.setdefault('grade_level', -1)
                lname = u"[%d 级]" % llevel
            else:
                lname = u"[? 级]"
                
            line = "*".join([v['floor'],  gname, lname, name]) + ":\t"            
            content = line +  v['content'].strip(' \t\n\r')
            print content
            #To known what has included... print it
            #for key, val in infos.items():
            #    print key, val
            
    # now forum and post use same function, since the similarity of their url
    def _modify_url(self, url, pn):
        ask = url.find('?')
        if ask == -1:
            return url + r"?pn=" + str(pn)

        kw = r"pn="
        index = url.find(kw)
        if index == -1:
            # there must have other parameters, append this
            return url + r"&pn=" + str(pn)
        # we also assume pn is the last one
        return url[0:index+len(kw)] + str(pn)
            
    def init_spider(self):
        self.start_pn = settings.get('START_PAGE_NO', 1)          
        self.end_pn = settings.get('END_PAGE_NO', 1)  
        self.maxpn_per_thread = settings.get('MAX_PAGE_PER_THREAD', 50)  
        self.forum_page_req = 0
        self.floors_per_page = settings.get('FLOORS_PER_PAGE', 30)           
        self.forums = settings.get('FORUMS', [])          
        self.request_posts = []
        self.thread_task = {}
        self._compile_callbacks()
        self.jcoder = json.JSONDecoder()
        
    def start_fetch_request(self):
       for forum in self.forums:
            url = "" + self.forum_page
            url = url.replace(r"$KW",  urllib.quote(forum.encode('gb2312')))
            url = url.replace(r"$PN",  str(self.start_pn))
            r = Request(url=url, callback=self._response_downloaded)
            r.meta.update(tiebatype='forum',  tiebapn=self.start_pn) 
            yield r
            self.forum_page_req += 1
  

    def parse(self, response):
	  # TODO: login...
        return [FormRequest.from_response(response, formnumber=1, 
                    formdata={'username': 'yyylllyyylllyy', 'password': 'abbc2012'},
                    callback=self.after_login,  dont_filter=True)]


    def after_login(self,  response):
        #print response
        #print response.body
        return self.after_prepahse(response)


    def after_prepahse(self,  response):
        self.init_spider()        
        return self.start_fetch_request()
        
    def _response_downloaded(self, response):
        callback = self._call_backs[response.meta['tiebatype']]
        return callback(response)
        
    def _post_callback(self,  response):

        pn = response.meta['tiebapn'] 

        self.log("Processing Post %s  [%d]" % (response.url , pn))
        thread = self.fetch_thread_store(response.url)
        
        hxs = HtmlXPathSelector(response)
        if pn == 1:
            while True:
                titles  = hxs.select('//title/text()')
                if not titles:
                    break
                title = titles[0].extract()
                title = title.strip()
                thread['title'] = title
                
                thread_infos = hxs.select('//div[@class = "l_thread_info"]')
                if not thread_infos:
                    break
                info = thread_infos[0]
                postnum = info.select('.//span[@class="d_red_num"]/text()')
                if not postnum:
                    break
                    
                postnum = int(postnum[0].extract())
                pnum = (postnum + self.floors_per_page  -1 ) / self.floors_per_page
                self.log("post num is %d, page num %d" % (postnum,  pnum))
                if pnum > self.maxpn_per_thread:
                    pnum = self.maxpn_per_thread
                    self.log("Too many floors in %s" % response.url, level=log.WARNING)
                thread['spagenum'] = pnum
                for n in range(2, pnum+1):
                    url = self._modify_url(response.url,  n)
                    if url:
                        r = Request(url=url, callback=self._response_downloaded)
                        r.meta.update(tiebatype='post',  tiebapn=n) 
                        yield r
                break
          
        thread['lpagenum']  += 1       
        thread_floors = thread['floors']
        posts = hxs.select('//div[@class="l_post"]')        
        for post in posts:
            spost = {'info':'', 'floor':'', 'content':''}
            infos = post.select('div[@class = "p_post"]/@data-field')
            floors = post.select('.//p[@class="d_floor"]/text()')
            contents = post.select('.//p[@class="d_post_content"]/text()')
            for info in infos:
                spost['info'] =  info.extract()
                break
            for floor in floors:
                spost['floor'] = floor.extract()
                break
            for content in contents:
                spost['content']  = content.extract()
                break
            floorid = int("".join([x for x in spost['floor'] if x in string.digits]))
            thread_floors[floorid] = spost
        
        if thread['lpagenum'] == thread['spagenum']:
            self.log("All %d pages have got for %s" % (thread['lpagenum'],  response.url))
            self.full_thread_process(thread)
            self.clear_thread_store(response.url)
            print "Remain on-going tasks %d" % self.thead_task_num()
            print "Remain un-fired tasks %d" % len(self.request_posts)
            
        # don't yield it too much, do't too many concurrency
        if self.thead_task_num()<5 and len(self.request_posts) > 0:
            yield self.request_posts.pop(0)
        
    def _forum_callback(self,  response):

        pn = response.meta['tiebapn'] 
        self.log("Processing Forum %s  [%d]" % (response.url , pn))
        
        hxs = HtmlXPathSelector(response)          
        bodies = hxs.select('//div/table/tbody')
        for body in bodies:
            threads = hxs.select('.//tr/td[@class="thread_title"]/a')
            for thread in threads:
                ref = thread.select('./@href')
                title =  thread.select('./text()')
                text = title[0].extract()
                link = ref[0].extract()

                url = urljoin_rfc(response.url, link)
                r = Request(url=url, callback=self._response_downloaded)
                r.meta.update(tiebatype='post',  tiebapn=1)
                self.request_posts.append(r)
                
        if pn == self.start_pn:
            for n in range(pn+1, self.end_pn+1):
                url = self._modify_url(response.url,  n)
                if url:
                    r = Request(url=url, callback=self._response_downloaded)
                    r.meta.update(tiebatype='forum',  tiebapn=n) 
                    self.forum_page_req += 1
                    yield r
                    
        self.forum_page_req -= 1
        if self.forum_page_req == 0:
            if len(self.request_posts) > 0:
                yield self.request_posts.pop(0)            

    def _compile_callbacks(self):
        def get_method(method):
            if callable(method):
                return method
            elif isinstance(method, basestring):
                return getattr(self, method, None)

        self._call_backs = {}
        for name in self.call_backs.keys():
            self._call_backs[name] = get_method(self.call_backs[name])

