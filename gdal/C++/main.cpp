#include <iostream>
#include <iomanip>
using namespace std;

#include <ctime>
// #include <windows.h>

#include "gdalshp.h"

clock_t start_time, end_time;

int main(){
    // LARGE_INTEGER t1, t2, tc;
    // QueryPerformanceFrequency(&tc);
    // QueryPerformanceCounter(&t1);
    clock_t start_time, end_time;

    start_time=clock();

    CGdalShp cshp = CGdalShp();
    for (int i = 0; i < 100; i++) {
        cshp.GetShp("C:/Users/wzm00/Desktop/test/testgdal/Export_Output_2.shp");
        cout<<i<<endl;
    }
    
    
    //system("pause");
    end_time = clock();
    double total_time = (double)(end_time) - (double)(start_time) * 1000 / CLOCKS_PER_SEC;
    cout << "total time(ms): " << total_time << endl;
    // QueryPerformanceCounter(&t2);
    // double time = (double)(t2.QuadPart - t1.QuadPart) / (double)tc.QuadPart * 1000;
    // cout << "time = " << time << "ms" << endl;  //���ʱ�䣨��λ����
    return 1;






    //int i = 0;
    //while ((poFeature = poLayer->GetNextFeature()) != NULL)
    //{
    //    // if (poFeature->GetFieldAsDouble("AREA") < 80000) continue; //ȥ�������С��polygon
    //    OGRGeometry* mPolygon = poFeature->GetGeometryRef();
    //    
    //    i = i++;
    //    cout << i << "  ";
    //    OGRFeatureDefn* poFDefn = poLayer->GetLayerDefn();
    //    int iField;
    //    int n = poFDefn->GetFieldCount(); //����ֶε���Ŀ��������ǰ�����ֶΣ�FID,Shape);
    //    for (iField = 0; iField < n; iField++)
    //    {
    //        //���ÿ���ֶε�ֵ
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
                cout << "�����" << pPolygon->get_Area() << endl;
            }
        }*/

        //OGRFeature::DestroyFeature(poFeature);
    //}
    //GDALClose(poDS);
    ////system("pause");
    //return 1;
}