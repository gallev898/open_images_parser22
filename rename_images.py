import os

img_class_folder = 'Book'
img_class = 'Beaker'
img_folder = 'images'
# img_folder = os.path.join('images', img_class_folder)

images = []

idx = 0
for img in os.listdir(img_folder):
    os.rename(os.path.join(img_folder,img), os.path.join(img_folder,img_class+'_'+str(idx)+'.jpg'))
    idx += 1

