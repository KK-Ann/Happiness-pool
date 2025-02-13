import pandas as pd

# 读取Excel文件
df = pd.read_excel('上海-休闲娱乐data.xls')
df2 = pd.read_excel('上海景点.xls')

# 筛选小分类为演出场馆、剧场/剧院、艺术中心/文化广场的数据
filtered_data = df[df['小分类'].isin(['演出场馆', '剧场/剧院', '艺术中心/文化广场'])]
filtered_data = filtered_data._append(df2[df2['小分类'] != '旅行社'])

# 将筛选后的数据保存为 CSV 文件
filtered_data.to_csv('filtered_venue.csv', index=False)



