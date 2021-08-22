#include "gdalshp.h"
#include "ogrsf_frmts.h"
#define  ACCEPT_USE_OF_DEPRECATED_PROJ_API_H

CGdalShp::CGdalShp()
{
}

CGdalShp::~CGdalShp()
{
}

int CGdalShp::GetShp(string shp_file_path) {
    GDALAllRegister();  //注册所有内置到GDAL/OGR中的格式驱动程序
    GDALDataset* poDS;
    CPLSetConfigOption("SHAPE_ENCODING", "");  //解决中文乱码问题
    //读取shp文件
    //const char* shp_file_path_char = shp_file_path.data();
    poDS = (GDALDataset*)GDALOpenEx(shp_file_path.c_str(), GDAL_OF_VECTOR, NULL, NULL, NULL);
    if (poDS == NULL) {
        cout << "Open failed.\n%s";
        return 0;
    }

    OGRLayer* poLayer;
    poLayer = poDS->GetLayer(0); //读取层
    OGRFeature* poFeature;

    poLayer->ResetReading();  // 开始读取该图层中的每一行
    int numFeature = 0;
    while ((poFeature = poLayer->GetNextFeature()) != NULL) {
        if (!numFeature) {
            int numField = poFeature->GetFieldCount();

            for (int inumField = 0; inumField < numField; inumField++) {
                OGRFieldDefn* poField = poFeature->GetFieldDefnRef(inumField);
                //cout << poField->GetNameRef() << "    ";
            }
            //cout << endl;
        }

        OGRGeometry* poGeometry;
        poGeometry = poFeature->GetGeometryRef();
        OGRPolygon* pPolygon = (OGRPolygon*)poGeometry->clone();
        double area = pPolygon->get_Area();
        //cout << "面积：" << pPolygon->get_Area() << endl;
        /*if (poGeometry != NULL) {
            OGRwkbGeometryType pGeoType = poGeometry->getGeometryType();
            if (pGeoType == wkbPoint) {
                OGRPoint* poPoint = (OGRPoint*)poGeometry;
                printf("%.3f,%.3f\n", poPoint->getX(), poPoint->getY());
            }else if (pGeoType == wkbPolygon){
                OGRPolygon* pPolygon = (OGRPolygon*)poGeometry->clone();
                cout << poGeometry->Polygonize() << endl;
            }
            else if (pGeoType == wkbPolygon25D) {
                OGRPolygon* pPolygon = (OGRPolygon*)poGeometry->clone();
                cout << "面积：" << pPolygon->get_Area() << endl;
            }
        }*/

        for (auto&& oField : *poFeature) {

            switch (oField.GetType()) {
            case OFTInteger:
                //cout << oField.GetInteger();
                //cout << "     ";
                break;
            case OFTInteger64:
                //cout << oField.GetInteger64();
                //cout << "     ";
                break;
            case OFTReal:
                //cout << setiosflags(ios::fixed) << oField.GetDouble();
                //cout << "     ";
                break;
            case OFTString:
                //cout << oField.GetString();
                //cout << "     ";
                break;
            default:
                //cout << oField.GetAsString();
                //cout << "     ";
                break;
            }
        }
        //cout << endl;
        numFeature++;
        OGRFeature::DestroyFeature(poFeature);

    }
    GDALClose(poDS);
}