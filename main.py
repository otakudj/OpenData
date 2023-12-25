from opendatatools import economy
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from matplotlib.font_manager import FontManager
import matplotlib
matplotlib.rc("font", family='Microsoft YaHei')

graphs_name = ['M1-M2增速差', '居民消费价格指数(上年同月=100)']


def plot_line_graph(i, date, value):
    x_axis_data = date.values[:0:-1]  # x
    y_axis_data = value.values[:0:-1]

    plt.subplot(2, 2, i)

    plt.plot(x_axis_data, y_axis_data, 'bo-', alpha=1, linewidth=1, label=graphs_name[i])  # 'bo-'表示蓝色实线，数据点实心原点标注
    # plot中参数的含义分别是横轴值，纵轴值，线的形状（'s'方块,'o'实心圆点，'*'五角星   ...，颜色，透明度,线的宽度和标签 ，

    plt.legend()  # 显示上面的label
    plt.xlabel('年月')  # x_label
    plt.ylabel('同比增长')  # y_label

    plt.xticks(rotation=45, fontsize=8)
    tick_spacing = 12
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(3))


# M1 - M2
df, msg = economy.get_M0_M1_M2()

M1 = df[df['indicator_name'] == '货币(M1)供应量_同比增长(%)'][['date', 'value']].reset_index(drop=True)
M2 = df[df['indicator_name'] == '货币和准货币(M2)供应量_同比增长(%)'][['date', 'value']].reset_index(drop=True)

for m1, m2 in zip(M1['date'].values, M2['date'].values):
    assert m1 == m2

date = M1['date']  # x
value = M1['value'] - M2['value']  # y

plot_line_graph(0, date, value)

# CPI
df, msg = economy.get_cpi()

CPI = df[df['indicator_name'] == '居民消费价格指数(上年同月=100)'][['date', 'value']].reset_index(drop=True)

date = CPI['date']

value = CPI['value'] - 100

plot_line_graph(1, date, value)

# retail

# plt.ylim(-1,1)#仅设置y轴坐标范围
# plt.show()
