from removebg import RemoveBg
import os
 
rmbg = RemoveBg("hy6r1BdkgFNUuGF16yQnHGZq", "error.log")
path = '%s/picture'%os.getcwd() #图片放到程序的同级文件夹 picture 里面
for pic in os.listdir(path):
    rmbg.remove_background_from_img_file("%s\%s"%(path,pic))
