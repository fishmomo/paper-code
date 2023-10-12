from netCDF4 import Dataset
import xarray as xr
import numpy as np
from datetime import datetime
from datetime import timedelta
import time

dataERA5 = xr.open_dataset('E:/ZiYuanPingGu/ERA5/contain_cloudcover/202001.nc')#读取ERA5 20200101整日数据
lon = dataERA5.longitude#经度
lat = dataERA5.latitude#维度
x2, y2 = np.meshgrid(lon, lat)#转化为坐标数据格式

st = '2022-01-01_00:00'
et = '2022-01-31_23:00'
d1 = datetime.strptime(st,'%Y-%m-%d_%H:%M')#type:str--->datetime
d2 = datetime.strptime(et,'%Y-%m-%d_%H:%M')

step = timedelta(minutes = 10)#设置datetime.timedelta类型的步进
seconds = (d2-d1).total_seconds()#转换成分钟   其中d2-d1为datetime.timedelta类型  timedelta只能储存days，seconds，microseconds

files = []
for i in range(0, int(seconds)+1, int(step.total_seconds())):
    if (d1 + timedelta(seconds=i)).minute == 0:
        files.append(d1 + timedelta(seconds=i))

filesname = [date.strftime('%Y%m/%d/%H/') +
         f'NC_H08_{date.strftime("%Y%m%d_%H%M")}_L2CLP010_FLDK.02401_02401.nc'
         for date in files]

ERA5_data = np.zeros([dataERA5.dims['time'], 3, 161, 221])
JRA55_data = np.zeros([dataERA5.dims['time'], 3, 33, 45])
MERRA2_data = np.zeros([dataERA5.dims['time'], 3, 81, 111])




def Get_Bias(H8filesname):

    def Get_H8lonlatindex(inputlon, inputlat):#获取80-135E，55-15N范围内对应的索引
        outputlon = round((inputlon - 80)/0.05)
        outputlat = round(-(inputlat - 60)/0.05)
        return outputlon, outputlat

    def transformH8(data1, data2, resolution1, resolution2):#data1是局部数据，data2为全域数据，避免单独处理边缘格点
        num = round((resolution1/resolution2 - 1) / 2)#匹配方框区域格点半边长
        trans_array = np.ones(data1.shape)

        for i in range(data1.shape[0]):
            for j in range(data1.shape[1]):
                lon = 80 + j*resolution1
                lat = 55 - i*resolution1
    #             print('lon:{0}, lat:{1}'.format(lon, lat))
                H8_lonindex, H8_latindex = Get_H8lonlatindex(lon, lat)

                lat_w = H8_latindex-num
                if j == 0:
                    temp_array = data2[H8_latindex-num:H8_latindex+num+1, H8_lonindex:H8_lonindex+num+1]
                    data_num = len(temp_array.flatten())
                    trans_array[i, j] = np.sum(temp_array[~np.isnan(temp_array)])/data_num

                else:         
                    temp_array = data2[H8_latindex-num:H8_latindex+num+1, H8_lonindex-num:H8_lonindex+num+1]
                    datanum = len(temp_array.flatten())
                    trans_array[i, j] = np.mean(temp_array[~np.isnan(temp_array)])
        return trans_array

    def transformCLoudH8(data1, data2, resolution1, resolution2):#data1是局部数据，data2为全域数据，避免单独处理边缘格点
        num = round((resolution1/resolution2 - 1) / 2)#匹配方框区域格点半边长
        trans_array = np.zeros(data1.shape)
        
        # treshold_u = round((resolution1/resolution2 - 1)**2*0.8)#一般情况下的阈值个数（80%的条件）
        total_num = (resolution1/resolution2 - 1)**2
        for i in range(data1.shape[0]):
            for j in range(data1.shape[1]):
                lon = 80 + j*resolution1
                lat = 55 - i*resolution1
    #             print('lon:{0}, lat:{1}'.format(lon, lat))
                H8_lonindex, H8_latindex = Get_H8lonlatindex(lon, lat)
                if j == 0:
                    temp_array = data2[H8_latindex-num:H8_latindex+num+1, H8_lonindex:H8_lonindex+num+1]
                    data_num = len(temp_array.flatten())
                    # treshold = round(datanum * 0.8)
                    # if np.sum(temp_array > 0.8) >= treshold:
                    trans_array[i, j] = np.sum(temp_array[~np.isnan(temp_array)])/data_num

                else:
                    temp_array = data2[H8_latindex-num:H8_latindex+num+1, H8_lonindex-num:H8_lonindex+num+1]
                    data_num = len(temp_array.flatten())
                    # if np.sum(temp_array > 0.8) >= treshold_u:
                    trans_array[i, j] = trans_array[i, j] = np.sum(temp_array[~np.isnan(temp_array)])/data_num
        return trans_array

    def slice_str(str1, st, ed):
        return str1[st:ed]

    print('start!')

    datakuihua = xr.open_dataset('H:/ZiYuanPingGu/hiwimari8_data/hiwamari/' + H8filesname)
    print('IO------over')
    
    lon_w = 0#索引，下同
    lon_e = 1100
    lat_n = 100
    lat_s = 900
    
    #验证经纬度是否有错

    #这部分代码会重复利用，目的就是从H8源文件提取想要的数据。
    binary_repr_v = np.vectorize(np.binary_repr)
    slice_str_v = np.vectorize(slice_str)
    qa = datakuihua.QA
    qa_int = qa.data
    qa_int = qa_int.astype(np.int)
    qa_bin = binary_repr_v(qa_int, 16)
    st = time.time()
    qa65 = slice_str_v(qa_bin, 9, 11)
    qasc = slice_str_v(qa_bin, -5, -3)
    #云水、云冰检测
    
    # qa65 = np.array([qa_bin[i][j][9:11] for i in range(len(qa_bin)) for j in range(len(qa_bin))])
    #云检测
    # qasc = np.array([qa_bin[i][j][-5:-3] for i in range(len(qa_bin)) for j in range(len(qa_bin))])

    qa65 = qa65.reshape(2401,2401)
    qasc = qasc.reshape(2401,2401)
    qa_wc = np.zeros([2401, 2401])*np.nan#水云数据矩阵初始化
    qa_ic = np.zeros([2401, 2401])*np.nan
    qa_cloud = np.zeros([2401, 2401])
    qa_wc[qa65 == '01'] = 1
    qa_ic[qa65 == '11'] = 1
    qa_cloud[qasc == '11'] = 1
    print('clear ?:', np.all(qa_cloud == 0)) #False就对了
    et = time.time()
    # print("IO time cost:", et-st)
    #匹配空间分辨率
    ct = datakuihua.CLOT.values#[lat_n:lat_s+1:5,lon_w:lon_e+1:5]
    cr = datakuihua.CLER_23.values#[lat_n:lat_s+1:5,lon_w:lon_e+1:5]
    clt = datakuihua.CLTT.values#[lat_n:lat_s+1:5,lon_w:lon_e+1:5]

    #剔除无效值
    cr[cr < -326] = np.nan
    ct[ct < -326] = np.nan
    
    print('cr shape:', cr.shape)
    
    H8lwp = ct * cr * 5/9 * 0.001
    lwp_qa = qa_wc * H8lwp
    #剔除温度大于268华氏摄氏度的格点
    lwp_qa[clt < 268] = np.nan
    lwparray_asERA5 = transformH8(np.zeros([161,221]), lwp_qa, 0.25, 0.05)
    lwparray_asJRA55 = transformH8(np.zeros([33,45]), lwp_qa, 1.25, 0.05)
    lwparray_asMERRA2 = transformH8(np.zeros([81,111]), lwp_qa, 0.5, 0.05)
    
    H8iwp = (ct**(1/0.84))/0.065 * 0.001
    iwp_qa = qa_ic * H8iwp
#     iwp_ori = iwp_qa
    # iwp_qa[clt < 268] = np.nan     
    iwparray_asERA5 = transformH8(np.zeros([161,221]), iwp_qa, 0.25, 0.05)
    iwparray_asJRA55 = transformH8(np.zeros([33,45]), iwp_qa, 1.25, 0.05)
    iwparray_asMERRA2 = transformH8(np.zeros([81,111]), iwp_qa, 0.5, 0.05)
    
    #处理cloud_sc 标签
    scarray_asERA5 = transformCLoudH8(np.zeros([161,221]), qa_cloud, 0.25, 0.05)
    scarray_asJRA55 = transformCLoudH8(np.zeros([33,45]), qa_cloud, 1.25, 0.05)
    scarray_asMERRA2 = transformCLoudH8(np.zeros([81,111]), qa_cloud, 0.5, 0.05)
    
    et = time.time()
    print("CPU time cost:", et-st)
    H8_bar = np.array([lwp_qa, iwp_qa, qa_cloud])
    ERA5_bar = np.array([lwparray_asERA5, iwparray_asERA5, scarray_asERA5])
    JRA55_bar = np.array([lwparray_asJRA55, iwparray_asJRA55, scarray_asJRA55])
    MERRA2_bar = np.array([lwparray_asMERRA2, iwparray_asMERRA2, scarray_asMERRA2])

    print(H8filesname + ':over!')
    return H8_bar, ERA5_bar, JRA55_bar, MERRA2_bar

from concurrent.futures import ProcessPoolExecutor, as_completed

if __name__ == '__main__':
    st = time.time()
    num_cpus = 2 
    fileindex = 0
    with ProcessPoolExecutor(max_workers=num_cpus) as pool:
        # pool.map(Get_Bias, tuple(filesname[0:3]))
        # 提交任务并获取 Future 对象列表
        futures = [pool.submit(Get_Bias, argument) for argument in filesname[0:10]]

        # 获取每个任务的结果
        results = []
        for future in as_completed(futures):
            result = future.result()  # 获取任务的结果
            ERA5_data[fileindex,:,:,:] =  result[1]#ERA5_bar
            JRA55_data[fileindex,:,:,:] =  result[2]#JRA55_bar
            MERRA2_data[fileindex,:,:,:] =  result[3]#MERRA2_bar
            fileindex += 1
            # results.append(result)
            # print(len(result), type(result))
        print(ERA5_data[0])
        # 在这里可以对结果进行进一步处理或保存
        # ...
    et = time.time()
    print('over! cost time:', et-st)  