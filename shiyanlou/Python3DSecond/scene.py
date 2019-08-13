import numpy

from node import Sphere, Cube, SnowFigure



class Scene(object):

    #放置节点的深度，放置的节点距离摄像机15个单位
    PLACE_DEPTH = 15.0

    def __init__(self):
        self.node_list = list()
        self.selected_node = None


    def add_node(self, node):
        """ 在场景中加入一个新节点 """
        self.node_list.append(node)

    def render(self):
        """ 遍历场景下所有节点并渲染 """
        for node in self.node_list:
            node.render()


    def pick(self, start, direction, mat):
        """
        参数中的mat为当前ModelView的逆矩阵，作用是计算激光在局部（对象）坐标系中的坐标
        """
        import sys

        if self.selected_node is not None:
            self.selected_node.select(False)
            self.selected_node = None

        # 找出激光击中的最近的节点。
        mindist = sys.maxsize
        closest_node = None
        for node in self.node_list:
            hit, distance = node.pick(start, direction, mat)
            if hit and distance < mindist:
                mindist, closest_node = distance, node

        # 如果找到了，选中它
        if closest_node is not None:
            closest_node.select()
            closest_node.depth = mindist
            closest_node.selected_loc = start + direction * mindist
            self.selected_node = closest_node


    def place(self, shape, start, direction, inv_modelview):
        new_node = None
        if shape == 'sphere': new_node = Sphere()
        elif shape == 'cube': new_node = Cube()
        elif shape == 'figure': new_node = SnowFigure()

        self.add_node(new_node)

        # 得到在摄像机坐标系中的坐标
        translation = (start + direction * self.PLACE_DEPTH)

        # 转换到世界坐标系
        pre_tran = numpy.array([translation[0], translation[1], translation[2], 1])
        translation = inv_modelview.dot(pre_tran)

        new_node.translate(translation[0], translation[1], translation[2])

    def move_selected(self, start, direction, inv_modelview):

        if self.selected_node is None: return

        # 找到选中节点的坐标与深度（距离）
        node = self.selected_node
        depth = node.depth
        oldloc = node.selected_loc

        # 新坐标的深度保持不变
        newloc = (start + direction * depth)

        # 得到世界坐标系中的移动坐标差
        translation = newloc - oldloc
        pre_tran = numpy.array([translation[0], translation[1], translation[2], 0])
        translation = inv_modelview.dot(pre_tran)

        # 节点做平移变换
        node.translate(translation[0], translation[1], translation[2])
        node.selected_loc = newloc
