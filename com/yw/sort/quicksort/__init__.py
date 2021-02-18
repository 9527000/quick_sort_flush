# coding=UTF-8
from com.yw.sort.quicksort.sortmain import Gui

FPS = 80            # 帧率
WIN_WIDTH = 1250    # 窗口宽度
WIN_HEIGHT = 600    # 窗口高度
if __name__ == '__main__':
    array = [1,3,7,6,5,2,4,9]  # 初始化数组
    # array = [5,2,3,4,1,6,7,8,9]  # 初始化数组
    gui = Gui(WIN_WIDTH, WIN_HEIGHT,FPS,array)
    gui.loop()