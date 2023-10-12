
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

def add_Chinese_provinces(ax, **kwargs):
    '''
    给一个GeoAxes添加中国省界.

    Parameters
    ----------
    ax : GeoAxes
        被绘制的GeoAxes,投影不限.

    **kwargs
        绘制feature时的Matplotlib关键词参数,例如linewidth,facecolor,alpha等.

    Returns
    -------
    None
    '''
    proj = ccrs.PlateCarree()#投影方式，平面投影
    shp_filepath = r'E:\邢台观测站\python_qixianglianxi\shp\China\china.shp'#读取shp文件，注意文件中应包括除shp外，
    #prj,shx等文件
    reader = Reader(shp_filepath)
    provinces = cfeature.ShapelyFeature(reader.geometries(), proj)
    ax.add_feature(provinces, **kwargs)

def set_map_ticks(ax, dx=60, dy=30, nx=0, ny=0, labelsize='medium'):
    '''
    为PlateCarree投影的GeoAxes设置tick和tick label.
    需要注意,set_extent应该在该函数之后使用.

    Parameters
    ----------
    ax : GeoAxes
        需要被设置的GeoAxes,要求投影必须为PlateCarree.

    dx : float, default: 60
        经度的major ticks的间距,从-180度开始算起.默认值为60.

    dy : float, default: 30
        纬度的major ticks,从-90度开始算起,间距由dy指定.默认值为60.

    nx : float, default: 0
        经度的minor ticks的个数.默认值为0.

    ny : float, default: 0
        纬度的minor ticks的个数.默认值为0.

    labelsize : str or float, default: 'medium'
        tick label的大小.默认为'medium'.

    Returns
    -------
    None
    '''
    if not isinstance(ax.projection, ccrs.PlateCarree):#判断是否为平面投影
        raise ValueError('Projection of ax should be PlateCarree!')
    proj = ccrs.PlateCarree()   # 专门给ticks用的crs.

    # 设置x轴.
    major_xticks = np.arange(-180, 180 + 0.9 * dx, dx)
    ax.set_xticks(major_xticks, crs=proj)
    if nx > 0:
        ddx = dx / (nx + 1)
        minor_xticks = np.arange(-180, 180 + 0.9 * ddx, ddx)#这个操作我不懂，又好像是末位取不到
        ax.set_xticks(minor_xticks, minor=True, crs=proj)

    # 设置y轴.
    major_yticks = np.arange(-90, 90 + 0.9 * dy, dy)
    ax.set_yticks(major_yticks, crs=proj)
    if ny > 0:
        ddy = dy / (ny + 1)
        minor_yticks = np.arange(-90, 90 + 0.9 * ddy, ddy)
        ax.set_yticks(minor_yticks, minor=True, crs=proj)

    # 为tick label增添度数标识.
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.tick_params(labelsize=labelsize)

