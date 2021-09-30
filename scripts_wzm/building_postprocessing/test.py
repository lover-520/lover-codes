# -*- coding: utf-8 -*-
"""
* @author: wzm
* @function: 测试后处理文件
"""

from postprocessing import PostProcessing
import time

if __name__ == '__main__':
    shp_file_path = "E:/MyProject/DataSet/罗山给wzm/411521罗山县/411521202004BHXX.shp"
    # shp_file_path = "E:/MyProject/DataSet/BuildingPostProcessing/shp/change.shp"
    # shp_file_path = "E:/MyProject/DataSet/给wzm/RasterT_tif53_Merge.shp"
    postprocessing_tmp = PostProcessing(shp_file_path)
    # postprocessing_tmp.check_topology()
    

    """
    # ####################################### 测试第一个功能 #####################################################
    start_time = time.process_time_ns()
    shp_file_path = "E:/MyProject/DataSet/BuildingPostProcessing/shp/change.shp"
    out_shp_file_name = "function1"
    threshold = 100
    postprocessing_tmp.remove_small_area(shp_file_path, out_shp_file_name, threshold)
    end_time = time.process_time_ns()
    print("total time(ms): " + str((end_time - start_time) / 1000000))
    print("功能一完成...")
    """

    """
    # ####################################### 测试第二个功能 #####################################################
    shp_file_path = "change.shp"
    out_shp_file_name = "function2"
    postprocessing_tmp.points_simplification(shp_file_path, out_shp_file_name)
    print("功能二完成...")

    
    # ####################################### 测试第三个功能 #####################################################
    shp_file_path = "change.shp"
    out_shp_file_name = "function3"
    angle_threshold = 45
    postprocessing_tmp.remove_redundancy_points(shp_file_path, out_shp_file_name, angle_threshold)
    print("功能三完成...")

    # ####################################### 测试第四个功能 #####################################################
    shp_file_path = "change.shp"
    out_shp_file_name = "function4"
    index_threshold = 10
    dis_threshold = 3
    area_threshold = 100
    postprocessing_tmp.remove_tail(shp_file_path, out_shp_file_name, index_threshold, dis_threshold, area_threshold)
    print("功能四完成...")

    
    # ####################################### 测试第五个功能 #####################################################
    shp_file_path = "change.shp"
    out_shp_file_name = "function5"
    postprocessing_tmp.get_minimum_rotated_rectangle(shp_file_path, out_shp_file_name)
    print("功能五完成...")
    """
    
    # # ####################################### 测试初步算法功能 #####################################################
    # out_shp_file_name = "function6"
    # postprocessing_tmp.check_must_not_overlay(out_shp_file_name)
    
    # # ####################################### 测试并集Union功能 #####################################################
    # out_shp_file_name = "functiontest"
    # postprocessing_tmp.check_must_not_overlay_test(out_shp_file_name)
    
    # # ####################################### 测试依次Union功能 #####################################################
    # out_shp_file_name = "function_dissolve"
    # postprocessing_tmp.check_must_not_overlay_dissolve(out_shp_file_name)
    
    # ####################################### 测试UnionCascaded功能 #####################################################
    out_shp_file_name = "function_cascaded"
    postprocessing_tmp.check_must_not_overlay_cascaded(out_shp_file_name)
