import cv2
import os
import shutil
import re

# 设置文件夹路径和tmp文件夹
image_folder = "saveimage"
tmp_folder = "tmp"

# 创建tmp文件夹（如果不存在）
if not os.path.exists(tmp_folder):
    os.makedirs(tmp_folder)

# 获取文件夹中所有图像文件的列表并按照数字部分排序
image_files = [f for f in os.listdir(image_folder) if re.match(r'left_\d+\.jpg', f)]
image_files.sort(key=lambda x: int(re.search(r'left_(\d+)\.jpg', x).group(1)))

index = 0

# 创建一个窗口
cv2.namedWindow("Image Pair", cv2.WINDOW_NORMAL)

while True:
    if index < 0:
        index = 0
    elif index >= len(image_files):
        break

    left_image_path = os.path.join(image_folder, image_files[index])
    right_image_path = os.path.join(image_folder, image_files[index].replace("left_", "right_"))

    left_image = cv2.imread(left_image_path)
    right_image = cv2.imread(right_image_path)

    if left_image is not None and right_image is not None:
        # 缩小图像大小为一半
        left_image = cv2.resize(left_image, (0, 0), fx=0.5, fy=0.5)
        right_image = cv2.resize(right_image, (0, 0), fx=0.5, fy=0.5)

        # 合并两张图像并显示在一个窗口中
        combined_image = cv2.hconcat([left_image, right_image])
        cv2.imshow("Image Pair", combined_image)

        # 打印当前显示的左右图像的名称和路径
        print(f"Current Left Image: {image_files[index]}")
        print(f"Left Image Path: {left_image_path}")
        print(f"Current Right Image: {image_files[index].replace('left_', 'right_')}")
        print(f"Right Image Path: {right_image_path}")

        key = cv2.waitKey(0)

        if key == ord("s"):
            shutil.copy(left_image_path, os.path.join(tmp_folder, image_files[index]))
            shutil.copy(right_image_path, os.path.join(tmp_folder, image_files[index].replace("left_", "right_")))
        elif key == ord("q"):
            index += 1  # 显示下一张图像
        else:
            index += 1  # 显示下一张图像

    cv2.destroyAllWindows()

# 清理临时文件夹（如果需要）
# shutil.rmtree(tmp_folder)

