#-*- coding: UTF-8 -*-
import sys
from pred_inupt import intent
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from socketserver import ThreadingMixIn
import urllib,re,urllib.parse
import time
import json


class mySoapServer(BaseHTTPRequestHandler):
    def do_head(self):
        pass

    def do_GET(self):
        try:
            self.protocal_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Welcome", "Contect")
            self.send_header("Content-Type", "text/html;charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            templateStr = '''
            <!DOCTYPE HTML><html>
            <meta charset="utf-8">
            <head><title>Get page</title></head>
            <body>
            <form		action="post_word"	method="post" >
            TYPE:<br>
            <input type="text"		name="TYPE"		/><br>
            VALUE:<br>
            <input type="text"		name="SENTENCE"	/><br>
            <input type="submit"	value="SUBMIT"	/>
            </form></body> </html>
            '''
            self.wfile.write(bytes(templateStr.encode(encoding='utf_8')))
        except IOError:
            self.send_error(404, message=None)

    def do_POST(self):
        try:
            self.send_response(200, message=None)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            datas = self.rfile.read(int(self.headers['content-length'])).decode("utf-8", 'ignore')
            # datas = urllib.unquote(datas).decode("utf-8", 'ignore')
            datasde = urllib.parse.unquote(datas)
            pattern = re.compile(r'TYPE=([^\&]*)\&SENTENCE=(.*)')
            match = pattern.match(datasde)
            if match:
                group_1 = match.group(1)
                group_2 = match.group(2)
                if group_1.upper() == 'CHAR_CNN':
                    start = time.time()
                    result = intent(group_2).result
                    data1 = set()
                    data1.add("domain: " + result)
                    data0 = {}
                    data0["type"] = "customdat]"
                    data0["data"] = data1
                    resultJson = {}
                    resultJson['flag'] = 1
                    resultJson['code'] = 200
                    resultJson['data'] = data0

                    resultJson ="{code: 200,data: {"+"domain: " + result+ "},Type: "+"CHAR_CNN"+",src_txt: "+ group_2 +"}"
                    self.jsonStr = json.dumps(resultJson, ensure_ascii=False)
                    print(u'CHAR_CNN：%s  %s srtart:%s end:%s 耗时： %s' % (group_2, resultJson, start,time.time(),time.time() - start))
                    self.wfile.write(bytes(resultJson.encode(encoding='gbk')))
        except IOError:
            self.send_error(404, message=None)


class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':

    myServer = ThreadingHttpServer(('', 8181), mySoapServer)
    myServer.serve_forever()
    myServer.server_close()