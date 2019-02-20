# -*- coding: utf-8 -*-
import urllib2
import time
import sys
import threading
import json
import copy
import uuid


QUERY_FILE = '/data/home/plorywang/music/tingting_sorted'
GET_REQUEST_URL = 'http://100.96.22.210:13313/my_api?q=%s'

POST_REQUEST_URL = 'http://100.96.22.210:13313/my_api'

POST_REQUEST_URL = 'http://%s:%d/emotion'
POST_DATA = {"utterances": "我我爱你", "time_out":200}


L5MODID = None

#EMOTION BERT
L5MODID = 64617153
L5CMDID = 65536

finished_num = 0
total_time = 0
lock = threading.Lock()

def multi_thread_test(thread_num, request_num, test_func):
    global finished_num, total_time
    threads = []
    for i in xrange(thread_num):
        t = threading.Thread(target=test_func, args=(i, request_num))
        t.setDaemon(True)
        t.start()
        threads.append(object)
    every_seconds_report = 10
    check_point = 5
    start = time.time()
    while True:
        time_used = time.time() - start
        if time_used > check_point:
            check_point += every_seconds_report
            print 'qps:%.2f, average_time:%.2f'%(finished_num / time_used, total_time * 1000 / finished_num)

def test_get(thread_id, request_num):
    global finished_num, total_time, lock
    num = 0
    while num < request_num:
        with open(QUERY_FILE) as ifile:
            for idx, line in enumerate(ifile):
                if num >= request_num:
                    break
                num += 1
                q = urllib2.quote(line.strip().split('\t')[0])
                request_url = GET_REQUEST_URL
                start = time.time()
                if L5MODID is not None:
                    ip, port = l5.get_ip_port(L5MODID, L5CMDID, print_log=False)
                    if port < 0:
                        print 'request L5 failed. %d:%d'%(L5MODID, L5CMDID)
                        continue
                    else:
                        request_url = request_url%(ip, port, q)
                else:
                    request_url = request_url % q
                try:
                    res = urllib2.urlopen(request_url, timeout = 10).read()
                except Exception, what:
                    print str(what)
                    continue
                time_used = time.time() - start
                with lock:
                    finished_num += 1
                    total_time += time_used

def test_post(thread_id, request_num):
    global finished_num, total_time, lock
    opener = urllib2.build_opener()
    num = 0
    while num < request_num:
        with open(QUERY_FILE) as ifile:
            for idx, line in enumerate(ifile):
                if num >= request_num:
                    break
                num += 1
                post_data = copy.copy(POST_DATA)
                #post_data['question'] = line.strip()
                #post_data['str_uin'] = str(uuid.uuid4())
                if 'q' in post_data:
                    post_data['q'] = line.strip().split('\t')[0]
                if 'utterance' in post_data:
                    post_data['utterance'] = line.strip().split('\t')[0]
                if 'utterances' in post_data:
                    post_data['utterance'] = line.strip().split('\t')[0]
                senddata = json.dumps(post_data)
                headers = {}
                headers['Content-Length'] = len(senddata)

                request_url = POST_REQUEST_URL
                start = time.time()
                if L5MODID is not None:
                    ip, port, ret, qos = l5.get_ip_port(L5MODID, L5CMDID, print_log=False)
                    if port < 0:
                        print 'request L5 failed. %d:%d'%(L5MODID, L5CMDID)
                        continue
                    else:
                        request_url = request_url%(ip, port)
                request = urllib2.Request(url=request_url, data=senddata, headers=headers)
                try:
                    response = opener.open(request).read()
                    response = eval(response)
                    if 'ret' in response and response['ret'] != 0:
                        print ip, port, response
                        sys.stdout.flush()
                    #print response
                except Exception, what:
                    print str(what), request_url
                    continue
                time_used = time.time() - start
                if L5MODID is not None:
                    l5.update_l5(ret, qos, int(time_used * 1000))
                with lock:
                    finished_num += 1
                    total_time += time_used


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'python yali_test_tool.py thread_num request_num [post/get]'
        exit(1)
    thread_num = int(sys.argv[1])
    request_num = int(sys.argv[2])
    mode = 'get'
    if len(sys.argv) == 4:
        mode = sys.argv[3].lower()
    if mode == 'post':
        test_func = test_post
    else:
        test_func = test_get
    multi_thread_test(thread_num, request_num, test_func)
