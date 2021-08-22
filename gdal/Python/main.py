# -*-coding:UTF-8 -*-
'''
* main.py
* @author wzm
* created 2021/08/21 16:55:00
* @function: 用来测试Python中gdal的加载速度；
'''
import sys
import time

from GdalShp import GdalShp

if __name__ == "__main__":
    gdalshp = GdalShp()

    start_time = time.process_time()
    shp_file_path = "C:/Users/wzm00/Desktop/test/testgdal/Export_Output_2.shp"
    for i in range(100):
        gdalshp.getShp(shp_file_path=shp_file_path)

    end_time = time.process_time()
    print("total time(ms): " + str((end_time - start_time)*1000))
