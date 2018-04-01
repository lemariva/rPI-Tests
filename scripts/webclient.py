import os, sys, requests
from tqdm import tqdm
from datetime import datetime
import random

url = "http://192.168.178.116:5000/"
FILENAME = "send_statistics.csv"

def send_data(filename=FILENAME):

    try:
        with open(filename, "w") as myfile:
            myfile.write("time,iteration,size,seconds,microseconds\n")
            
        for iteration in tqdm(range(100000)):
            idx = random.randint(0, 10)
            # open file and get information
            fin = open('images/image'+str(idx)+'.jpg', 'rb')
            statinfo = os.stat('images/image'+str(idx)+'.jpg')
            size = statinfo.st_size
            # making array to send
            files = {'file': fin, 'name': 'image'+str(idx)+'.jpg'}#
            
            # sending data and check timing
            start_time = datetime.now()   
            r = requests.post(url, files=files)
            script_time = datetime.now() - start_time
            
            # saving statistics
            seconds = script_time.seconds
            microseconds = script_time.microseconds
            
            now = datetime.now()
            now_epoch = now.strftime('%s')   
            
            with open(filename, "a") as myfile:
                myfile.write("%s, %d, %d, %d, %d\n" %(now_epoch, iteration, size, seconds, microseconds))

    finally:
        print("END")
    
if __name__ == "__main__":    
    if len(sys.argv) < 2:
        print('please enter a file name')
    else:
        filename = str(sys.argv[1])
        send_data(filename)
    

        
    
        