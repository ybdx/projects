import Queue
import urllib
import urllib2
import json
import re
import string
import base64

q = Queue.Queue()


#file_input = open("./data/proxy.txt", "r")
#data = file_input.readlines()
#for i in data:
#    q.put(i)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        global q
        if q.qsize() <= 10:
            url = 'http://svip.kuaidaili.com/api/getproxy/?orderid=927200326076035&num=2000&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_ha=1&sp1=1&sp2=1&quality=2&format=json&sep=1'
            s = urllib2.urlopen(url, timeout=1000).read()
            j = json.loads(s)
            if 'code' in j and j['code'] == 0:
                for f in j['data']['proxy_list']:
                    q.put(f)
        item = q.get()
        request.meta['proxy'] = 'http://%s' % (item)
#        patch = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})')
#        match = pattern.search(item)
#        if match:
#            front = match.group(1)
#            end = match.group(2)
#            request.meta['proxy'] = 'http://%s:%s' % (front,end)
#        else:
#            print 'Some Error Happens!'
