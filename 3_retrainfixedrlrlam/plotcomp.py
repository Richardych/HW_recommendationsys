import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
# 必须配置中文字体，否则会显示成方块
# 注意所有希望图表显示的中文必须为unicode格式
font_size = 10 # 字体大小
fig_size = (8, 6) # 图表大小
names = (u'train_RMSE', u'train_MRR') # 姓名
subjects = (u'one', u'two', u'three',u'four',u'five',u'withoutRegu') # 科目
#scores = ((0.9038564662058626, 0.9000283363220195, 0.8996683253780979, 0.9029435650977378, 0.9019978759563007, 0.9654190049412967), (0.1459193383755506, 0.14593167580675806, 0.14596022622931534, 0.14599121487015698, 0.1462305335171043, 0.14512023037764532)) # 成绩
#scores = ((0.90385, 0.90002, 0.89966, 0.90294, 0.90199, 0.96541), (0.14591, 0.14593, 0.14596, 0.14599, 0.14623, 0.14512)) # test
scores = ((0.88952, 0.88660, 0.88737, 0.88930, 0.88840, 0.86711), (0.14625, 0.14620, 0.14624, 0.14616, 0.14597, 0.14615)) # train

# 更新字体大小
mpl.rcParams['font.size'] = font_size
# 更新图表大小
mpl.rcParams['figure.figsize'] = fig_size
# 设置柱形图宽度
bar_width = 0.35
index = np.arange(len(scores[0]))
# 绘制「小明」的成绩
rects1 = plt.bar(index, scores[0], bar_width, color='#0072BC', label=names[0])
# 绘制「小红」的成绩
rects2 = plt.bar(index + bar_width, scores[1], bar_width, color='#ED1C24', label=names[1])
# X轴标题
plt.xticks(index + bar_width/2, subjects)
# Y轴范围
plt.ylim(ymax=1.0, ymin=0)
# 图表标题
plt.title(u'Train RMSE and Train MRR')
# 图例显示在图表下方
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=5)
# 添加数据标签
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
        # 柱形图边缘用白色填充，纯粹为了美观
        rect.set_edgecolor('white')
add_labels(rects1)
add_labels(rects2)
# 图表输出到本地
plt.savefig('loss_par.png')
