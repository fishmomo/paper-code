## Introduction

**File: AMSR_nc**

(注意：该文件夹中的nc数据为H8与AMSR的中间生成数据，其按文章中的匹配算法生成。)

note: The nc data in this folder is the intermediate generated data between H8 and AMSR, which is generated according to the matching algorithm in the article.



## Here is the code

(以下为代码介绍)

**1.read_ERA5_H8**

（用于读取研究时段的H8和ERA5数据，如2020年1,4,7,10月。目的得到转化后不同分辨率的H8数据转换为可与其他再分析资料进行比较的中间数据。）

 H8 and ERA5 data were read for study periods, such as January, April, July, and October 2020. Objective to obtain the transformed H8 data with different resolutions and to convert them into intermediate data which can be compared with other reanalysis data.

**2.H8_ERA5_analyze**

（H8与ERA5做偏差分析，并得到统计值。）

 H8 and ERA5 were analyzed and the statistical values were obtained. 

**3.H8_JRA55_analyze**

（H8与JRA55做偏差分析，并得到统计值。）

 H8 and JRA55 were analyzed and the statistical values were obtained. 

**4.H8_MERRA2_analyze**

（H8与MEARR2做偏差分析，并得到统计值。）

 H8 and MERRA2 were analyzed and the statistical values were obtained. 

**5.simple_contrast**

（H8与其他三个再分析资料的单一时次的对比图绘制。）

 A single-time comparison of H8 data with the other three reanalysis data was drawn. 

**6.plot_picture_function、plot_bias_function**

（自定义绘图函数。）

 Custom drawing functions. 

**7.plot_hist2d**

（读取H8与AMSR的匹配数据[AMSR_nc]，并绘制二维直方图。）

The matching data of H8 and AMSR (AMSR_nc) are read and 2-dimensional histogram is drawn.

**8.Grid_picture_plot**

(偏差与原数据组合图的绘制。 )

The drawing of some combination graphs in the paper.