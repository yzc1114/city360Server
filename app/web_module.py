# -*- coding: utf-8 -*-
from flask import Blueprint
import json
from flask import request
import os
# import Levenshtein

web = Blueprint('city_web_blue', __name__, url_prefix='/city360_web', 
    static_folder='../city360', static_url_path="")

@web.route("/")
def hello():
    return web.send_static_file('index.html')

@web.route('/childpage/check.php', methods=['POST'])
def check_pic():
    res = {}
    A = request.form['A']
    B = request.form['B']
    C = request.form['C']
    D = request.form['D']
    E = request.form['E']
    F = request.form['F']
    G = request.form['G']
    H = request.form['H']
    requirement_str = 'A'+A+'B'+B+'C'+C+'D'+D+'E'+E+F+'G'+G+'H'+H
    requirement_str = requirement_str.encode('utf-8')
    print(requirement_str)
    if (A == "" or B == "" or C == "" or D == "" or E == "" or F == ""or G == "" or H == ""):
        res['code'] = 1
        res['msg'] = "参数不完整"
        return json.dumps(res)
    else:
        pic_list = list(map(lambda x: x.split('.')[0], 
            os.listdir(os.getcwd() + '/pic')))
        print(pic_list)
        for i in range(len(pic_list)):
            pic_list[i] = pic_list[i].encode('utf-8')

        # distance_list = list(zip(pic_list, list(map(lambda x:
        #     Levenshtein.distance(requirement_str, x), pic_list))))

        # sorted_distance = sorted(distance_list, key = lambda x: x[1])

        # chosen_pic = [{'pic': sorted_distance[0][0]},
        #     {'pic': sorted_distance[1][0]}]
        # res['code'] = 1
        # res['pic'] = chosen_pic
        # print(json.dumps(res))
        # return json.dumps(res)

