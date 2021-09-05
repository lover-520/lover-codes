#include "cpostprocessing.h"
#include "ogrsf_frmts.h"
#define  ACCEPT_USE_OF_DEPRECATED_PROJ_API_H

#include <iostream>
using namespace std;
#include <iomanip>

CPostProcessing::CPostProcessing()
{
}

CPostProcessing::~CPostProcessing()
{
}

/*打印shp文件的属性表信息*/
int CPostProcessing::PrintShp(string shp_file_path) {
    GDALAllRegister();  //注册所有内置到GDAL/OGR中的格式驱动程序
    GDALDataset* poDS;
    CPLSetConfigOption("SHAPE_ENCODING", "");  //解决中文乱码问题
    //读取shp文件
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
        // 获取字段属性
        if (!numFeature) {
            int numField = poFeature->GetFieldCount();

            for (int inumField = 0; inumField < numField; inumField++) {
                OGRFieldDefn* poField = poFeature->GetFieldDefnRef(inumField);
                cout << poField->GetNameRef() << "    ";
            }
            cout << endl;
        }

        OGRGeometry* poGeometry;
        poGeometry = poFeature->GetGeometryRef();
        OGRPolygon* pPolygon = (OGRPolygon*)poGeometry->clone();
        double area = pPolygon->get_Area();
        //cout << "面积：" << pPolygon->get_Area() << endl;
        /*
        if (poGeometry != NULL) {
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
                cout << oField.GetInteger();
                cout << "     ";
                break;
            case OFTInteger64:
                cout << oField.GetInteger64();
                cout << "     ";
                break;
            case OFTReal:
                cout << setiosflags(ios::fixed) << oField.GetDouble();
                cout << "     ";
                break;
            case OFTString:
                cout << oField.GetString();
                cout << "     ";
                break;
            default:
                cout << oField.GetAsString();
                cout << "     ";
                break;
            }
        }
        cout << endl;
        numFeature++;
        OGRFeature::DestroyFeature(poFeature);

    }
    GDALClose(poDS);
    return 1;
}

int CPostProcessing::RemoveSmallArea(string shp_file_path, string output_shp_file_path, int threshold) {
    GDALAllRegister();  //GDAL注册所有驱动
    GDALDataset* poDS;  //加载数据
    poDS = (GDALDataset*)GDALOpenEx(shp_file_path.c_str(), GDAL_OF_VECTOR, NULL, NULL, NULL);
    if (poDS == NULL) {
        cout << "open failed!" << endl;
        exit(1);
    }
    //读取层
    OGRLayer* poLayer;
    poLayer = poDS->GetLayer(0);
    poLayer->ResetReading();
    OGRSpatialReference* poSpatial = poLayer->GetSpatialRef();
    //cout << poSpatial->GetEPSGGeogCS() << endl;
    OGRSpatialReference poTarSpatial;
    poTarSpatial.importFromEPSG(3857);
    OGRCoordinateTransformation* ogrCT;
    ogrCT = OGRCreateCoordinateTransformation(poSpatial, &poTarSpatial);

    const char* pszDriverName = "ESRI Shapefile";
    GDALDriver* poDriver;
    GDALAllRegister();
    poDriver = GetGDALDriverManager()->GetDriverByName(pszDriverName);
    if (poDriver == NULL)
    {
        cout << pszDriverName << " driver not available." << endl;
        exit(1);
    }
    
    int shp_folder_index = shp_file_path.find_last_of('/');
    string shp_folder_path = shp_file_path.substr(0, shp_folder_index);
    string output_file_path = shp_folder_path + "/" + output_shp_file_path + ".shp";
    
    GDALDataset* poDSTar;
    poDSTar = poDriver->Create(output_file_path.c_str(), 0, 0, 0, GDT_Unknown, NULL);
    if (poDSTar == NULL) {
        cout << "Creation of output file failed." << endl;
        exit(1);
    }
    OGRLayer* poLayerTar;
    poLayerTar = poDSTar->CreateLayer(output_shp_file_path.c_str(), &poTarSpatial, wkbPolygon, NULL);
    if (poLayerTar == NULL) {
        cout << "Layer creation failed." << endl;
        exit(1);
    }

    OGRFeature* poFeature;
    while ((poFeature = poLayer->GetNextFeature())!=NULL){
        OGRGeometry* poGeometry;
        poGeometry = poFeature->GetGeometryRef();
        OGRGeometry* poTarGeometry;
        poTarGeometry = poGeometry->clone();
        poTarGeometry->transform(ogrCT);
        if (poGeometry == NULL) {
            cout << "Geometry get failed!" << endl;
        }
        if (poGeometry->getGeometryType() == wkbPolygon) {
            //OGRPolygon* poPolygon = poGeometry->toPolygon();
            //cout << poPolygon->get_Area() << "    ";
            OGRPolygon* poTarPolygon = poTarGeometry->toPolygon();
            double poArea = poTarPolygon->get_Area();
            if (poArea > threshold) {
                poFeature->SetGeometry(poTarGeometry);
                OGRErr ogrErr = poLayerTar->CreateFeature(poFeature);
            }
            //cout << poTarPolygon->get_Area() << endl;
        }
        
    }
    OGRFeature::DestroyFeature(poFeature);
    GDALClose(poDS);
    GDALClose(poDSTar);
    return 1;
}
