# -*- coding: utf-8 -*-
"""
* @author: wzm
* @function: 后处理类
"""

import os
import math

from osgeo import ogr, osr, gdal
import shapefile
from shapely.geometry import Polygon

class PostProcessing:
    def __init__(self):
        pass
    
    def remove_small_area(self, shp_file_path, output_shp_file_name="output", threshold=0):
        """
        @function: 去除噪点环（根据面积阈值去除较小面积的多边形）;(在原shp文件的同级目录下生成一个新的名为output_shp_file_name的shp文件)
        @params:
        * shp_file_path: 原始的待处理的shp文件
        * output_shp_file_name: 输出的shp文件名，不要加.shp后缀
        * threshold: 面积阈值
        @return:
        """
        driver = ogr.GetDriverByName("ESRI Shapefile")
        datasource = driver.Open(shp_file_path, 1)
        layer = datasource.GetLayer()

        src_srs = layer.GetSpatialRef()  # 获取原始的坐标系或投影
        tgt_srs = osr.SpatialReference()  # 获取目标的坐标系或投影， web mercator
        tgt_srs.ImportFromEPSG(3857)
        transform = osr.CoordinateTransformation(src_srs, tgt_srs)

        tgt_datasource  = driver.CreateDataSource(os.path.split(shp_file_path)[0])
        tgt_geomtype = ogr.wkbPolygon
        tgt_layer = tgt_datasource.CreateLayer(output_shp_file_name, srs=tgt_srs, geom_type=tgt_geomtype)
        # from ipdb import set_trace; set_trace()
        layerDefinition = layer.GetLayerDefn()  # 获取图层的字段信息
        for i in range(layerDefinition.GetFieldCount()):
            tgt_layer.CreateField(layerDefinition.GetFieldDefn(i))
            # fieldName = layerDefinition.GetFieldDefn(i).GetName()
            # fieldTypeCode = layerDefinition.GetFieldDefn(i).GetType()
            # fieldType = layerDefinition.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
            # fieldWidth = layerDefinition.GetFieldDefn(i).GetWidth()
            # fieldPrecision = layerDefinition.GetFieldDefn(i).GetPrecision()
            # print(fieldName, fieldTypeCode, fieldType, fieldWidth, fieldPrecision)
            # from ipdb import set_trace; set_trace()

        for feature in layer:
            geom = feature.GetGeometryRef()
            geom_tgt = geom.Clone()
            geom_tgt.Transform(transform)
            if geom_tgt.GetArea() >= threshold:
                feature.SetGeometry(geom_tgt)
                tgt_layer.CreateFeature(feature)
        
        datasource.Destroy()
        tgt_datasource.Destroy()
    
    def points_simplification(self, shp_file_path, output_shp_file_name):
        """
        @function: 多边形点数化简，依次遍历每一个多边形的所有点，去掉偶数个;(在原shp文件的同级目录下生成一个新的名为output_shp_file_name的shp文件)
        @params:
        * shp_file_path: 原始的待处理的shp文件
        * output_shp_file_name: 输出的shp文件名，不要加.shp后缀
        @return:
        """
        driver = ogr.GetDriverByName("ESRI Shapefile")
        datasource = driver.Open(shp_file_path, 1)
        layer = datasource.GetLayer()

        src_srs = layer.GetSpatialRef()  # 获取原始的坐标系或投影
        tgt_srs = osr.SpatialReference()  # 获取目标的坐标系或投影， web mercator
        tgt_srs.ImportFromEPSG(3857)
        transform = osr.CoordinateTransformation(src_srs, tgt_srs)

        tgt_datasource  = driver.CreateDataSource(os.path.split(shp_file_path)[0])
        tgt_geomtype = ogr.wkbPolygon
        tgt_layer = tgt_datasource.CreateLayer(output_shp_file_name, srs=tgt_srs, geom_type=tgt_geomtype)
        layerDefinition = layer.GetLayerDefn()  # 获取图层的字段信息
        for i in range(layerDefinition.GetFieldCount()):
            tgt_layer.CreateField(layerDefinition.GetFieldDefn(i))

        for feature in layer:
            geom = feature.GetGeometryRef()
            geom_tgt = geom.Clone()
            geom_tgt.Transform(transform)
            geom_tgt_points = geom_tgt.GetGeometryRef(0).GetPoints()
            geom_tgt_point_aim = []
            for i, po in enumerate(geom_tgt_points):
                if i%2 == 0:
                    geom_tgt_point_aim.append(po)
            if len(geom_tgt_points) % 2 == 0:
                geom_tgt_point_aim.append(geom_tgt_points[-1])
            ring = ogr.Geometry(ogr.wkbLinearRing)
            for po in geom_tgt_point_aim:
                ring.AddPoint(po[0], po[1])
            ring.CloseRings()
            polygon = ogr.Geometry(ogr.wkbPolygon)
            polygon.AddGeometry(ring)
            feature.SetGeometry(polygon)
            tgt_layer.CreateFeature(feature)
        
        datasource.Destroy()
        tgt_datasource.Destroy()

    def remove_redundancy_points(self, shp_file_path, output_shp_file_name, angle_threshold=5):
        """
        @function: 去除冗余点，连续三个点的夹角少于某一阈值，中间点就是冗余点；（在原shp文件的同级目录下生成一个新的名为output_shp_file_name的shp文件）
        @params:
        * shp_file_path: 原始的待处理的shp文件
        * output_shp_file_name: 输出的shp文件名，不要加.shp后缀
        * angle_threshold: 角度阈值
        @return:
        """
        driver = ogr.GetDriverByName("ESRI Shapefile")
        datasource = driver.Open(shp_file_path, 1)
        layer = datasource.GetLayer()

        src_srs = layer.GetSpatialRef()  # 获取原始的坐标系或投影
        tgt_srs = osr.SpatialReference()  # 获取目标的坐标系或投影， web mercator
        tgt_srs.ImportFromEPSG(3857)
        transform = osr.CoordinateTransformation(src_srs, tgt_srs)

        tgt_datasource  = driver.CreateDataSource(os.path.split(shp_file_path)[0])
        tgt_geomtype = ogr.wkbPolygon
        tgt_layer = tgt_datasource.CreateLayer(output_shp_file_name, srs=tgt_srs, geom_type=tgt_geomtype)
        layerDefinition = layer.GetLayerDefn()  # 获取图层的字段信息
        for i in range(layerDefinition.GetFieldCount()):
            tgt_layer.CreateField(layerDefinition.GetFieldDefn(i))

        for feature in layer:
            geom = feature.GetGeometryRef()
            geom_tgt = geom.Clone()
            geom_tgt.Transform(transform)
            geom_tgt_points = geom_tgt.GetGeometryRef(0).GetPoints()
            del geom_tgt_points[-1]
            geom_tgt_point_aim = []
            for i, po in enumerate(geom_tgt_points):
                if i==0:
                    angle = self._caluate_angle(geom_tgt_points[-1], geom_tgt_points[0], geom_tgt_points[1])
                    if (angle>angle_threshold) & (angle<(180-angle_threshold)):
                        geom_tgt_point_aim.append(po)
                    continue
                if i==len(geom_tgt_points)-1:
                    angle = self._caluate_angle(geom_tgt_points[-2], geom_tgt_points[-1], geom_tgt_points[0])
                    if (angle>angle_threshold) & (angle<(180-angle_threshold)):
                        geom_tgt_point_aim.append(po)
                    continue
                angle = self._caluate_angle(geom_tgt_points[i-1], geom_tgt_points[i], geom_tgt_points[i+1])
                if (angle>angle_threshold) & (angle<(180-angle_threshold)):
                        geom_tgt_point_aim.append(po)

            if len(geom_tgt_point_aim) >= 2:
                if geom_tgt_point_aim[0] != geom_tgt_point_aim[-1]:
                    geom_tgt_point_aim.append(geom_tgt_point_aim[0])
                ring = ogr.Geometry(ogr.wkbLinearRing)
                for po in geom_tgt_point_aim:
                    ring.AddPoint(po[0], po[1])
                ring.CloseRings()
                polygon = ogr.Geometry(ogr.wkbPolygon)
                polygon.AddGeometry(ring)
                feature.SetGeometry(polygon)
                tgt_layer.CreateFeature(feature)
            else:
                tgt_layer.CreateFeature(feature)   
        
        datasource.Destroy()
        tgt_datasource.Destroy()
    
    def _caluate_angle(self, p1, p2, p3):
        """
        @funcion: 计算连续三个点的夹角，p2是中间的点，余弦定理
        @param:
        * p1,p2,p3: 三个点
        @return: 角度值
        """
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        x3, y3 = p3[0], p3[1]

        p1p2 = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
        p2p3 = math.sqrt((x3 - x2) * (x3 - x2) + (y3 - y2) * (y3 - y2))
        p1p3 = math.sqrt((x1 - x3) * (x1 - x3) + (y1 - y3) * (y1 - y3))
        tmp = (p1p2 * p1p2 + p2p3 * p2p3 - p1p3 * p1p3) / (2 * p1p2 * p2p3)
        if tmp>1:
            tmp = 1
        if tmp<-1:
            tmp=-1
        angle = math.acos(tmp) * 180.0 / 3.1415926
        if angle<0:
            angle = -angle
        return angle
    
    def remove_tail(self, shp_file_path, output_shp_file_name, index_threshold=10, dis_threshold=3, area_threshold=500):
        """
        @function: 去除多边形尾巴和分割多边形；（在原shp文件的同级目录下生成一个新的名为output_shp_file_name的shp文件）
        @params:
        * shp_file_path: 原始的待处理的shp文件
        * output_shp_file_name: 输出的shp文件名，不要加.shp后缀
        * index_threshold: 下标阈值
        * dis_threshold: 距离阈值
        * area_threshold: 面积阈值
        @return:
        """
        driver = ogr.GetDriverByName("ESRI Shapefile")
        datasource = driver.Open(shp_file_path, 1)
        layer = datasource.GetLayer()

        src_srs = layer.GetSpatialRef()  # 获取原始的坐标系或投影
        tgt_srs = osr.SpatialReference()  # 获取目标的坐标系或投影， web mercator
        tgt_srs.ImportFromEPSG(3857)
        transform = osr.CoordinateTransformation(src_srs, tgt_srs)

        tgt_datasource  = driver.CreateDataSource(os.path.split(shp_file_path)[0])
        tgt_geomtype = ogr.wkbPolygon
        tgt_layer = tgt_datasource.CreateLayer(output_shp_file_name, srs=tgt_srs, geom_type=tgt_geomtype)
        layerDefinition = layer.GetLayerDefn()  # 获取图层的字段信息
        for i in range(layerDefinition.GetFieldCount()):
            tgt_layer.CreateField(layerDefinition.GetFieldDefn(i))

        for feature in layer:
            geom = feature.GetGeometryRef()
            geom_tgt = geom.Clone()
            geom_tgt.Transform(transform)
            geom_tgt_points = geom_tgt.GetGeometryRef(0).GetPoints()
            geom_tgt_point_aim = []

            avg_dis, dis = 0, 0
            for i in range(len(geom_tgt_points)-1):
                dx = geom_tgt_points[i][0] - geom_tgt_points[i+1][0]
                dy = geom_tgt_points[i][1] - geom_tgt_points[i+1][1]
                dis += math.sqrt((dx * dx) + (dy * dy))
            avg_dis = dis / (len(geom_tgt_points)-1)

            dis_threshold *= avg_dis
            
            i_pair = self._get_dis_index(geom_tgt_points, index_threshold, dis_threshold)  # 得到了多边形中可能是尾巴的两个边界点

            # 如果是只有一个点
            if i_pair[0]==i_pair[1]:
                del geom_tgt_points[i_pair[0]]
                if len(geom_tgt_points) == 0:
                    continue
                if geom_tgt_points[0] != geom_tgt_points[-1]:
                    geom_tgt_points.append(geom_tgt_points[0])
                ring = ogr.Geometry(ogr.wkbLinearRing)
                for po in geom_tgt_points:
                    ring.AddPoint(po[0], po[1])
                ring.CloseRings()
                polygon = ogr.Geometry(ogr.wkbPolygon)
                polygon.AddGeometry(ring)
                feature.SetGeometry(polygon)
                tgt_layer.CreateFeature(feature)

            if i_pair[0] < i_pair[1]:
                geom_tgt_points1 = geom_tgt_points[i_pair[0]:i_pair[1]+1]
                geom_tgt_points1.append(geom_tgt_points1[0])  # 尾部多边形首尾一致
                del geom_tgt_points[i_pair[0]:i_pair[1]+1]
                if len(geom_tgt_points) != 0:
                    if geom_tgt_points[0] != geom_tgt_points[-1]:
                        geom_tgt_points.append(geom_tgt_points[0])
                ring = ogr.Geometry(ogr.wkbLinearRing)
                for po in geom_tgt_points1:
                    ring.AddPoint(po[0], po[1])
                ring.CloseRings()
                polygon = ogr.Geometry(ogr.wkbPolygon)
                polygon.AddGeometry(ring)
                if polygon.GetArea() > area_threshold:
                    feature.SetGeometry(polygon)
                    tgt_layer.CreateFeature(feature)    
                
                ring = ogr.Geometry(ogr.wkbLinearRing)
                for po in geom_tgt_points:
                    ring.AddPoint(po[0], po[1])
                ring.CloseRings()
                polygon = ogr.Geometry(ogr.wkbPolygon)
                polygon.AddGeometry(ring)
                feature.SetGeometry(polygon)
                tgt_layer.CreateFeature(feature)
            
            if i_pair[0] > i_pair[1]:
                geom_tgt_points2 = geom_tgt_points[i_pair[1]+1:i_pair[0]]  # 主体部分
                if len(geom_tgt_points2) != 0:
                    geom_tgt_points2.append(geom_tgt_points2[0])
                del geom_tgt_points[i_pair[1]+1:i_pair[0]]
                if len(geom_tgt_points) != 0:
                    if geom_tgt_points[0] != geom_tgt_points[1]:
                        geom_tgt_points.append(geom_tgt_points[0])
                ring = ogr.Geometry(ogr.wkbLinearRing)
                for po in geom_tgt_points:
                    ring.AddPoint(po[0], po[1])
                ring.CloseRings()
                polygon = ogr.Geometry(ogr.wkbPolygon)
                polygon.AddGeometry(ring)
                if polygon.GetArea() > area_threshold:
                    feature.SetGeometry(polygon)
                    tgt_layer.CreateFeature(feature)
                
                ring = ogr.Geometry(ogr.wkbLinearRing)
                for po in geom_tgt_points2:
                    ring.AddPoint(po[0], po[1])
                ring.CloseRings()
                polygon = ogr.Geometry(ogr.wkbPolygon)
                polygon.AddGeometry(ring)
                feature.SetGeometry(polygon)
                tgt_layer.CreateFeature(feature)
             
        datasource.Destroy()
        tgt_datasource.Destroy()

    def _get_dis_index(self, points, index_thres, dis_thres):
        """
        @funcion: 计算每一个多边形的点中符号要求的一个下标对；
        @params:
        * points: 多边形的点，列表
        * index_thres: 下标阈值
        * dis_thres:  距离阈值
        @return:
        (j,k)下标对
        """
        index_pairs = []
        for i in range(len(points)):
            p1 = points[i]
            aim_k = -1
            for j in range(index_thres):
                tmp_num = (i + j + 1) % (len(points) - 1)
                p2 = points[tmp_num]
                dx, dy = p1[0] - p2[0], p1[1] - p2[1]
                tmp_ds = math.sqrt(dx * dx + dy * dy)
                if tmp_ds < dis_thres:
                    aim_k = tmp_num
            if aim_k != -1:
                index_pairs.append((i, aim_k))
        if len(index_pairs) == 0:
            return None
        index_pairs = sorted(index_pairs, key=lambda i_pair:i_pair[1]-i_pair[0])
        min_dis = float('inf')
        aim_pair = None
        for i_pair in index_pairs:
            dx, dy = points[i_pair[0]][0] - points[i_pair[1]][0], points[i_pair[0]][1] - points[i_pair[1]][1]
            tmp_dis = math.sqrt(dx * dx + dy * dy)
            if tmp_dis < min_dis:
                aim_pair = i_pair
                min_dis = tmp_dis
        return aim_pair
    
    def get_minimum_rotated_rectangle(self, shp_file_path, output_shp_file_name):
        """
        @function: 获取最小外接矩形；（在原shp文件的同级目录下生成一个新的名为output_shp_file_name的shp文件）
        @params:
        * shp_file_path: 原始的待处理的shp文件
        * output_shp_file_name: 输出的shp文件名，不要加.shp后缀
        @return:
        """
        driver = ogr.GetDriverByName("ESRI Shapefile")
        datasource = driver.Open(shp_file_path, 1)
        layer = datasource.GetLayer()

        src_srs = layer.GetSpatialRef()  # 获取原始的坐标系或投影
        tgt_srs = osr.SpatialReference()  # 获取目标的坐标系或投影， web mercator
        tgt_srs.ImportFromEPSG(3857)
        transform = osr.CoordinateTransformation(src_srs, tgt_srs)

        tgt_datasource  = driver.CreateDataSource(os.path.split(shp_file_path)[0])
        tgt_geomtype = ogr.wkbPolygon
        tgt_layer = tgt_datasource.CreateLayer(output_shp_file_name, srs=tgt_srs, geom_type=tgt_geomtype)
        layerDefinition = layer.GetLayerDefn()  # 获取图层的字段信息
        for i in range(layerDefinition.GetFieldCount()):
            tgt_layer.CreateField(layerDefinition.GetFieldDefn(i))

        for feature in layer:
            geom = feature.GetGeometryRef()
            geom_tgt = geom.Clone()
            geom_tgt.Transform(transform)
            geom_tgt_points = geom_tgt.GetGeometryRef(0).GetPoints()
            geom_tgt_point_aim = []
            geom_polygon = Polygon(geom_tgt_points)
            geom_mininum_ratated_rectangle = geom_polygon.minimum_rotated_rectangle
            geom_rectangle_x, geom_rectangle_y = geom_mininum_ratated_rectangle.exterior.coords.xy
            for i in range(len(geom_rectangle_x)):
                geom_tgt_point_aim.append([geom_rectangle_x[i], geom_rectangle_y[i]])
            
            ring = ogr.Geometry(ogr.wkbLinearRing)
            for po in geom_tgt_point_aim:
                ring.AddPoint(po[0], po[1])
            ring.CloseRings()
            polygon = ogr.Geometry(ogr.wkbPolygon)
            polygon.AddGeometry(ring)
            feature.SetGeometry(polygon)
            tgt_layer.CreateFeature(feature)
             
        datasource.Destroy()
        tgt_datasource.Destroy()
