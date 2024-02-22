from opendatatools import economy
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from time import sleep
import numpy as np
import pandas as pd

from matplotlib.font_manager import FontManager
import matplotlib
matplotlib.rc("font", family='Microsoft YaHei')

from data import date_gen, social_financing

config = [
    [
        {
            'func': 'get_cpi',
            'title': 'CPI',
            'utils': ['居民消费价格指数(上年同月=100)'],
            'range': 86,
        },
        {
            'func': 'get_gdp_q',
            'title': 'GDP',
            'utils': ['分季国内生产总值指数'],
            'unit': 'season',
            'range': 29,
        },
    ], [
        {
            'func': 'get_M0_M1_M2',
            'title': 'M1-M2增速差',
            'utils': ['货币(M1)供应量_同比增长(%)', '货币和准货币(M2)供应量_同比增长(%)'],
        },
    ], [
        {
            'func': 'get_ppi',
            'title': 'PPI',
            'utils': ['工业生产者出厂价格指数(上年同月=100)'],
        },
        {
            'func': '',
            'title': '社融',
            'utils': ['社会融资规模存量同比'],
        },
    ], [
        {
            'func': 'get_retail_sales',
            'title': '社零',
            'utils': ['社会消费品零售总额_同比增长(%)'],
        },
    ]
]

rows, columns = 2, 3


def plot_line_graph(ax, title_list, unit_list, date, value_list):
    x_axis_data = date.values  # x
    y_axis_data = value_list[0].values

    x_axis_data = [date[:4] + '-' + date[4:] for date in x_axis_data]

    ax.set_title('&'.join(title_list))
    x_tmp = [i for i in range(85)]
    ax.plot(x_tmp, y_axis_data, 'bo-', alpha=1, linewidth=1, label=title_list[0])  # 'bo-'表示蓝色实线，数据点实心原点标注
    # plot中参数的含义分别是横轴值，纵轴值，线的形状（'s'方块,'o'实心圆点，'*'五角星   ...，颜色，透明度,线的宽度和标签 ，

    # plt.legend()  # 显示上面的label
    # ax.set_xlabel('年月')  # x_label
    ax.set_ylabel('同比增长')  # y_label
    ax.legend(loc='upper left')

    if len(unit_list) == len(value_list) == 2:
        if unit_list[1] == 'season':
            x_twin_tmp = x_axis_data[::3]
        else:
            x_twin_tmp = x_axis_data

        y_axis_data_twin = value_list[1].values
        ax_twin = ax.twinx()
        ax_twin.plot(x_twin_tmp, y_axis_data_twin, 'ro-', alpha=1, linewidth=1, label=title_list[1])  # 'bo-'表示蓝色实线，数据点实心原点标注
        ax_twin.legend(loc='upper right')

    # ax.set_xticks(x_axis_data)
    ax.tick_params(axis='x', labelrotation=45)
    tick_spacing = 12
    if unit_list[0] == 'month':
        ax.xaxis.set_major_locator(ticker.MultipleLocator(3))


def data_preprocess(func, title, utils, unit, duration):
    if func != '':
        print(f'{func} ...', end='')
        rsp, msg = getattr(economy, func)(duration)
        sleep(3)
        df = rsp[rsp['indicator_name'] == utils[0]][['date', 'value']].reset_index(drop=True)
        date = df['date']  # x

        if func == 'get_M0_M1_M2':
            df_attach = rsp[rsp['indicator_name'] == utils[1]][['date', 'value']].reset_index(drop=True)
            for m1, m2 in zip(df['date'].values, df_attach['date'].values):
                assert m1 == m2
            value = df['value'] - df_attach['value']  # y
        elif func in ['get_cpi', 'get_gdp_q', 'get_ppi']:
            value = df['value'] - 100
        else:
            value = df['value']

        value = value[::-1]
        date = date[::-1]

        # remove last invalid data
        if unit == 'month':
            value = value[:-1]
            date = date[:-1]
    else:
        date = pd.Series(date_gen)

        if title == '社融':
            print(f'{title} ...', end='')
            value = pd.Series(social_financing[-37:])

        date = date[::-1]

    if unit == 'season':
        date = date[-41:]
        value = value[-41:]
    elif unit == 'year':
        date = date[-4:]
        value = value[-4:]

    return date, value


if __name__ == '__main__':
    unit = 5
    fig, ax = plt.subplots(rows, columns, figsize=(columns * unit, rows * unit))

    for ind, values in enumerate(config):
        title_list, unit_list, value_list, date_list = [], [], [], []
        for value in values:
            func = value['func']
            title = value['title']
            utils = value['utils']
            unit = value.get('unit', 'month')
            duration = value.get('range', '38')

            date, value = data_preprocess(func, title, utils, unit, duration)

            title_list.append(title)
            unit_list.append(unit)
            value_list.append(value)
            date_list.append(date)

        plot_line_graph(ax[ind // columns][ind % columns], title_list,
                        unit_list, date_list[0], value_list)
        print('Done')
        break

    # # CPI
    # print('CPI ...', end='')
    # ind = 1
    # df, _ = economy.()
    #
    # CPI = df[df['indicator_name'] == graphs_name[ind]][['date', 'value']].reset_index(drop=True)
    # date = CPI['date']
    # value = CPI['value'] - 100
    #
    # plot_line_graph(ind, date, value)
    # sleep(3)
    # print('Done')
    #
    # # retail
    # print('Retail Sales ...', end='')
    # ind = 2
    # df, _ = economy.get_retail_sales()
    # Retail = df[df['indicator_name'] == graphs_name[ind]][['date', 'value']].reset_index(drop=True)
    #
    # date = Retail['date']
    # value = Retail['value']
    #
    # plot_line_graph(ind, date, value)
    # sleep(3)
    # print('Done')
    fig.tight_layout()
    # plt.ylim(-1,1)#仅设置y轴坐标范围
    plt.savefig(f'macro.jpg', dpi=100, bbox_inches='tight')
