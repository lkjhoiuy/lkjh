import http.server
import socketserver
import os

from pprint import pprint

import json
import lkjh.sites.ma as ma_
import lkjh.sites.fj as fj_
ma = ma_.xSite('json');
fj = fj_.xSite('json');

# http://bioportal.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/SocketServer/index.html

PORT = 8234  # 51234 -> redemarrer la box
#~ PORT = 3306  # 51306
PORT = 5900  # 51900
xs = fj

class LkjhHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        rootdir = 'd:/.lkjhdata/libraries/'
        #~ print(self.path)
        pprint(self.client_address)  # (ip, port)
        ip = self.client_address[0]
        if not ip in['127.0.0.1', '193.251.1.43']: return  # 109.69.197.247 ?
        print(self.headers.get('Host'))  # localhost:8000
        print(self.headers.get('User-Agent'))  # Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2101.0 Safari/537.36
        #~ pprint(vars(self.headers))

        resp = b''
        try:
            
            if self.path.endswith('.jpg'):
                f = open(rootdir + '/covers/ma' + self.path, 'rb')  # open requested file

                self.send_response(200)
                self.send_header('Content-type','image/jpeg')
                #~ self.send_header("Content-length", os.stats)
                self.end_headers()

                #send file content to client
                self.wfile.write(f.read())
                f.close()
                return

            p, modelid = self.path[1:].split('/')
            if p == 'model':
                if modelid == 'list':
                    r = xs.models.sortedkeys()
                    s = json.dumps(r, 2)
                    
                    self.send_response(200)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    
                    self.wfile.write(s.encode('utf-8'))
            
                else:
                    #~ print(modelid)
                    r = xs.export_modelupdates(modelid)
                    s = json.dumps(r, 2)
                    
                    self.send_response(200)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    
                    self.wfile.write(s.encode('utf-8'))
            
            return
            
            if self.path.endswith('.html'):
                f = open(rootdir + self.path, 'rb')  # open requested file

                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                #send file content to client
                self.wfile.write(f.read())
                f.close()
                
            elif self.path.endswith('.py'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                r = os.path.exists(rootdir + self.path)
                resp = '{0}'.format(r)
                self.wfile.write(resp.encode('utf-8'))
            
            else:
                resp = b'404'
                self.send_response(404)
                self.send_header('Content-type','text/html')
                self.send_header("Content-length", len(resp))
                self.end_headers()
                
                self.wfile.write(resp)

        except IOError:
            self.send_error(404, 'file not found')
    
def run():
    #~ httpd = socketserver.TCPServer(("127.0.0.1", PORT), LkjhHTTPRequestHandler)
    httpd = socketserver.TCPServer(("", PORT), LkjhHTTPRequestHandler)
    print('running on port', PORT)
    httpd.serve_forever()        

if __name__ == "__main__":
    run()
