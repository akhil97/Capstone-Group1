import os
import shutil

# get your local directory
city_name = 'nairobi'

# Get your local directory and create a folder with the city name
local_dir = os.getcwd()
local_dir = os.path.join(local_dir, city_name)

#will cretae folder with city name in your local
local_dir = os.path.join(local_dir,city_name)
layer0_1_dir=['raw_images','cloud_free_images']
layer0_2_dir=['ob_images']
layer0_3_dir=['Mixed_data']
layer0_4_dir=['results']
layer1_dir=['tif','png']
layer2_dir=['train','test']
layer3_dir=['0','1']
layer0_1_1_dir=['raw_images','ob_images']
layer2_1_dir=['train','test','validation']

#check if the folder is not exists then create all folders
def check_local_dir(local_dir_name):
    if not os.path.exists(local_dir_name):
       os.makedirs(local_dir_name)
       for l0_1 in layer0_1_dir:
           d0=os.path.join(local_dir_name,l0_1)
           os.makedirs(d0)
           for l1 in layer1_dir:
               d1=os.path.join(d0,l1)
               os.makedirs(d1)
               for l2 in layer2_dir:
                   d2 = os.path.join(d1, l2)
                   os.makedirs(d2)
                   for l3 in layer3_dir:
                       d3 = os.path.join(d2, l3)
                       os.makedirs(d3)
       for l0_2 in layer0_2_dir:
           d0=os.path.join(local_dir_name,l0_2)
           os.makedirs(d0)
           for l2 in layer2_dir:
              d1 = os.path.join(d0, l2)
              os.makedirs(d1)
              for l3 in layer3_dir:
                d3 = os.path.join(d1, l3)
                os.makedirs(d3)
       for l0_3 in layer0_3_dir:
           d0=os.path.join(local_dir_name,l0_3)
           os.makedirs(d0)
           for l1 in layer0_1_1_dir:
               d1=os.path.join(d0,l1)
               os.makedirs(d1)
               for l2 in layer2_1_dir:
                   d2 = os.path.join(d1, l2)
                   os.makedirs(d2)
       for l0_4 in layer0_4_dir:
           d0=os.path.join(local_dir_name,l0_4)
           os.makedirs(d0)
    else:
        shutil.rmtree(local_dir_name)
        check_local_dir(local_dir_name)


check_local_dir(local_dir)

#change to correct folder if needed
# for accra data change to this '/home/ubuntu/accra'
remote_dir = '/home/ubuntu/Capstone/nairobi'
