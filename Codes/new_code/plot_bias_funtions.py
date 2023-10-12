import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
import cartopy.crs as ccrs
from plot_picture_function import set_map_ticks, add_Chinese_provinces
import numpy as np

def Round_level(values_max, values_min, level):
    if abs(values_max) >= abs(values_min):
        level_limit = round(abs(values_max)*0.8, level)
    else:
        level_limit = round(abs(values_min)*0.8, level)
    print("level_limit :", level_limit)
    if (level_limit == 0) | (level_limit == 1/10**(level)):
        return Round_level(values_max, values_min, level=level+1)
    else:
        print("level:", level)
        return level_limit

def Plot_ComparedPic(x, y, data1, data2, picname, title1, title2, colorp, directionLevels=True, decascale=False):

    X, Y = np.meshgrid(x, y)

    extent = [80, 135, 15, 55]#100E--110E,25N--35N
    proj = ccrs.PlateCarree()#选择投影方式，平面投影
    fig = plt.figure(figsize=(9,6), dpi=1000)
    ax1 = fig.add_subplot(211, projection=proj)#创建一个轴，或者是说主体
    # 设置经纬度刻度.
    set_map_ticks(ax1, dx=10, dy=10, nx=1, ny=1, labelsize='small')#自定义函数set_map_tick
    add_Chinese_provinces(ax1, lw=0.5, ec='gray', fc='none')#后两个参数是设置eagecolor,facecolor,linewigth线宽
    ax1.set_extent(extent, crs=proj)
    ax1.set_title(title1, fontsize=8)

    value_max = max(np.nanmax(data1), np.nanmax(data2))
    value_min = min(np.nanmin(data1), np.nanmin(data2))
    print("value_max:{}, value_min:{}".format(value_max, value_min))
    level_limit = Round_level(value_max, value_min, level=1)
    #是否需要双向色标轴    
    if directionLevels:
        levels = np.linspace(0, level_limit, 11)
        extend_str = 'max'
    else:
        levels = np.linspace(-level_limit, level_limit, 11)
        extend_str = 'both'
    im1 = ax1.contourf(X, Y, data1, cmap = colorp, levels = levels, extend=extend_str)

    cax1 = fig.add_axes([ax1.get_position().x1 + 0.03, ax1.get_position().y0, 0.02, ax1.get_position().height])
    plt.colorbar(im1, cax=cax1)

    ax2 = fig.add_subplot(212, projection=proj)#创建一个轴，或者是说主体
    # 设置经纬度刻度.
    set_map_ticks(ax2, dx=10, dy=10, nx=1, ny=1, labelsize='small')#自定义函数set_map_tick
    add_Chinese_provinces(ax2, lw=0.5, ec='gray', fc='none')#后两个参数是设置eagecolor,facecolor,linewigth线宽
    ax2.set_extent(extent, crs=proj)
    ax2.set_title(title2, fontsize=8)

    if decascale:
        levels = levels/10
    im2 = ax2.contourf(X, Y, data2, cmap = colorp, levels = levels, extend=extend_str)

    cax2 = fig.add_axes([ax2.get_position().x1 + 0.03, ax2.get_position().y0, 0.02, ax2.get_position().height])
    plt.colorbar(im2, cax=cax2)
#     plt.savefig(f'D:/python project/python_qixianglianxi/ZiYuanPingGu/analyze_draw/{picname}.png',
#                 dpi=100,
#                 bbox_inches = 'tight'
#     #             facecolor = 'g',
#     #             edgecolor = 'b'
#                )
    plt.show()