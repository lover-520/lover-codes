# -*- coding: utf-8 -*-
"""
@author: WZM
@time: 2021/8/22 14:22
@function:
"""
import sys

from osgeo import gdal
from osgeo import ogr


class GdalShp:
    def __init__(self):
        pass

    def getShp(self, shp_file_path):
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")  # 为了支持中文路径
        gdal.SetConfigOption("SHAPE_ENCODING", "")  # 为了使属性表字段支持中文

        ogr.RegisterAll()  # 注册所有驱动

        # 打开数据
        ds = ogr.Open(shp_file_path, 0)
        if ds is None:
            # print("打开%s失败" % shp_file_path)
            sys.exit(1)
        # print("文件 %s 打开成功" % shp_file_path)

        iLayerCount = ds.GetLayerCount()  # 获取该数据源中的图层个数，一般shp数据图层只有一个，mdb、dxf可能有多个
        # 获取第一个图层
        iLayerIndex = 0
        oLayer = ds.GetLayerByIndex(iLayerIndex)

        if oLayer is None:
            print("获取第 %d 个图层失败！！！" % iLayerIndex)
            sys.exit(1)

        # 对图层进行初始化
        oLayer.ResetReading()

        # 获取图层中给定属性表表头并输出
        # print("属性表结构信息")
        oDefn = oLayer.GetLayerDefn()
        iFieldCount = oDefn.GetFieldCount()
        for iAttr in range(iFieldCount):
            oField = oDefn.GetFieldDefn(iAttr)
            # print(oField.GetNameRef(), end="    ")
        # print()
        # 输出图层中的要素个数
        oFeature = oLayer.GetNextFeature()
        while oFeature is not None:
            # print("当前处理第%d个：属性值" % oFeature.GetFID())

            oGeometry = oFeature.GetGeometryRef()
            # print(oGeometry.GetArea())

            for iField in range(iFieldCount):
                oFieldDefn = oDefn.GetFieldDefn(iField)
                # print(oFeature.GetFieldAsString(iField), end="    ")
            # print()
            oFeature = oLayer.GetNextFeature()
        # print("数据集关闭！")
