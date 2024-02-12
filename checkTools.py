import math
import random
# 将RGB值转换为XYZ颜色空间的函数
def rgb_to_xyz(rgb):
   # 将RGB值正规化为0到1之间的范围
   r, g, b = [x / 255.0 for x in rgb]
   # 对RGB值进行非线性校正
   r = pivot_rgb_to_xyz(r)
   g = pivot_rgb_to_xyz(g)
   b = pivot_rgb_to_xyz(b)
   # 使用转换矩阵将RGB颜色转换为CIE 1931 XYZ颜色
   x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
   y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
   z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
   return x, y, z

# RGB值非线性校正的辅助函数
def pivot_rgb_to_xyz(value):
   # 如果RGB值小于或等于0.04045，使用线性校正
   if value <= 0.04045:
       value = value / 12.92
   else:
       # 如果RGB值大于0.04045，使用幂次方校正
       value = ((value + 0.055) / 1.055) ** 2.4
   return value

# 计算CIEDE2000色差和和谐度的函数
def ciede2000(L1, a1, b1, L2, a2, b2,K_l=1,K_c=1):
    # 参数设置
    kL = 1
    kC = 1
    kH = 1

    # 彩度计算
    def cai_du(a, b):

        return math.sqrt(a * a + b * b)

    # 色调角计算
    def se_diao_jiao(a, b):
        h = math.atan2(b, a) * 180 / math.pi
        if a > 0 and b >= 0:
            return h
        elif a < 0:
            return h + 180
        else:
            return h + 360
    # 计算和谐度
    def harmon(L1, a1, b1, L2, a2, b2,K_c):
        G = 0.5 * (1 - (cai_du(a1, b1) ** 7) / (cai_du(a1, b1) ** 7 + 25 ** 7) ** 0.5)*K_c
        LL1 = L1
        aa1 = a1 * (1 + G)
        bb1 = b1
        LL2 = L2
        aa2 = a2 * (1 + G)
        bb2 = b2
        return (-0.7 * math.tanh(-0.7 + 0.04 * abs(bb2 - bb1))
                - 0.3 * math.tanh(-1.1 + 0.05 * abs(aa2 - aa1))
                + 0.4 * math.tanh(-1.1 + 0.05 * abs(LL2 - LL1))
                + 0.3 + 0.6 * math.tanh(-4.2 + 0.028 * (aa1 + aa2)))
    mean_LL = (L1 + L2) / 2
    mean_CC = (cai_du(a1, b1) + cai_du(a2, b2)) / 2
    mean_hh = (se_diao_jiao(a1, b1) + se_diao_jiao(a2, b2)) / 2
    SL = 1 + 0.015 * (mean_LL - 50) ** 2 / math.sqrt(20 + (mean_LL - 50) ** 2)
    SC = 1 + 0.045 * mean_CC
    T = 1 - 0.17 * math.cos((mean_hh - 30) * math.pi / 180) + 0.24 * math.cos((2 * mean_hh) * math.pi / 180) + \
        0.32 * math.cos((3 * mean_hh + 6) * math.pi / 180) - 0.2 * math.cos((4 * mean_hh - 63) * math.pi / 180)
    SH = 1 + 0.015 * mean_CC * T
    delta_LL = L2 - L1
    delta_CC = cai_du(a2, b2) - cai_du(a1, b1)
    delta_hh = se_diao_jiao(a2, b2) - se_diao_jiao(a1, b1)
    delta_HH = 2 * math.sin(math.pi * delta_hh / 360) * (cai_du(a1, b1) * cai_du(a2, b2)) ** 0.5
    L_item = delta_LL / ((kL * SL)*K_l)
    C_item = delta_CC / ((kC * SC)*K_l)
    H_item = delta_HH / ((kH * SH)*K_l)
    E00 = math.sqrt(L_item ** 2 + C_item ** 2 + H_item ** 2)
    harmon_score = harmon(L1, a1, b1, L2, a2, b2,K_c)
    return E00,harmon_score

def hex_to_rgb(hex_color):
    # 去除十六进制颜色代码中的'#'字符（如果存在）
    hex_color = hex_color.lstrip('#')
    # 将十六进制颜色代码转换为RGB值
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)

def calculate_sum_pairs(colors):
    # 创建一个集合来跟踪已经计算过的组合
    computed_pairs = set()
    # 存储结果的列表
    results = []
    # 遍历列表中的每一对数
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):
            # 组合两个颜色并计算 cie 以及chu
            if colors[i]==colors[j]:
                continue
            pair = (colors[i], colors[j])
            pair_color = calcu2color(colors[i], colors[j])

            # 检查是否已经计算过这个组合，如果没有，添加到结果列表中并标记为已计算
            if pair not in computed_pairs and pair[::-1] not in computed_pairs:
                results.append((pair, pair_color))
                computed_pairs.add(pair)
    return results

def calcu2color(color1,color2):

    xyz_color = rgb_to_xyz(color1)
    xyz_color2 = rgb_to_xyz(color2)
    L1, a1, b1 = xyz_color
    L2, a2, b2 = xyz_color2
    E00_score, harmon_score = ciede2000(L1, a1, b1, L2, a2, b2)
    print(color1,color2," CIEDE2000色差:", E00_score)
    print(color1,color2," ChU和谐度:", harmon_score)
    return E00_score,harmon_score
# Press the green button in the gutter to run the script.

def generate_colors(n, min_harmony, max_harmony, min_diff, max_diff):
    colors = []

    while len(colors) < n:
        if not colors:  # 如果是第一个颜色，直接添加
            colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        else:
            new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            valid_color = True
            for color in colors:
                diff, harmony = calcu2color(color, new_color)
                if not (min_harmony <= harmony <= max_harmony and min_diff <= diff <= max_diff):
                    valid_color = False
                    break

            if valid_color:
                colors.append(new_color)

    return colors

if __name__ == '__main__':


    # numbers = [(101, 178, 243), (101, 178, 242), (254, 254, 127), (126, 1, 1)]
    # result_pairs = calculate_sum_pairs(numbers)
    # for pair, pair_sum in result_pairs:
    #     print(f"{pair[0]} + {pair[1]} = {pair_sum}")

    """
    rgb_to_xyz 函数：将RGB颜色值转换为CIE 1931 XYZ颜色值。该函数首先对输入的RGB值进行归一化处理，然后使用非线性校正函数 pivot_rgb_to_xyz 对每个颜色通道进行校正，最后使用线性转换矩阵将RGB颜色转换为XYZ颜色。
    pivot_rgb_to_xyz 函数：对RGB值进行非线性校正的辅助函数。该函数根据输入的RGB值大小选择不同的校正方法：当RGB值小于或等于0.04045时，使用线性校正；当RGB值大于0.04045时，使用幂次方校正。
    ciede2000 函数：计算两个颜色之间的CIEDE2000色差和和谐度。该函数首先定义了三个参数 kL、kC 和 kH，然后定义了计算彩度、色调角和谐度的辅助函数。接下来，计算两个颜色的平均亮度、平均彩度、平均色调角，以及对应的色调角差、彩度差和亮度差。最后，将这些差值代入公式计算CIEDE2000色差和谐度。
    hex_to_rgb 函数：将十六进制颜色代码转换为RGB值。该函数首先去除十六进制颜色代码中的 '#' 字符（如果存在），然后将十六进制颜色代码转换为RGB值。
    calculate_sum_pairs 函数：计算颜色列表中所有颜色对的色差和谐度。该函数首先创建一个集合来跟踪已经计算过的组合，然后遍历列表中的每一对颜色，计算它们的色差和谐度。如果这个组合还没有计算过，就将结果添加到结果列表中，并将这个组合添加到已计算集合中。
    calcu2color 函数：计算两个颜色的CIEDE2000色差和谐度。该函数首先将两个RGB颜色转换为XYZ颜色，然后将XYZ颜色转换为Lab颜色，最后调用 ciede2000 函数计算色差和谐度。
    """

    colors = generate_colors(10, 0.08, 0.9, 0.3, 0.4
                             )

    for color in colors:
        print(color)

