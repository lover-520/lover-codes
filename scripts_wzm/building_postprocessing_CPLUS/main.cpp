#include <iostream>
#include <iomanip>
using namespace std;

#include <ctime>

#include "cpostprocessing.h"

clock_t start_time, end_time;

int main(){
    start_time=clock();

    CPostProcessing cshp = CPostProcessing();
    //cshp.PrintShp("E:/MyProject/DataSet/BuildingPostProcessing/shp/change.shp");
    
    cshp.RemoveSmallArea("/home/wuzm/BuildingPostProcessing/shp/change.shp", "function1-c", 100);
    /*string filepath = "E:/MyProject/DataSet/BuildingPostProcessing/shp/change.shp";
    int pathindex = filepath.find_last_of('/');
    string path = filepath.substr(0, pathindex);
    cout << path << endl;
    string name = filepath.substr(pathindex + 1, -1);
    cout << name << endl;
    string out = "function1-c.shp";
    string outname = path + "/" + out;
    cout << outname << endl;*/

    
    //system("pause");
    end_time = clock();
    double total_time = ((double)(end_time) - (double)(start_time)) * 1000 / CLOCKS_PER_SEC;
    cout << "total time(ms): " << total_time << endl;
    return 1;

}
