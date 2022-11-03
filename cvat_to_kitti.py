#------------------------------------------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------------------------------------------
from itertools import count
from re import sub
import xml.etree.ElementTree as ET
import os
import numpy as np

#<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\
#<!DOCTYPE boost_serialization>\
#<boost_serialization version="9" signature="serialization::archive">',
#</boost_serialization>
root = ET.Element('tracklets')
# Set tracklets
root.set('version', '0')
root.set('tracking_level', '0')
root.set('class_id', '0')
# Set count
cnt = ET.SubElement(root, 'count')
# Set item version
item_version = ET.SubElement(root, 'item_version')
item_version.text = '1'

# Loop over files in the directory
i = 0
tot_score = 0
frame = 1
for filename in os.listdir('./results'):
    # Loop over the lines of the file
    with open('./results/' + filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # Create Item
            item = ET.SubElement(root, 'item')
            # Split the line into the different parts
            line = line.split(' ')
            # Collect KITTI data
            type = line[0]
            truncated = line[1]
            occluded = line[2]
            alpha = line[3]
            bbox = line[4:8]
            dimensions = line[8:11]
            location = line[11:14]
            rotation_y = line[14]
            score = float(line[15])
            tot_score += score
            print("Score", score)
        
            # Set item
            objectType = ET.SubElement(item, 'objectType')
            objectType.text = type
            h = ET.SubElement(item, 'h')
            h.text = dimensions[0]
            w = ET.SubElement(item, 'w')
            w.text = dimensions[2]
            l = ET.SubElement(item, 'l')
            l.text = dimensions[1]
            first_frame = ET.SubElement(item, 'first_frame')
            first_frame.text = str(frame)         
            # Create poses
            poses = ET.SubElement(item, 'poses')
            cnt_ = ET.SubElement(poses, 'count')
            cnt_.text = '1'
            item_version = ET.SubElement(poses, 'item_version')
            item_version.text = '0'
            # Create subItem
            subitem = ET.SubElement(poses, 'item')
            tx = ET.SubElement(subitem, 'tx')
            tx.text = location[0]
            ty = ET.SubElement(subitem, 'ty')
            ty.text = location[1]
            tz = ET.SubElement(subitem, 'tz')
            tz.text = location[2]
            rx = ET.SubElement(subitem, 'rx')
            rx.text = '0'
            ry = ET.SubElement(subitem, 'ry')
            ry.text = '0'
            rz = ET.SubElement(subitem, 'rz')
            rz.text = rotation_y
            state = ET.SubElement(subitem, 'state')
            state.text = '2'
            occlusion = ET.SubElement(subitem, 'occlusion')
            occlusion.text = occluded
            occlusion_kf = ET.SubElement(subitem, 'occlusion_kf')
            occlusion_kf.text = occluded
            truncation = ET.SubElement(subitem, 'truncation')
            truncation.text = truncated
            amt_occlusion = ET.SubElement(subitem, 'amt_occlusion')
            amt_occlusion.text = '-1'
            amt_border_l = ET.SubElement(subitem, 'amt_border_l')
            amt_border_l.text = '-1'
            amt_border_r = ET.SubElement(subitem, 'amt_border_r')
            amt_border_r.text = '-1'
            amt_occlusion_kf = ET.SubElement(subitem, 'amt_occlusion_kf')
            amt_occlusion_kf.text = '-1'
            amt_border_kf = ET.SubElement(subitem, 'amt_border_kf')
            amt_border_kf.text = '-1'
            # Set finished
            finished = ET.SubElement(item, 'finished')
            finished.text = '1'
            
            i += 1
    frame += 1


# Set subItem
subitem.set('version', '1')
subitem.set('tracking_level', '0')
subitem.set('class_id', '3')

# Set poses
poses = ET.SubElement(item, 'poses')
poses.set('version', '0')
poses.set('tracking_level', '0')
poses.set('class_id', '2')

# Set item data
item.set('version', '1')
item.set('tracking_level', '0')
item.set('class_id', '1')

# Set count
cnt.text = str(i)

# Save the XML file
tree = ET.ElementTree(root)
tree.write('tracklet_labels_prediction.xml', encoding='UTF-8', xml_declaration=True)

# Show average score
print("Average score", tot_score/i)



            
