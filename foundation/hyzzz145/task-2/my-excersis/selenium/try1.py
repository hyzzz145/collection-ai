import numpy as np
import pandas as pd

df = pd.DataFrame({
    '姓名': ['小明', '小红', '小刚', '小丽', '小强'],
    '语文': [85, 92, 78, 88, 95],
    '数学': [90, 88, 95, 70, 82],
    '英语': [80, 85, 90, 92, 78]
})
avg = df.pivot_table(index='姓名',
                     values=['语文', '数学', '英语'],
                     aggfunc='mean')
print(avg)

# 每个学生的总平均（对三科再平均）
each_avg = avg.mean(axis=1)

# NumPy 找最大值对应的人
idx = np.argmax(each_avg.values)
best = each_avg.index[idx]
print('平均分最高：', best, each_avg.values[idx])

