#pragma once
#include <iostream>
#include <string>
using namespace std;

class CPostProcessing
{
public:
	CPostProcessing();
	~CPostProcessing();

	int PrintShp(string shp_file_path);

	int RemoveSmallArea(string shp_file_path, string output_shp_file_path, int threshold);
private:

};
