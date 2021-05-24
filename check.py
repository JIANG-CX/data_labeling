import cv2
import os


path_anchor="anchor"
path_image="img"
path_xml="xml"

anchorlist=os.listdir(path_anchor)
print(len(anchorlist)*2)
#anchorlist=sorted(anchorlist)

for i in range(0,len(anchorlist)*2):#anchorlist:
    #if i!=".DS_Store":
    try:
        img=cv2.imread(path_anchor+"/"+str(i)+".jpg")
        cv2.imshow("frame", img)
    except :
        continue

    key= cv2.waitKey(0)&0xFF
    if key==ord('w'):
        print(i)
        os.remove(path_xml+"/"+str(i)+".xml")
        os.remove(path_image+"/"+str(i)+".jpg")
        os.remove(path_anchor+"/"+str(i)+".jpg")
    elif key==ord('q'):
        break
    else:
        print(i)
        continue

