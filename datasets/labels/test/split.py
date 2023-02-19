#Author:Elin 
#Create Time:2023-02-19 09:30:48
#Last Modified By:Elin
#Update Time:2023-02-19 09:30:48
import shutil as st
import os
from tqdm import tqdm
train_percent = 0.5
val_percent = 0.3
test_percent = 0.2
for root,path,files in os.walk("."):
    labels = files
    try:
        train_num = int(len(labels)*train_percent)
        val_num = int(len(labels)*val_percent)
        test_num = int(len(labels)*test_percent)
        train_files = labels[:train_num]
        val_files = labels[train_num:train_num+val_num]
        test_files = labels[train_num+val_num:]
        for i in tqdm(range(len(train_files)),desc="moving train files",unit="labels"):
            st.move(train_files[i],"./train")
        for i in tqdm(range(len(val_files)),desc="moving val files",unit="labels"):
            st.move(val_files[i],"./val")
        for i in tqdm(range(len(test_files)),desc="moving test files",unit="labels"):
            st.move(test_files[i],"./test")
    except Exception:
        exit(0)