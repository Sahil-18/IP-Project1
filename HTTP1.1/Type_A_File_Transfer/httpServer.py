from http.server import BaseHTTPRequestHandler, HTTPServer  
import os
from dotenv import load_dotenv
load_dotenv()

SERVER_ADDRESS = (os.getenv('COMP1_IP'), int(os.getenv('PORT')))
FILE_FOLDER = os.getenv("A_FILES_LOCATION")

class HTTPRequestHandler(BaseHTTPRequestHandler):  
  #handle GET command  
  def do_GET(self):  
    file_path = FILE_FOLDER + self.path
    try:  
        f = open(file_path,  'rb') #open requested file  
        #send code 200 response  
        self.send_response(200)    
        #send header first  
        self.send_header('Content-type', 'text/plain')  
        self.end_headers()  
        self.wfile.write(f.read())
        f.close()  
        return  

    except IOError:  
      self.send_error(404, 'file not found')  

def run():  
  print('http server is starting...')  
  
  #ip and port of servr  
  #by default http server port is 80    
  httpd = HTTPServer(SERVER_ADDRESS, HTTPRequestHandler)  
  print('http server is running...')  
  httpd.serve_forever()  

if __name__ == '__main__':  
  run() 