from flask import Blueprint
from flask import request
import os
import shutil
import json

blue = Blueprint('first', __name__)


baseDir = os.getcwd()
# all images dir
projectImgsDir = os.path.join(baseDir, 'projectImgs')

@blue.route('/')
def index():
    return 'Hello,world!'


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
    projectId = controller.insertProject(projectName=projectName,
                            creatorOpenid=creatorOpenid,
                            workersOpenid="",
                            workersNumber=0,
                            projectStatus="",
                            mainProject=False)
    projectId = str(projectId).zfill(6)
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
        'mainProject': None
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
                                         mainProject=attrs['mainProject'])
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
    print(data)
    boundary = data.split(b'\r\n')[0]
    form_list = data.split(boundary)
    print(form_list)
    projectId = str(form_list[1].split(b'\r\n')[-2], encoding='utf-8')
    img_part = form_list[2].split(b'\r\n')
    print(img_part[-2])
    print(img_part[-1])
    img_content = img_part[-2] + b'\r\n' + img_part[-1]
    print(img_content)
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


