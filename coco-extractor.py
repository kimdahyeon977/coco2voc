from pycocotools.coco import COCO # pip install pycocotools
from xml.etree.ElementTree import Element, SubElement, ElementTree
import requests
import os
import sys
import threading

def makeDirectory(dirName):
    try:
        os.mkdir(dirName)
        print(f"\nMade {dirName} Directory.\n")
    except:
        pass

def getImagesFromClassName(className):
    makeDirectory(f'overload_images/{className}')
    catIds = coco.getCatIds(catNms=[className])
    imgIds = coco.getImgIds(catIds=catIds )
    images = coco.loadImgs(imgIds)

    print(f"Total Images: {len(images)} for class '{className}'")

    for im in images:
        image_file_name = im['file_name']
        label_file_name = im['file_name'].split('.')[0] + '.xml'

        fileExists = os.path.exists(f'overload_images/{className}/{image_file_name}')
        if(not fileExists):
            img_data = requests.get(im['coco_url']).content
            annIds = coco.getAnnIds(imgIds=im['id'], catIds=catIds, iscrowd=None)
            anns = coco.loadAnns(annIds)    
            print(f"{className}. Downloading - {image_file_name}")
            for i in range(len(anns)):
                # Yolo Format: center-x center-y width height
                # All values are relative to the image.
                xmin = int(anns[i]['bbox'][0])
                ymin = int(anns[i]['bbox'][1])
                xmax = int(anns[i]['bbox'][0] + anns[i]['bbox'][2]) 
                ymax = int(anns[i]['bbox'][1] + anns[i]['bbox'][3]) 
                filename=image_file_name
                label='healthy'
                root = Element('annotation')
                SubElement(root, 'folder').text = image_file_name
                SubElement(root, 'filename').text = filename 
                SubElement(root, 'path').text = './object_detection/images' +  filename
                source = SubElement(root, 'source')
                SubElement(source, 'database').text = 'Unknown'
                size = SubElement(root, 'size')
                SubElement(size, 'width').text = str(im['width'])
                SubElement(size, 'height').text = str(im['height'])
                SubElement(size, 'depth').text = '3'
                
                SubElement(root, 'segmented').text = '0'
                
                obj = SubElement(root, 'object')
                SubElement(obj, 'name').text = label
                SubElement(obj, 'pose').text = 'Unspecified'
                SubElement(obj, 'truncated').text = '0'
                SubElement(obj, 'difficult').text = '0'
                anns[i]['bbox'] = SubElement(obj, 'bndbox')
                SubElement(anns[i]['bbox'], 'xmin').text = str(xmin)
                SubElement(anns[i]['bbox'], 'ymin').text = str(ymin)
                SubElement(anns[i]['bbox'], 'xmax').text = str(xmax)
                SubElement(anns[i]['bbox'], 'ymax').text = str(ymax)
                
                tree = ElementTree(root)
            with open(f'overload_images/{className}/{image_file_name}', 'wb') as image_handler:
                image_handler.write(img_data)
            with open(f'overload_images/{className}/{label_file_name}', 'wb') as file:
                tree.write(file, encoding='utf-8', xml_declaration=True)
                
        else:
           print(f"{className}. {image_file_name} - Already Downloaded.")

argumentList = sys.argv

classes = argumentList[1:]

classes = [class_name.lower() for class_name in classes] # Converting to lower case


if(classes[0] == "--help"):
    with open('classes.txt', 'r') as fp:
        lines = fp.readlines()
    print("**** Classes ****\n")
    [print(x.split('\n')[0]) for x in lines]
    exit(0)     

print("\nClasses to download: ", classes, end = "\n\n")

makeDirectory('overload_images')

coco = COCO('instances_train2017.json')
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]

for name in classes:
    if(name not in nms):
        print(f"{name} is not a valid class, Skipping.")
        classes.remove(name)

threads = []

# Creating threads for every class provided.
for i in range(len(classes)):
    t = threading.Thread(target=getImagesFromClassName, args=(classes[i],)) 
    threads.append(t)
    
for t in threads:
    t.start()

for t in threads:
    t.join()

print("Done.")
