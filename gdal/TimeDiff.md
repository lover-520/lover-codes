# gdal时间差异比较

-------------------------------------------比较一---------------------------------------------------------

比较情况：读取shp并从打印出来：

数据：shp文件，8kb，属性表中30行，每一行包括六个字段（不包括FID和Shape）

* 包含输出，打印属性表信息（包括表头字段名称和每一行的信息）（单位ms）

| 语言   | 一    | 二   | 三    | 四    | 五    | 六    | 七    | 八    | 九    | 十     |
| ------ | ----- | ---- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ------ |
| C++    | 159   | 164  | 161   | 164   | 222   | 168   | 177   | 170   | 166   | 151    |
| Python | 31.25 | 62.5 | 31.25 | 31.25 | 31.25 | 31.25 | 31.25 | 31.25 | 31.25 | 15.625 |

* 不包括输出，仅仅是简单的读取，运行100次再取平均

| 语言   | 一      | 二      | 三      | 四      | 五      | 六      | 七      | 八      | 九     | 十      |
| ------ | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------ | ------- |
| C++    | 4.97619 | 4.97057 | 5.43498 | 4.57527 | 5.22256 | 4.74738 | 4.98199 | 4.47691 | 4.7447 | 4.80887 |
| Python | 5.46875 | 4.84375 | 5.00    | 5.00    | 5.00    | 5.00    | 5.00    | 4.84375 | 4.6875 | 5.00    |
