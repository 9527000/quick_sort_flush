# coding=UTF-8
import pygame
import random
import time
FPS = 80            # 帧率
WIN_WIDTH = 1250    # 窗口宽度
WIN_HEIGHT = 600    # 窗口高度
BUBBLE_SPACE = 60   # 气泡之间的间距
INIT_R = 4          # 气泡初始大小（半径）
DR = 2              # 气泡数字值一个单位对应的气泡半径增加量
NUMBER = 7          # 排序数字个数
SLEEP_TIME=0.2      # 移动停顿时间（毫秒）
COLORS = {
    "bg": (255, 255, 255),      # 背景颜色
    "bubble": (0, 120, 160),    # 气泡颜色
    "select": (190, 150, 0),    # 被选择的气泡颜色
    "text": (255, 255, 255),    # 文本颜色
}
pygame.init()                               # pygame 初始化，必须有，且必须在开头
font = pygame.font.SysFont("Arial",20, True)     #气泡上数字的字体、大小、加粗
class Bubble:
    color = COLORS["bubble"]
    def __init__(self, master, x, y, v, r):
        self.isMid=False
        self._master = master   # 父控件
        self.cx = x             # 气泡中心横坐标 - x
        self.cy = y             # 气泡中心纵坐标 - y
        self.v = v              # 气泡内部数字
        self.radius = r         # 气泡半径
    def left(self):             # 气泡左移
        self.cx -= DR
    def right(self):            # 气泡右移
        self.cx += DR
    def move(self, gui, x, y):       # 移动气泡到相应的坐标
        time.sleep(0.3)  # 停顿0.2秒，否则太快了效果不好
        if x-self.cx!=0:
            a= (float(y - self.cy)) / (float(x - self.cx))
            b= self.cy - a * self.cx
        while True:
            self.cy +=DR
            if x - self.cx != 0 and a!=0:
                self.cx = (self.cy - b) / a
            gui.updatePyGame()
            if  self.cy==y:
                break

    def draw(self, current=False):  # 绘制单个气泡（包括圆及数字），current表示是否当前气泡
        text = font.render(str(self.v), 1, COLORS["text"])
        if current:     #当前气泡
            pygame.draw.circle(self._master, COLORS["select"], (self.cx, self.cy), self.radius)#画圆
        else:           #其它气泡
            pygame.draw.circle(self._master, self.color, (self.cx, self.cy), self.radius)
        text_width = text.get_width()       #数字宽度
        text_height = text.get_height()     #数字高度
        self._master.blit(text, (self.cx - text_width // 2, self.cy - text_height // 2)) #数字附着在圆心


class BubbleManager:  # 管理所有气泡
    def __init__(self, master,hight,isNode, arr=[]):
        self.left=None
        self.right=None
        self.hight=hight
        self.btnList= []
        self._master = master  # 父控件窗体
        self.bubbleList = []  # bubble列表
        self.node=isNode
        if arr:  # 数组
            self.arr = arr
        else:
            self.arr = [i for i in range(1, NUMBER + 1)]
            random.shuffle(self.arr)  # 打乱顺序
        # 根据数组中的数字建立Bubble对象，添加到bubbleList中
        # 注意动画界面是从左到右展示数组的元素的
        right_x = 300  # 上一个气泡最右点到左边界的距离（即其X坐标，等于圆心到左边界的距离加上气泡半径），初始为0
        if isNode:
            for i in range(len(self.arr)):
                v = self.arr[i]
                vr = INIT_R + v * DR  # 气泡半径大小，数字越大、半径越大
                center_x = right_x + BUBBLE_SPACE + vr  # 当前气泡圆心到左边界的距离，等于上一个气泡最右点x坐标+气泡间距+半径
                right_x = center_x + vr  # 记录当前气泡最右点x坐标，供下一个使用
                bubble_i = Bubble(master, center_x, self.hight, v, vr)
                self.bubbleList.append(bubble_i)
        else:
            self.bubbleList=arr
        if len(self.bubbleList)>=2:
            self.j = len(self.bubbleList) // 2
            self.mid=self.bubbleList[self.j]
            self.bubbleList[self.j].isMid=True

    def initBuList(self):
        self.bubbleList

    #选择比较基准小球（选择中间值，也可以选择第一个或者最后一个）
    def select(self,gui):
        time.sleep(0.5)  # 停顿0.2秒，否则太快了效果不好
        yy=self.mid.cy + 100
        while True:
            self.mid.cy+=DR
            gui.updatePyGame()
            if self.mid.cy==yy :
                break
        # self.mid.cy+=100

    #移动当前比较小球大于基准小球
    def dright(self, gui, right, selectBu):
        if len(right)==0:
            referBu=self.mid
        else:
            referBu=right[len(right)-1]
        selectBu.move(gui, referBu.cx+100, referBu.cy)

    #移动当前比较小球小于于基准小球
    def dleft(self, gui, left, selectBu):
        if len(left)==0:
            referBu=self.mid
        else:
            referBu=left[len(left)-1]
        selectBu.move(gui, referBu.cx-100, referBu.cy)

    #移动小球
    # def move(self,gui,select,num,moveSize):
    #     time.sleep(0.3)  # 停顿0.2秒，否则太快了效果不好
    #     xx = select.cx + moveSize
    #     if xx-num.cx!=0:
    #         a=(float(select.cy-num.cy))/(float(xx-num.cx))
    #         b=num.cy-a*num.cx
    #     while True:
    #         num.cy +=DR
    #         if xx - num.cx != 0 and a!=0:
    #             num.cx = (num.cy-b)/a
    #         gui.updatePyGame()
    #         if  num.cy==select.cy:
    #             break


    def draw(self):                     # 绘制所有气泡
        for j in range(len(self.bubbleList)):
            db = self.bubbleList[j]
            db.draw(j==self.j)          #如果是当前气泡，绘制橙色
        if self.left is not None and len(self.left.bubbleList)>=2:
            self.left.draw()
        if self.right is not None and len(self.right.bubbleList)>=2:
            self.right.draw()


    #递归排序借宿，退出递归将所有小球按照排序结果展示
    def rsult(self,gui):
        yy=400
        lastBu=None
        flag = True
        while flag:
            flag=False
            for j in range(len(self.bubbleList)):
                db = self.bubbleList[j]
                if db.cy>yy:
                    db.cy-=DR
                    flag=True
                if db.cy < yy:
                    db.cy += DR
                    flag = True
            gui.updatePyGame()

class Gui:
    def __init__(self, width, height, fps=FPS, arr=[]):
        self.win = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.fps = fps
        pygame.display.set_caption("AAAAAAAAAAAAAAAAAA")
        self.start=False
        self.lefth=100
        self.rightg=100
        self.bm=BubbleManager(self.win, 100,True,arr)

    def quick_sort(self,bmm):
        """快速排序"""
        data = bmm.bubbleList
        if len(data) >= 2:  # 递归入口及出口
            mid = bmm.bubbleList[len(bmm.bubbleList) // 2]  # 选取基准值，也可以选取第一个或最后一个元素sd
            self.updatePyGame()             # 更新显示
            bmm.select(self)                    #移动基准小球
            self.updatePyGame()            # 更新显示
            left, right = [], []            # 定义基准值左右两侧的小球列表
            leftList, rightList = [], []  # 定义基准值左右两侧的数值列表
            #开始比较
            for num in bmm.bubbleList:
                if not num.isMid:
                    if num.v >= mid.v:
                        bmm.dright(self,right,num)
                        right.append(num)
                        leftList.append(num.v)
                    else:
                        bmm.dleft(self,left,num)
                        left.append(num)
                        rightList.append(num.v)

                    self.updatePyGame()      # 更新显示

            #构建左右小球集合的管理器
            bmm.left=BubbleManager(self.win, 100,False,left)
            bmm.right=BubbleManager(self.win, 100,False,right)
            #递归调用
            return self.quick_sort( bmm.left) + [mid] + self.quick_sort( bmm.right)
        else:
            return data

    def resultSortList(self):
        self.bm.rsult(self)              # 循环结束，将小球合并到统一水平线
        self.updatePyGame()              # 更新显示
    def loop(self):                      # 循环监听键鼠设备触发相应数据
        self.updatePyGame()
        while True:
            # 检查事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                    pygame.quit()
                if event.type == pygame.KEYDOWN:  # 点击任意键开始动画
                    sortList=self.quick_sort(self.bm)
                    self.bm.initBuList()
                    self.bm.bubbleList=sortList
                    self.resultSortList()

    def updatePyGame(self):         # 更新画布
        self.win.fill(COLORS["bg"])
        self.bm.draw()
        self.clock.tick(FPS)
        pygame.display.update()

