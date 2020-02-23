import cv2
from utils.cv_plot import plot_kpt, plot_vertices, plot_pose_box
from skimage.io import imread, imsave


image_path = '/data/me/IN_PRNET/t1head.png'


image = imread(image_path)
image_pose = plot_pose_box(image, camera_matrix, kpt)
cv2.imshow('sparse alignment', plot_kpt(image, kpt))
cv2.imshow('dense alignment', plot_vertices(image, vertices))
cv2.imshow('pose', plot_pose_box(image, camera_matrix, kpt))
cv2.waitKey(0)