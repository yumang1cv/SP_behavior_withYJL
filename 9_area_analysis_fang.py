# -*- coding:utf-8 -*-
# @FileName  :9_area_analysis_fang.py
# @Time      :2022/4/26 10:07
# @Author    :XuYang
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import math
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

matplotlib.use('Qt5Agg')


def search_csv(path=".", name=""):  # 抓取csv文件
    result = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            search_csv(item_path, name)
        elif os.path.isfile(item_path):
            if name + ".csv" == item:
                # global csv_result
                # csv_result.append(name)
                result.append(item_path)
                # print(csv_result)
                # print(item_path + ";", end="")
                # result = item
    return result


def read_csv(path='.', name="", column="", element=""):
    """
    Unique_serial_number:1,2,...,438          date:20210916
    mouse:#13                                 gender:female/male
    ExperimentTime:day/night                  origin_seg:1,2,3
    re_seg_Index:1,2,...,73                   split_number:1,2,...,6
    coordinate_file:calibrationimages_XY20210916_1
    """
    item_path = os.path.join(path, name)
    with open(item_path, 'rb') as f:
        df = pd.read_excel(f)

    df1 = df.set_index([column])  # 选取某一列数据
    sel_data = df1.loc[element]  # 根据元素提取特定数据

    return sel_data


def choose_data(dataframe, column="", element=""):
    df = dataframe.loc[dataframe[column].isin([element])]  # 限定条件挑选数据(二次限定使用)

    return df


def normliza_data(data1, data_name=''):
    size = int(len(data1) / 2)
    norm_data = np.array(data1[data_name]).reshape(size, 2)
    scaler = MinMaxScaler(feature_range=(-24, 24))  # 计算圆弧使用
    # scaler = MinMaxScaler(feature_range=(1, 49))  # 计算 50*50 小方格使用
    norm = scaler.fit(norm_data)
    norm_data = scaler.transform(norm_data)
    norm_data = norm_data.reshape(len(data1), 1)

    return norm_data


def nine_area_analysis(file_list, length):  # 传统 9 区域分析   边长按照 1 : 2 : 1 划分

    boundary = length / 4
    angle_time = []
    center_time = []
    line_time = []

    for file_num in range(len(csv_FD)):

        data1 = pd.read_csv(csv_FD[file_num])
        data2 = data1.iloc[2:, 4:7]

        x = 0  # 四角时间
        y = 0  # 边界时间
        z = 0  # 中心时间
        for i in range(len(data2)):
            if (data2['x'].iloc[i] >= boundary and data2['y'].iloc[i] >= boundary) or \
                    (data2['x'].iloc[i] <= -boundary and data2['y'].iloc[i] <= -boundary) or \
                    (data2['x'].iloc[i] <= -boundary and data2['y'].iloc[i] >= boundary) or \
                    (data2['x'].iloc[i] >= boundary and data2['y'].iloc[i] <= -boundary):
                x = x + 1

            elif (-boundary <= data2['x'].iloc[i] <= boundary <= data2['y'].iloc[i]) or \
                    (boundary >= data2['x'].iloc[i] >= -boundary >= data2['y'].iloc[i]) or \
                    (-boundary <= data2['y'].iloc[i] <= boundary <= data2['x'].iloc[i]) or \
                    (boundary >= data2['y'].iloc[i] >= -boundary >= data2['x'].iloc[i]):
                y = y + 1

            # elif np.abs(data2['x'].iloc[i]) <= 125 and np.abs(data2['y'].iloc[i]) <= 125:
            else:
                z = z + 1

        angle_time.append(x / 30)
        line_time.append(y / 30)
        center_time.append(z / 30)

    return angle_time, center_time, line_time


if __name__ == '__main__':

    a = read_csv(path=r'D:/3D_behavior/Spontaneous_behavior/result_fang',
                 name="video_info.xlsx", column='roundTime', element=1)

    A = choose_data(a, column='ExperimentTime', element='day')
    B = choose_data(A, column='gender', element='male')
    angle_time_all = []
    center_time_all = []
    line_time_all = []
    for time_state in range(1, 7):
        # time_state = 1
        # 多条件筛选
        X = choose_data(a, column='split_number', element=time_state)  # split_number=1 not have ''
        df_day = pd.DataFrame(X, columns=["Unique_serial_number"])
        # data = df_day.values.tolist()
        csv_FD = []
        for item in tqdm(df_day['Unique_serial_number']):
            csv_result3 = search_csv(
                path=r"D:/3D_behavior/Spontaneous_behavior/result_fang/3Dskeleton/back_coordinates_origin/",
                name="rec-{}-G1-2022114230_Cali_Data3d_Replace".format(item))
            csv_FD.append(csv_result3[0])

        angle_time_single, center_time_single, line_times_single = nine_area_analysis(csv_FD, length=500)

        angle_time_all.append(angle_time_single)
        center_time_all.append(center_time_single)
        line_time_all.append(line_times_single)

        print('第{}分钟已处理结束'.format(time_state*10))









    """
        传统 9 区域分析   边长按照 1 : 2 : 1 划分
    """
    # angle_time = []
    # center_time = []
    # line_time = []
    #
    # for file_num in range(len(csv_FD)):
    #
    #     data1 = pd.read_csv(csv_FD[file_num])
    #     data2 = data1.iloc[2:, 4:7]
    #
    #     x = 0  # 四角时间
    #     y = 0  # 边界时间
    #     z = 0  # 中心时间
    #     for i in range(len(data2)):
    #         if (data2['x'].iloc[i] >= 125 and data2['y'].iloc[i] >= 125) or \
    #                 (data2['x'].iloc[i] <= -125 and data2['y'].iloc[i] <= -125) or \
    #                 (data2['x'].iloc[i] <= -125 and data2['y'].iloc[i] >= 125) or \
    #                 (data2['x'].iloc[i] >= 125 and data2['y'].iloc[i] <= -125):
    #             x = x + 1
    #
    #         elif (125 >= data2['x'].iloc[i] >= -125 and data2['y'].iloc[i] >= 125) or \
    #                 (125 >= data2['x'].iloc[i] >= -125 >= data2['y'].iloc[i]) or \
    #                 (125 >= data2['y'].iloc[i] >= -125 and data2['x'].iloc[i] >= 125) or \
    #                 (125 >= data2['y'].iloc[i] >= -125 >= data2['x'].iloc[i]):
    #             y = y + 1
    #
    #         # elif np.abs(data2['x'].iloc[i]) <= 125 and np.abs(data2['y'].iloc[i]) <= 125:
    #         else:
    #             z = z + 1
    #
    #     angle_time.append(x / 30)
    #     center_time.append(y / 30)
    #     line_time.append(z / 30)


