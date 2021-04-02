import matplotlib.pyplot as plt
import matplotlib 
import numpy as np
from matplotlib import rc
import seaborn as sns
from ast import literal_eval

# font_path = r'Users/kim-yerim/Downloads/NanumGothic_OTF'
# fontprop = fm.FontProperties(fname=font_path, size=18)
# matplotlib.rcParams['axes.unicode_minus'] = False 
# matplotlib.rcParams['font.family'] = "AppleGothic"

def start(value0, value1, value2, name, contribution, standard):

    ratio = [30, 30, 40]
    labels = ['참여성', '창의성', '기타']
    colors = ['#ff9999', '#ffc000', '#8fd9b6']
    wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
    list_value0_key = list(literal_eval(value0).keys())
    list_value0_value = list(literal_eval(value0).values())

    x = np.arange(len(list_value0_key))
    member = list_value0_key


    def createValue0():
        plt.rc('font', family='AppleGothic') 
        plt.rcParams['font.family']
        plt.cla()
        plt.bar(x, list_value0_value, width=0.4, align='center', color="red",
                linewidth=3, tick_label=member)
        plt.xlabel('참여성', fontsize=15)
        plt.ylabel('(%)', fontsize=15)
        plt.xticks(x, member)
        # plt.show()
        plt.savefig(f"static/{name}_value0.jpg")

    def createValue1():
        plt.rc('font', family='AppleGothic') 
        plt.rcParams['font.family']
        plt.cla()
        list_value1_value = list(literal_eval(value1).values())
        plt.bar(x, list_value1_value, width=0.4, align='center', color="blue",
                linewidth=3, tick_label=member)
        plt.xlabel('창의성', fontsize=15)
        plt.ylabel('(%)', fontsize=15)
        plt.xticks(x, member)
        # plt.show()
        plt.savefig(f"static/{name}_value1.jpg")

    def createValue2():
        plt.rc('font', family='AppleGothic') 
        plt.rcParams['font.family']
        plt.cla()
        list_value_name_value = list(literal_eval(value2).values())
        plt.bar(x, list_value_name_value, width=0.4, align='center', color="green",
                linewidth=3, tick_label=member)
        plt.ylabel('(%)', fontsize=15)
        plt.xlabel('기타', fontsize=15)
        plt.xticks(x, member)
        # plt.show()
        plt.savefig(f"static/{name}_value2.jpg")

    def createCont():
        plt.rc('font', family='AppleGothic') 
        plt.rcParams['font.family']
        plt.cla()
        temp = ['1','2','3']
        temp2 = [0, contribution, 0]
        plt.bar(temp, temp2, width=0.4, align='center', color="c")
        plt.axhline(y=standard, color='r', linewidth=1)
        plt.ylabel('(%)', fontsize=15)
        plt.xticks(name)
        plt.savefig(f"static/{name}_contribution.jpg")

    createValue0()
    createValue1()
    createValue2()
    createCont()
    
# def createPie(name):
#     plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False, colors=colors, wedgeprops=wedgeprops)
#     # plt.show()
#     plt.savefig(f"media/{name}_pie.jpg")
