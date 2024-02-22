from opendatatools import stock, fund
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from styleframe import StyleFrame
import seaborn as sns
import pandas as pd
# import matplotlib.pyplot as plt

# sns.set_style(rc={'font.sans-serif': "Microsoft Yahei"})
# plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']

# from matplotlib import font_manager
# my_font = font_manager.FontProperties(fname="wryh.ttc")
#
import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']
# plt.rcParams['axes.unicode_minus'] = False

days = 100

now = datetime.now()
end_date = now.strftime('%Y-%m-%d')
# near one season
start_date = (now - timedelta(days=days)).strftime('%Y-%m-%d')

# 国证指数
index_dict = {
    '399373.SZ': '大盘价值',
    '399375.SZ': '中盘价值',
    '399377.SZ': '小盘价值',
    '399372.SZ': '大盘成长',
    '399374.SZ': '中盘成长',
    '399376.SZ': '小盘成长',
}

# 基金列表
fund_dict = {
    '160119': '中证500',
    '202015': '沪深300',
    '002656': '创业板',
    '011608': '科创50',
    '016630': '中证1000',
    '510050': '上证50'
}
df_total = None
for symbol in index_dict.keys():
    df, msg = stock.get_daily(symbol, start_date=start_date, end_date=end_date)
    # if x_date is None:
    #     x_date = [str(t).split(' ')[0] for t in df['time']]
    # else:
    #     assert [str(t).split(' ')[0] for t in df['time']] == x_date
    cur_df = pd.DataFrame(
        {symbol: df['last'].values},
        index=[str(t).split(' ')[0] for t in df['time']]
    )
    if df_total is None:
        df_total = cur_df
    else:
        df_total = df_total.join(cur_df)

for symbol in fund_dict.keys():
    df, msg = fund.get_fund_nav(symbol)
    cur_df = pd.DataFrame(
        {symbol: df['nav1'].values},
        index=df['date']
    )
    df_total = df_total.join(cur_df)

np_total = df_total.values.astype(float)
np_delta = (np_total[1:] - np_total[:-1]) / np_total[:-1]

cc = np.corrcoef(np_delta, rowvar=False)
np_cov = cc[:len(index_dict), -len(fund_dict):]

fund_names = [f'{value}\n{key}' for key, value in fund_dict.items()]
index_names = [f'{value}\n{key}' for key, value in index_dict.items()]

df_cov = pd.DataFrame(np_cov, columns=fund_names, index=index_names)

excel_writer = StyleFrame.ExcelWriter(f'cov_{days}.xlsx')
sf = StyleFrame(df_cov)
sf.to_excel(
    excel_writer=excel_writer,
    best_fit=fund_names,
    index=True
)
excel_writer.save()


# plt.rcParams['font.family'] = 'Times New Roman' # 设置英文字体为Times New Roman
plt.figure(figsize=(10,8))#figsize可以规定热力图大小
plt.xticks(size=18,fontproperties='Microsoft Yahei',weight='bold')
plt.yticks(size=18,fontproperties='Microsoft Yahei',weight='bold')
fig = sns.heatmap(df_cov, #所绘数据
                  cmap='coolwarm', #颜色
                annot=True,fmt='.3g',#annot为热力图上显示数据；结果保留3位数字
                annot_kws={'size': 18, 'style': 'normal', #字体大小和格式
                           'family':'Times New Roman','weight': 'bold'}, #字体和风格--加粗
                linewidths=3, #图框分割线宽度
                square=True,  #使每个图框大小一致
                cbar = True) #绘制图例
cbar = fig.collections[0].colorbar
cbar.ax.tick_params(labelsize=20)  #设置图例字体大小
plt.savefig(f'cov_{days}.jpg', dpi=100, bbox_inches='tight')
print('@')
