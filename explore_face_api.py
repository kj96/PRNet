import numpy as np
import os
from glob import glob
import scipy.io as sio
from skimage.io import imread, imsave
from skimage.transform import rescale, resize
from time import time
import argparse
import ast

from api import PRN

from utils.estimate_pose import estimate_pose
from utils.rotate_vertices import frontalize
from utils.render_app import get_visibility, get_uv_mask, get_depth_image
from utils.write import write_obj_with_colors, write_obj_with_texture

def main(args):
    # if args.isShow or args.isTexture:
    #     import cv2
    #     from utils.cv_plot import plot_kpt, plot_vertices, plot_pose_box

    # ---- init PRN
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu # GPU number, -1 for CPU
    prn = PRN(is_dlib = args.isDlib)

    # ------------- load data
    image_folder = args.inputDir
    save_folder = args.outputDir
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    types = ('*.jpg', '*.png')
    image_path_list= []
    for files in types:
        image_path_list.extend(glob(os.path.join(image_folder, files)))
    total_num = len(image_path_list)

    for i, image_path in enumerate(image_path_list):
        print("@ -> ", i)
        name = image_path.strip().split('/')[-1][:-4]

        # read image
        image = imread(image_path)
        [h, w, c] = image.shape
        if c>3:
            image = image[:,:,:3]

        # the core: regress position map
        # if args.isDlib:
        max_size = max(image.shape[0], image.shape[1])
        if max_size> 1000:
            image = rescale(image, 1000./max_size)
            image = (image*255).astype(np.uint8)
        pos = prn.process(image) # use dlib to detect face
        # else:
        #     if image.shape[0] == image.shape[1]:
        #         image = resize(image, (256,256))
        #         pos = prn.net_forward(image/255.) # input image has been cropped to 256x256
        #     else:
        #         box = np.array([0, image.shape[1]-1, 0, image.shape[0]-1]) # cropped with bounding box
        #         pos = prn.process(image, box)
        
        image = image/255.
        if pos is None:
            continue

        # 3D vertices
        vertices = prn.get_vertices(pos)
        save_vertices = vertices.copy()
        save_vertices[:,1] = h - 1 - save_vertices[:,1]


        # corresponding colors
        colors = prn.get_colors(image, vertices)

        # if args.isTexture:
        #     if args.texture_size != 256:
        #         pos_interpolated = resize(pos, (args.texture_size, args.texture_size), preserve_range = True)
        #     else:
        #         pos_interpolated = pos.copy()
        #     texture = cv2.remap(image, pos_interpolated[:,:,:2].astype(np.float32), None, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,borderValue=(0))
        #     if args.isMask:
        #         vertices_vis = get_visibility(vertices, prn.triangles, h, w)
        #         uv_mask = get_uv_mask(vertices_vis, prn.triangles, prn.uv_coords, h, w, prn.resolution_op)
        #         uv_mask = resize(uv_mask, (args.texture_size, args.texture_size), preserve_range = True)
        #         texture = texture*uv_mask[:,:,np.newaxis]
        #     write_obj_with_texture(os.path.join(save_folder, name + '.obj'), save_vertices, prn.triangles, texture, prn.uv_coords/prn.resolution_op)#save 3d face with texture(can open with meshlab)
        # else:
        write_obj_with_colors(os.path.join(save_folder, name + '.obj'), save_vertices, prn.triangles, colors) #save 3d face(can open with meshlab)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Joint 3D Face Reconstruction and Dense Alignment with Position Map Regression Network')

    parser.add_argument('-i', '--inputDir', default='TestImages/', type=str,
                        help='path to the input directory, where input images are stored.')
    parser.add_argument('-o', '--outputDir', default='TestImages/results', type=str,
                        help='path to the output directory, where results(obj,txt files) will be stored.')
    parser.add_argument('--gpu', default='0', type=str,
                        help='set gpu id, -1 for CPU')
    parser.add_argument('--isDlib', default=True, type=ast.literal_eval,
                        help='whether to use dlib for detecting face, default is True, if False, the input image should be cropped in advance')

    main(parser.parse_args())
