from waitress import serve
from ObticTodo.wsgi import application 
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO) # will print some usefull info

if __name__ == '__main__':
    serve(application, port='80') # this will run the server on 127.0.0.1:8000


