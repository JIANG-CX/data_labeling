import os
import xml.etree.ElementTree as ET

import cv2
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString

classes = ["player", "ball"]
add_num = 300

def make_xml(xmin_tuple, ymin_tuple, xmax_tuple, ymax_tuple, image_name, cls_id):

    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'VOC'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = image_name + '.jpg'

    node_object_num = SubElement(node_root, 'object_num')
    node_object_num.text = str(len(xmin_tuple))

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = '1920'

    node_height = SubElement(node_size, 'height')
    node_height.text = '1080'

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'

    for i in range(len(xmin_tuple)):
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = classes[cls_id[i]]
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'

        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(xmin_tuple[i])
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(ymin_tuple[i])
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(xmax_tuple[i])
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(ymax_tuple[i])

    xml = tostring(node_root, pretty_print = True)
    dom = parseString(xml)
    return dom
if __name__ == '__main__':
    mode = 'xml'
    if mode == 'img':
        os.chdir('img')
        dirlist = os.listdir()
        for dir in dirlist:
            index = dir[:-4]
            frame = cv2.imread(dir)
            cv2.imwrite(str(int(index)+add_num)+ '.jpg',frame)

    if mode == 'xml':
        os.chdir('xml')
        dirlist = os.listdir()
        for dir in dirlist:
            in_file = open(dir)
            index = dir[:-4]

            tree = ET.parse(in_file)
            root = tree.getroot()
            xmin_tuple = []
            ymin_tuple = []
            xmax_tuple = []
            ymax_tuple = []
            cls_ids = []
            for obj in root.iter('object'):
                difficult = 0
                if obj.find('difficult') != None:
                    difficult = obj.find('difficult').text
                if obj.find('name').text == 'player':
                    cls_ids.append(1)
                else:
                    cls_ids.append(0)
                xmlbox = obj.find('bndbox')
                xmin_tuple.append(int(xmlbox.find('xmin').text))
                ymin_tuple.append(int(xmlbox.find('ymin').text))
                xmax_tuple.append(int(xmlbox.find('xmax').text))
                ymax_tuple.append(int(xmlbox.find('ymax').text))


            file_xml = make_xml(xmin_tuple,ymin_tuple,xmax_tuple,ymax_tuple,str(int(index)+add_num), cls_ids)
            xml_name = os.path.join(str(int(index)+add_num)+ '.xml')
            with open(xml_name, 'w') as f:
                f.write(file_xml.toprettyxml(indent='\t'))

#269
# in_file = open("xml/1.xml")
# os.chdir('xml')
# dirlist = os.listdir()
# for dir in dirlist:
#     in_file = open(dir)
#     tree = ET.parse(in_file)
#     root = tree.getroot()
#     xmin_tuple=[]
#     ymin_tuple=[]
#     xmax_tuple=[]
#     ymax_tuple=[]
#     cls_ids = []
#     for obj in root.iter('object'):
#         difficult = 0
#         if obj.find('difficult')!=None:
#             difficult = obj.find('difficult').text
#         if obj.find('name').text == 'player':
#             cls_ids.append(1)
#         else:
#             cls_ids.append(0)
#         xmlbox = obj.find('bndbox')
#         xmin_tuple.append(int(xmlbox.find('xmin').text))
#         ymin_tuple.append(int(xmlbox.find('ymin').text))
#         xmax_tuple(int(xmlbox.find('xmax').text))
#         ymax_tuple(int(xmlbox.find('ymax').text))
#
#
#
#
#
#
#
#         if cls not in classes or int(difficult) == 1:
#             continue
#         cls_id = classes.index(cls)
#
#
#
#         xmlbox = obj.find('bndbox')
#         b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text),
#              int(xmlbox.find('ymax').text))
#         list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
#
#     def convert_annotation(year, image_id, list_file):
#         in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml' % (year, image_id), encoding='utf-8')
#         tree = ET.parse(in_file)
#         root = tree.getroot()
#
#         for obj in root.iter('object'):
#             difficult = 0
#             if obj.find('difficult') != None:
#                 difficult = obj.find('difficult').text
#
#             cls = obj.find('name').text
#             if cls not in classes or int(difficult) == 1:
#                 continue
#             cls_id = classes.index(cls)
#             xmlbox = obj.find('bndbox')
#             b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text),
#                  int(xmlbox.find('ymax').text))
#             list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
#
#
#     wd = getcwd()
#
#     for year, image_set in sets:
#         image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt' % (year, image_set)).read().strip().split()
#         list_file = open('%s_%s.txt' % (year, image_set), 'w')
#         for image_id in image_ids:
#             list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg' % (wd, year, image_id))
#             convert_annotation(year, image_id, list_file)
#             list_file.write('\n')
#         list_file.close()
