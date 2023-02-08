#Author:Elin 
#Create Time:2023-02-08 21:55:41
#Last Modified By:Elin
#Update Time:2023-02-08 21:55:41
  
import os
from datetime import datetime

timer = datetime.now().__str__().replace(" ","")
excute_cmd = f"nohup python server.py >> ../log/{timer}.log &"
os.system(excute_cmd)
exit(1)