#------------------------------------------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------------------------------------------
import xml.etree.ElementTree as ET
import os
import numpy as np

def limit_period(val, offset=0.5, period=np.pi):
    """Limit the value into a period for periodic function.

    Args:
        val (torch.Tensor | np.ndarray): The value to be converted.
        offset (float, optional): Offset to set the value range.
            Defaults to 0.5.
        period ([type], optional): Period of the value. Defaults to np.pi.

    Returns:
        (torch.Tensor | np.ndarray): Value in the range of
            [-offset * period, (1-offset) * period]
    """
    limited_val = val - np.floor(val / period + offset) * period
    return limited_val

# Pass the path of the xml document 
tree = ET.parse('tracklet_labels.xml') 
frame_list = open('frame_list.txt', 'r')
def_calib = "P0: 7.070493000000e+02 0.000000000000e+00 6.040814000000e+02 0.000000000000e+00 0.000000000000e+00 7.070493000000e+02 1.805066000000e+02 0.000000000000e+00 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 0.000000000000e+00\n" + \
"P1: 7.070493000000e+02 0.000000000000e+00 6.040814000000e+02 -3.797842000000e+02 0.000000000000e+00 7.070493000000e+02 1.805066000000e+02 0.000000000000e+00 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 0.000000000000e+00\n" + \
"P2: 7.070493000000e+02 0.000000000000e+00 6.040814000000e+02 4.575831000000e+01 0.000000000000e+00 7.070493000000e+02 1.805066000000e+02 -3.454157000000e-01 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 4.981016000000e-03\n" + \
"P3: 7.070493000000e+02 0.000000000000e+00 6.040814000000e+02 -3.341081000000e+02 0.000000000000e+00 7.070493000000e+02 1.805066000000e+02 2.330660000000e+00 0.000000000000e+00 0.000000000000e+00 1.000000000000e+00 3.201153000000e-03\n" + \
"R0_rect: 9.999128000000e-01 1.009263000000e-02 -8.511932000000e-03 -1.012729000000e-02 9.999406000000e-01 -4.037671000000e-03 8.470675000000e-03 4.123522000000e-03 9.999556000000e-01\n" + \
"Tr_velo_to_cam: 6.927964000000e-03 -9.999722000000e-01 -2.757829000000e-03 -2.457729000000e-02 -1.162982000000e-03 2.749836000000e-03 -9.999955000000e-01 -6.127237000000e-02 9.999753000000e-01 6.931141000000e-03 -1.143899000000e-03 -3.321029000000e-01\n" + \
"Tr_imu_to_velo: 9.999976000000e-01 7.553071000000e-04 -2.035826000000e-03 -8.086759000000e-01 -7.854027000000e-04 9.998898000000e-01 -1.482298000000e-02 3.195559000000e-01 2.024406000000e-03 1.482454000000e-02 9.998881000000e-01 -7.997231000000e-01\n"

# get the parent tag 
root = tree.getroot() 
velo_paths = frame_list.readlines()
# print the attributes of the first tag  
for i in range(int(root[0][0].text)):
    velo_path = velo_paths[int(root[0][2+i][4].text)].split(' ')[1].rstrip('\n')
    
    os.system("cp exampleImage.png ./image_2/" + velo_path.replace('.', '') + ".png")

    calib_flie = open("calib/"+velo_path.replace('.', '')+".txt", 'w')
    calib_flie.write(def_calib)
    calib_flie.close()

    label_2_file = open("label_2/"+velo_path.replace('.', '')+".txt", 'a')
    label_2 = root[0][2+i][0].text + " " # type
    label_2 += root[0][2+i][5][2][9].text + " " # truncation
    label_2 += root[0][2+i][5][2][7].text + " " # occlusion
    label_2 += root[0][2+i][5][2][5].text + " " # alpha
    label_2 += "712.40 143.00 810.73 307.92 " # bbox2d
    if ( 1 == 2 ):
        label_2 += root[0][2+i][2].text + " " + root[0][2+i][1].text + " " + root[0][2+i][3].text + " " # bbox3d (dim)
        label_2 += str(-float(root[0][2+i][5][2][1].text)) + " " + str(-float(root[0][2+i][5][2][2].text)) + " " + root[0][2+i][5][2][0].text + " " # bbox3d (loc)
        yaw = float(root[0][2+i][5][2][5].text)
        yaw = round(limit_period(-yaw - np.pi / 2, period=np.pi * 2),4)
        label_2 += str(yaw) + "\n" # bbox3d (rot_y)
    else:
        label_2 += root[0][2+i][1].text + " " + root[0][2+i][3].text + " " + root[0][2+i][2].text + " " # bbox3d (dim)
        label_2 += root[0][2+i][5][2][0].text + " " + root[0][2+i][5][2][1].text + " " + root[0][2+i][5][2][2].text + " " # bbox3d (loc)
        label_2 += root[0][2+i][5][2][5].text + "\n" # bbox3d (rot_y)
    
    label_2_file.write(label_2)
    label_2_file.close()

    os.system("mv  velodyne/" + velo_path + '.bin' + " velodyne/" + velo_path.replace('.', '') + ".bin > /dev/null 2>&1")
