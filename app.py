from flask import Flask, request, jsonify
from flask_cors import CORS

from checkTools import ciede2000, rgb_to_xyz, hex_to_rgb, calculate_sum_pairs, generate_colors
import random
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/check', methods=['POST'])
def post_example():
    # 检查请求是否为POST方法
    if request.method == 'POST':
        # 从请求中获取JSON数据
        data = request.get_json()
        print(data)

        # 检查数据是否存在
        if data is None:
            return jsonify({'error': 'No JSON data received'})

        # 从JSON数据中获取特定字段
        # rgb_list=[]
        # hex_list = data.get('color_list')
        #
        # for hex in hex_list:
        #     rgb_list.append(hex_to_rgb(hex))
        #
        # print(rgb_list)
        #
        # result_pairs = calculate_sum_pairs(rgb_list)
        # for pair, pair_sum in result_pairs:
        #     print(f"{pair[0]} + {pair[1]} = {pair_sum}")


        # 在这里可以执行任何处理POST请求数据的逻辑
        # 例如，可以将数据存储到数据库或进行其他操作

        # 返回一个JSON响应
        # response = {
        #     'ChU': result_pairs,
        #     'CIE': result_pairs
        # }
        temp_results = []
        colors = generate_colors(data["colorCount"], 0.04, 0.9, 0, 1)
        for color in colors:

            r, g, b = color

            # 将RGB颜色值转换为十六进制字符串
            hex_color = convert_rgb_to_hex(r, g, b)

            temp_results.append(hex_color)
        print(temp_results)

        # 返回选择的颜色
        return jsonify({'color': temp_results})
        # return jsonify(response)

@app.route('/recommend', methods=['POST'])
def recommend():
    # 检查请求是否为POST方法
    if request.method == 'POST':
        # 从请求中获取JSON数据
        data = request.get_json()
        print(data)
        # 检查数据是否存在
        if data is None:
            return jsonify({'error': 'No JSON data received'})

        temp_results = []
        for i in range(0,10):
            random_colors = [random.randint(0, 255) for _ in range(3)]
            r,g,b = random_colors

            # 将RGB颜色值转换为十六进制字符串
            hex_color = convert_rgb_to_hex(r,g,b)

            temp_results.append(hex_color)
        print(temp_results)

        # 返回选择的颜色
        return jsonify({'color': temp_results})


def convert_rgb_to_hex(r, g, b):
    hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    return hex_color



if __name__ == '__main__':
    app.run(debug=True)
