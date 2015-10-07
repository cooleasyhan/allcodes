import time
import logging


logging.basicConfig( level= logging.INFO, 
                 format = '[-%(levelname)s-] [%(threadName)s] [%(process)d] %(asctime)s [line:%(lineno)d] %(message)s' , 
                 filename = '/tmp/supervisortest.log' ,
                 filemode = 'a') 

n = 1
while n<1000:
	n += 1
	time.sleep(5)

	logging.info('sec test case is running');
