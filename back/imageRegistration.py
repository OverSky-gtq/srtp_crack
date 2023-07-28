import math
import os

import cv2 as cv
import numpy as np


# 裁剪图像周围的黑色部分
def crop_image(image):
    # 将图像转换为灰度图
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # 获取图像的高度和宽度
    height, width = gray.shape

    # 定义中心区域的尺寸和边界
    center_width = width // 2
    center_height = height // 2
    scan_radius = min(center_width, center_height)
    y_start = center_height - scan_radius
    y_end = center_height + scan_radius
    x_start = center_width - scan_radius
    x_end = center_width + scan_radius

    # 扫描图像找到最小水平矩形的边界值
    x_min = width
    y_min = height
    x_max = 0
    y_max = 0
    for y in range(y_start, y_end):
        row = gray[y, x_start:x_end]
        if np.any(row != 0):
            non_zero_indices = np.nonzero(row)[0]
            x_min = min(x_min, non_zero_indices[0] + x_start)
            x_max = max(x_max, non_zero_indices[-1] + x_start)
            y_min = min(y_min, y)
            y_max = max(y_max, y)

    # 裁剪图像
    cropped_image = image[y_min:y_max + 1, x_min:x_max + 1]

    return cropped_image


# 提取两张图像的特征点和特征描述符
def detect_sift(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 创建SIFT对象
    sift = cv.SIFT_create()
    # 检测关键点和计算描述符
    result = sift.detectAndCompute(gray, None)
    return result


# 匹配特征点，提取较好的点对
def get_good_matches(des1, des2):
    # 创建FLANN匹配器
    flann = cv.FlannBasedMatcher()

    # 匹配关键点
    matches = flann.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good_matches.append(m)
    return good_matches, m


# 变换，拼接图片
def image_stitching(img1_path, img2_path, output_path='result.jpg'):
    img1 = cv.imread(img1_path)
    img2 = cv.imread(img2_path)
    (kp1, des1) = detect_sift(img1)
    (kp2, des2) = detect_sift(img2)
    good_matches, m = get_good_matches(des1, des2)

    if len(good_matches) <= 4:
        print("failed")
        return False

    # 提取匹配的特征点坐标
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # 估计变换矩阵
    H, status = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

    # 矩形图片最大长度为斜边长度，因为只有img1在变换，所以只需计算diagonal1
    h1, w1, _ = img1.shape
    h2, w2, _ = img2.shape
    diagonal1 = int(math.sqrt(h1 * h1 + w1 * w1))

    # 构建平移矩阵，向右下移动，避免溢出画布的情况
    T = np.array([[1.0, 0, diagonal1],
                  [0, 1.0, diagonal1],
                  [0, 0, 1.0]])
    H = np.dot(T, H)

    # 计算拼接后可能用到的最大画布
    size = (2 * diagonal1 + w2, 2 * diagonal1 + h2)

    warped_image = cv.warpPerspective(img1, H, size)
    # img2归位（需要平移同样的单位）
    warped_image[diagonal1:diagonal1 + h2, diagonal1:diagonal1 + w2] = img2
    result = crop_image(warped_image)
    cv.imwrite(output_path, result)
    return True


def multi_image_stitching(path, output_path='result.jpg'):
    file_list = os.listdir(path)
    first = os.path.join(path, file_list[0])
    second = os.path.join(path, file_list[1])
    image_stitching(first, second, output_path)


if __name__ == '__main__':
    image_stitching('uploads/A1.jpg', 'uploads/A2.jpg')
