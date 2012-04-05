# -*- coding: utf8 -*-
# Scrapy settings for ImageGrabber project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME    = 'TiebaPostGrabber'
BOT_VERSION = '0.1'

# Random interval between 0.5 and 1.5 * DOWNLOAD_DELAY
DOWNLOAD_DELAY     = 0.25 

SPIDER_MODULES     = ['TiebaPostGrabber.spiders']
NEWSPIDER_MODULE   = 'TiebaPostGrabber.spiders'
DEFAULT_ITEM_CLASS = 'TiebaPostGrabber.items.PostItem'

USER_AGENT   = "Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.1.19) Gecko/20110430 Iceweasel/3.5.19 (like Firefox/3.5.19)"
ITEM_PIPELINES = ['TiebaPostGrabber.pipelines.PostFileDownload']
STORE_DIR = 'TiebaPostGrabber/TiebaPostStore'
# 哪些论坛。最好一次一个。否则打印比较混乱
#FORUMS = ['2012', u'李毅', u'魔兽世界' ]
FORUMS = [u'孙燕姿']
# 每个论坛的起终页面，目前实现至少要下载START_PAGE_NO
START_PAGE_NO = 1
END_PAGE_NO = 2

# 每个文章贴内楼高（用于估计每个Thread使用的页面数，这里设置比较方便）
FLOORS_PER_PAGE = 30
# 每个Thread最大的页面数（超过部分将舍弃）
MAX_PAGE_PER_THREAD = 50

LOG_LEVEL = 'INFO'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn,zh;q=0.5',
    'Accept-Encoding': 'deflate',
    'Accept-Charset' :'GBK,utf-8;q=0.7,*;q=0.7', 
}
