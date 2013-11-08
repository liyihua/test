import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import websocket
import os
import json

from tornado.options import define, options
import getTemHum as gth


define("port", default=8000, help="run on the given port", type=int)
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": "True",
}

    
class MainHandler(tornado.web.RequestHandler):  
    def get(self):
        self.render("index.html")

class MyWebSocket(websocket.WebSocketHandler):
    def open(self):
        #self.write_message("hi from the server")
        print "open websocket"

    def on_message(self, message):    
        print "websocket received a message:"+message
        self.write_message("you said:"+ message)
        prev_time=float(message)
        j=0
        while j<110:
            pro1 = gth.ProcessScript()
            pro1.RunProcess(1,prev_time)
            #print len(pro1.TimeVector[0])
            #print len(pro1.unpkData.getTemp())
            #print len(pro1.TimeVector[1])
            #print len(pro1.unpkData.getHum())
            if ((len(pro1.TimeVector[0])>0 and len(pro1.TimeVector[1])>0) and (len(pro1.unpkData.getTemp())>0 and len(pro1.unpkData.getHum())>0 )):
               self.write_message(""+str(pro1.TimeVector[0][0])+","+str(pro1.unpkData.getTemp()[0])+","+str(pro1.unpkData.getHum()[0]))
               prev_time=pro1.TimeVector[0][-1]+10.1
            else:
               prev_time+=20.0
            print prev_time
            j+=1
            
        #pro1.TimeVector[0], pro1.unpkData.getTemp()
        #message_parsed= json.loads(message)              
        #username= message_parsed[len(message_parsed)-1]

        #self.write_message(json.dumps({"tree":new_tree,"treeRelation":new_treeRelation,"boxPosition":[]}))
        #index= message_parsed[0]
       
        #for i in range(len(pro1.TimeVector[0])):
           #self.write_message(json.dumps({pro1.TimeVector[0][i]:pro1.unpkData.getTemp()[i]}))
    def on_close(self):
        print "WebSocket closed"
def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", MyWebSocket)

    ],**settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    import time, threading
    main()
