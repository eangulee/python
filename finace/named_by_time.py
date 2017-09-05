import datetime  
import re  
import os  
  
  
projectName='Mate 8'  
filename="../"+projectName+"_PicsDetectedResults_" + re.sub(r'[^0-9]','_',str(datetime.datetime.now())) + '.xml'  
print(filename)