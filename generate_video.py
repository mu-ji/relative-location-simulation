import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import cv2
import PIL.Image as Image
 
fps =20# 视频帧率
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_path='picture2video.mp4'
videoWriter = cv2.VideoWriter(video_path, fourcc, fps, (2400,800)) #尺寸为(2400,800)与图片尺寸保持一致
 
 
for i in range(0,200):
    '''绘图'''
    #1. 数据生成
    x = np.random.normal(0, 1, 10)
    y = np.random.normal(0, 1, 10)
	#2.画布设置：
    plt.figure(figsize=(30, 10), dpi=80)#尺寸为(30*80,10*80)与视频尺寸保持一致
    axes=plt.subplot2grid((1,1), (0,0), facecolor='w')
    #3.绘制散点图
    plt.scatter(x,y, c='red', s=500)
    #4.保存图片
    canvas = FigureCanvasAgg(plt.gcf())
    # 绘制图像
    canvas.draw()
    # 获取图像尺寸
    w, h = canvas.get_width_height()
    # 解码string 得到argb图像
    buf = np.fromstring(canvas.tostring_argb(), dtype=np.uint8)
    # 重构成w h 4(argb)图像
    buf.shape = (w, h, 4)
    # 转换为 RGBA
    buf = np.roll(buf, 3, axis=2)
    # 得到 Image RGBA图像对象 (需要Image对象的同学到此为止就可以了)
    image = Image.frombytes("RGBA", (w, h), buf.tostring())
    # 转换为numpy array rgba四通道数组
    image = np.asarray(image)
    # 转换为rgb图像
    rgb_image = image[:, :, :3]
    # 转换为bgr图像
    r,g,b=cv2.split(rgb_image)
    img_bgr = cv2.merge([b,g,r])
    '''生成视频'''
    videoWriter.write(img_bgr)
    '''释放内存'''
    plt.clf()
    plt.close()