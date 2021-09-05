# C++版本AI解译结果后处理脚本说明

* cpostprocessing.h 后处理的头文件
* cpostprocessing.cpp 后处理的cpp文件
* main.cpp 主程序入口

编译说明：

两种方式：

*****分开编译*****

g++ -c cpostprocessing.cpp （会得到一个叫cpostprocessing.o的中间文件）

g++ -c main.cpp（会得到一个main.o的中间文件，只编译cpp文件即可）

g++ cpostprocessing.o main.o -o main（-o参数后面的main是生成的可执行文件的名称，随便取）

*****集中编译*****

g++ -o main cpostprocessing.cpp main.cpp -lgdal

-lgdal选项是在gdal的docker容器中进行编译需要的参数，需要寻找动态链接库；