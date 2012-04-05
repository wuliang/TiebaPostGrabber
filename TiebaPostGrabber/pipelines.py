from os.path import isfile, join, basename
from urllib import unquote
from scrapy.http import Request
from scrapy.contrib.pipeline.media import MediaPipeline
from scrapy.conf import settings


STORE_DIR = settings.get('STORE_DIR', '/tmp/tieba')


class PostFileDownload(MediaPipeline):

    def get_media_requests(self, item, info):
        return [Request(x) for x in item.get('image_urls', [])]   


    def media_to_download(self, request, info):
        tpath = self._path(request.url)
        return tpath if isfile(join(STORE_DIR, tpath)) else None

    def media_downloaded(self, response, request, info):
        tpath = self._path(request.url)
        tfile = open(join(STORE_DIR, tpath), 'wb')
        tfile.write(response.body)
        tfile.close()
        return tpath


    def _path(self, url):
        return basename(unquote(url))
