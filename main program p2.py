import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


def get_month(year_month):
    return int(year_month[5:7])


matplotlib.rcParams['font.family'] = 'SimHei'
df = pd.read_excel('1.1.xls')
df['年份'] = df.apply(lambda x: "2018" if "2018" in x['日期'] else "2019", axis=1)
df['月份'] = df.apply(lambda x: get_month(x['日期']), axis=1)
# print(df)
year_df = df['年份'].value_counts().sort_values()
print(year_df)
year_df.plot(kind='bar', color=['c', 'b', 'r', 'm', 'y'])
plt.xticks(rotation=0)
plt.title('每年报道总量统计', fontproperties='SimHei', size=15)
plt.xlabel('年份', fontproperties='SimHei', size=10)
plt.ylabel('报道量', fontproperties='SimHei', size=10)
plt.show()

# month_year_list = sorted(list(df['日期'].unique()))
# print(month_year_list)


def get_year_plot(year):
    month_df = df.loc[(df['年份'] == year)]["月份"].value_counts().sort_index()
    month_df.plot(kind='bar', color=['r', 'g', 'b', 'm', 'y'])
    plt.xticks(rotation=0)
    plt.title(year + "年每个月的报道量 ", fontproperties='SimHei', size=15)
    plt.xlabel('月份', fontproperties='SimHei', size=10)
    plt.ylabel('报道量', fontproperties='SimHei', size=10)
    plt.show()


get_year_plot("2018")
get_year_plot("2019")

