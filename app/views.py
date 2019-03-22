# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import send_from_directory
import os
import shutil
import json

blue = Blueprint('first', __name__)


baseDir = os.getcwd()
# all images dir
projectImgsDir = os.path.join(baseDir, 'projectImgs')

@blue.route('/')
def index():
    return 'new Hello,world!'


@blue.route('/insertUser', methods=['POST'])
def insertUser():
    openid = request.form['openid']
    avatarUrl = request.form['avatarUrl']
    nickName = request.form['nickName']
    userIdentity = request.form['userIdentity']
    ownedProjects = ""
    participatedProjects = ""
    from db_control import controller
    return controller.insertUser(openid=openid,
                                 userIdentity=userIdentity,
                                 avatarUrl=avatarUrl,
                                 nickName=nickName,
                                 ownedProjects=ownedProjects,
                                 participatedProjects=participatedProjects)


@blue.route('/updateUser', methods=['POST'])
def updateUser():
    attrs = {
        'avatarUrl': None,
        'userIdentity': None,
        'nickName': None,
        'ownedProjects': None,
        'participatedProjects': None
    }
    openid = request.form['openid']
    print("when updating user, openid = ", openid)
    for (key, value) in attrs.items():
        if key in request.form:
            attrs[key] = request.form[key]

    from db_control import controller
    return controller.updateUser(openid=openid,
                                 userIdentity=attrs['userIdentity'],
                                 avatarUrl=attrs['avatarUrl'],
                                 nickName=attrs['nickName'],
                                 ownedProjects=attrs['ownedProjects'],
                                 participatedProjects=attrs['participatedProjects'])


@blue.route('/queryUser', methods=['POST'])
def queryUser():
    from db_control import controller
    openid = request.form['openid']
    print("when querying user, openid = ", openid)
    u = controller.queryUser(openid)
    json_dict = {
        'openid': u.openid,
        'nickName': u.nickName,
        'avatarUrl': u.avatarUrl,
        'ownedProjects': u.ownedProjects,
        'userIdentity': u.userIdentity,
        'participatedProjects': u.participatedProjects
    }
    print(json_dict)
    return json.dumps(json_dict)


@blue.route('/check_if_user_existed', methods=['POST'])
def check_if_user_existed():
    from db_control import controller
    openid = request.form['openid']
    return controller.check_if_user_existed(openid)


@blue.route('/newProject', methods=['POST'])
def newProject():
    from db_control import controller
    print(request.form)
    projectName = request.form['projectName']
    creatorOpenid = request.form['creatorOpenid']
    createTimeStamp = request.form['createTimeStamp']
    mainProject = request.form['mainProject']
    if mainProject == "true":
        mainProject = 1
    else:
        mainProject = 0
    projectId = controller.insertProject(projectName=projectName,
                                         creatorOpenid=creatorOpenid,
                                         workersOpenid="",
                                         workersNumber=0,
                                         projectStatus=u"方案设计阶段",
                                         mainProject=mainProject,
                                         createTimeStamp=createTimeStamp)
    projectImgDir = os.path.join(projectImgsDir, projectId)
    # if we have got the directory already, delete it and remake one
    if projectId in os.listdir(projectImgsDir):
        shutil.rmtree(projectImgDir)
    os.mkdir(projectImgDir)
    return projectId


@blue.route('/updateProject', methods=['POST'])
def updateProject():
    from db_control import controller
    print(request.form)
    # None means do not update
    projectId = request.form['projectId']
    attrs = {
        'projectName': None,
        'creatorOpenid': None,
        'workersOpenid': None,
        'workersNumber': None,
        'projectStatus': None,
        'mainProject': None,
        'createTimeStamp': None,
        'updateImg': None,
    }
    for (key, value) in attrs.items():
        if key in request.form:
            attrs[key] = request.form[key]

    projectId = controller.updateProject(projectId=projectId,
                                         projectName=attrs['projectName'],
                                         creatorOpenid=attrs['creatorOpenid'],
                                         workersOpenid=attrs['workersOpenid'],
                                         workersNumber=attrs['workersNumber'],
                                         projectStatus=attrs['projectStatus'],
                                         mainProject=attrs['mainProject'],
                                         createTimeStamp=attrs['createTimeStamp'])
    if attrs['updateImg']:
        projectId = str(projectId).zfill(6)
        projectImgDir = os.path.join(projectImgsDir, projectId)
        # if we have got the directory already, delete it and remake one
        if projectId in os.listdir(projectImgsDir):
            shutil.rmtree(projectImgDir)
        os.mkdir(projectImgDir)
    return projectId


@blue.route('/uploadImg', methods=['POST'])
def uploadImg():
    from db_control import controller
    data = request.get_data()
    print("!!!!!!!!!!!!!!!!!!ORIGINAL DATA")
    print(str(data))
    boundary = data.split(b'\r\n')[0]
    print("BOUNDARY IS ====>", boundary)
    form_list = data.split(boundary)
    print("BOUNDARY SPLIT DATA, RESULT ====>", form_list)
    projectId = str(form_list[1].split(b'\r\n')[-2])
    print("projectId ====>", projectId)
    img_part = form_list[2].split(b'\r\n')
    print("FIRST PART OF IMG ====>",img_part[-3])
    print("SECOND PART OF IMG ====>", img_part[-2])
    img_content = img_part[-3] + b'\r\n' + img_part[-2]
    print("ALL OF IMG ====>", img_content)
    projectImgDir = os.path.join(projectImgsDir, projectId, projectId + '.png')
    with open(projectImgDir, 'wb') as f:
        f.write(img_content)
    return 'save success'


@blue.route('/project/query_if_mine_or_participated', methods=['POST'])
def query_if_mine_or_participated():
    from db_control import controller
    openid = request.form['openid']
    projectId = request.form['projectId']
    result = controller.query_if_mine_or_participated(openid, projectId)
    return result


@blue.route('/joinProject', methods=['POST'])
def joinProject():
    from db_control import controller
    openid = request.form['openid']
    projectId = request.form['projectId']
    result = controller.joinProject(openid, projectId)
    return result


@blue.route('/project/getMainProject')
def getMainProject():
    from db_control import controller
    return json.dumps(controller.getMainProject())


@blue.route('/project/getProject', methods=['POST'])
def getProject():
    from db_control import controller
    projectId = request.form['projectId']
    return json.dumps(controller.getProject(projectId))


@blue.route('/downloadImg/<projectId>', methods=['GET'])
def downloadImg(projectId):
    projectImgDir = os.path.join(projectImgsDir, projectId)
    filename = projectId + '.png'
    return send_from_directory(projectImgDir, filename, as_attachment=True)


@blue.route('/project/query_batch_projects', methods=['POST'])
def query_batch_projects():
    from db_control import controller
    print(request.form)
    order_by = request.form['order_by']
    start = int(request.form['start'])
    end = int(request.form['end'])
    result_dict = controller.query_batch_projects(order_by=order_by,
                                    start=start,
                                    end=end)
    return json.dumps(result_dict)


@blue.route('/project/deleteProject', methods=['POST'])
def deleteProject():
    from db_control import controller
    print(request.form)
    projectId = request.form['projectId']
    return controller.deleteProject(projectId)
