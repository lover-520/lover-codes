#include <iostream>
#include <iomanip>
using namespace std;

#include <ctime>
#include <windows.h>

#include "gdalshp.h"

clock_t start_time, end_time;

int main(){
    LARGE_INTEGER t1, t2, tc;
    QueryPerformanceFrequency(&tc);
    QueryPerformanceCounter(&t1);

    //start_time=clock();

    CGdalShp cshp = CGdalShp();
    for (int i = 0; i < 100; i++) {
        cshp.GetShp("C:/Users/wzm00/Desktop/test/testgdal/Export_Output_2.shp");
    }
    
    
    //system("pause");
    //end_time = clock();
    //double total_time = (double)(end_time) - (double)(start_time) * 1000 / CLOCKS_PER_SEC;
    //cout << "total time(ms): " << total_time << endl;
    QueryPerformanceCounter(&t2);
    double time = (double)(t2.QuadPart - t1.QuadPart) / (double)tc.QuadPart * 1000;
    cout << "time = " << time << "ms" << endl;  //输出时间（单位：ｓ）
    return 1;






    //int i = 0;
    //while ((poFeature = poLayer->GetNextFeature()) != NULL)
    //{
    //    // if (poFeature->GetFieldAsDouble("AREA") < 80000) continue; //去掉面积过小的polygon
    //    OGRGeometry* mPolygon = poFeature->GetGeometryRef();
    //    
    //    i = i++;
    //    cout << i << "  ";
    //    OGRFeatureDefn* poFDefn = poLayer->GetLayerDefn();
    //    int iField;
    //    int n = poFDefn->GetFieldCount(); //获得字段的数目，不包括前两个字段（FID,Shape);
    //    for (iField = 0; iField < n; iField++)
    //    {
    //        //输出每个字段的值
    //        OGRFieldDefn* poField = poFeature->GetFieldDefnRef(iField);
    //        cout << poField->GetNameRef() << endl;
    //        cout << poFeature->GetFieldAsString(iField) << "    ";
    //    }
    //    cout << endl;

        
        /*OGRGeometry* poGeometry;
        poGeometry = poFeature->GetGeometryRef();
        if (poGeometry != NULL) {
            OGRwkbGeometryType pGeoType = poGeometry->getGeometryType();
            if (pGeoType == wkbPoint) {
                OGRPoint* poPoint = (OGRPoint*)poGeometry;
                printf("%.3f,%.3f\n", poPoint->getX(), poPoint->getY());
            }else if (pGeoType == wkbPolygon){
                OGRPolygon* pPolygon = (OGRPolygon*)poGeometry->clone();
                cout << mPolygon->Polygonize() << endl;
            }
            else if (pGeoType == wkbPolygon25D) {
                OGRPolygon* pPolygon = (OGRPolygon*)poGeometry->clone();
                cout << "面积：" << pPolygon->get_Area() << endl;
            }
        }*/

        //OGRFeature::DestroyFeature(poFeature);
    //}
    //GDALClose(poDS);
    ////system("pause");
    //return 1;
}