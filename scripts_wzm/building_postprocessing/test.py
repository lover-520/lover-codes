# -*- coding: utf-8 -*-
"""
* @author: wzm
* @function: 测试后处理文件
"""

from postprocessing import PostProcessing

if __name__ == '__main__':
    postprocessing_tmp = PostProcessing()

    
    ######################################## 测试第一个功能 #####################################################
    shp_file_path = "change.shp"
    out_shp_file_name = "function1"
    threshold = 100
    postprocessing_tmp.remove_small_area(shp_file_path, out_shp_file_name, threshold)
    print("功能一完成...")

    
    ######################################## 测试第二个功能 #####################################################
    shp_file_path = "change.shp"
    out_shp_file_name = "function2"
    postprocessing_tmp.points_simplification(shp_file_path, out_shp_file_name)
    print("功能二完成...")

    
    ######################################## 测试第三个功能 #####################################################
    shp_file_path = "change.shp"
    out_shp_file_name = "function3"
    angle_threshold = 45
    postprocessing_tmp.remove_redundancy_points(shp_file_path, out_shp_file_name, angle_threshold)
    print("功能三完成...")

    ######################################## 测试第四个功能 #####################################################
    shp_file_path = "change.shp"
    out_shp_file_name = "function4"
    index_threshold = 10
    dis_threshold = 3
    area_threshold = 100
    postprocessing_tmp.remove_tail(shp_file_path, out_shp_file_name, index_threshold, dis_threshold, area_threshold)
    print("功能四完成...")

    
    ######################################## 测试第五个功能 #####################################################
    shp_file_path = "change.shp"
    out_shp_file_name = "function5"
    postprocessing_tmp.get_minimum_rotated_rectangle(shp_file_path, out_shp_file_name)
    print("功能五完成...")
