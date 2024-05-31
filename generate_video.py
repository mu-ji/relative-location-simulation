import cv2
import os

# 设置输出视频的参数
fps = 30
size = (640, 480)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_file = 'output_video.mp4'

# 创建视频写入器
video_writer = cv2.VideoWriter(output_file, fourcc, fps, size)

# 遍历figure_buffer文件夹中的所有图片
image_files = os.listdir('figure_buffer')
image_files.sort()

image_file = 'start_states.png'
image_path = os.path.join('figure_buffer', image_file)
image = cv2.imread(image_path)
# 将每个图片显示30帧
for i in range(30):
    video_writer.write(image)

steps = 1
while True:

    image_file = 'step{}.png'.format(steps)
    image_path = os.path.join('figure_buffer', image_file)

    if os.path.exists(image_path):
        image = cv2.imread(image_path)
        
        # 将每个图片显示30帧
        for i in range(10):
            video_writer.write(image)
        
        steps = steps + 1
    else:
        break


image_file = 'corrected_state.png'
image_path = os.path.join('figure_buffer', image_file)
image = cv2.imread(image_path)
# 将每个图片显示30帧
for i in range(30):
    video_writer.write(image)

# 释放视频写入器
video_writer.release()
print('视频生成完成!')