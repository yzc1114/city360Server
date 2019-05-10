# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import send_from_directory
import os
import shutil
import json
import Levenshtein

blue = Blueprint('first', __name__, static_folder='../', static_url_path="")


baseDir = os.getcwd()
# all images dir
projectImgsDir = os.path.join(baseDir, 'projectImgs')
# pic dir
picDir = os.path.join(baseDir, 'pic')


@blue.route('/')
def index():
    return 'new Hello,world!'


@blue.route('/insertUser', methods=['POST'])
def insertUser():
    openid = request.form['openid']
    avatarUrl = request.form['avatarUrl']
    nickName = request.form['nickName']
    userIdentity = request.form['userIdentity']
    from db_control import controller
    print(request.form)
    return controller.insertUser(openid=openid,
                                 userIdentity=userIdentity,
                                 avatarUrl=avatarUrl,
                                 nickName=nickName)


@blue.route('/updateUser', methods=['POST'])
def updateUser():
    attrs = {
        'avatarUrl': None,
        'userIdentity': None,
        'nickName': None,
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
                                 nickName=attrs['nickName'])


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
        'userIdentity': u.userIdentity
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
    mainProject = False if 'false' == mainProject else True
    projectCity = request.form['projectCity']
    projectStreetBlock = request.form['projectStreetBlock']
    projectId = controller.insertProject(projectName=projectName,
                                         creatorOpenid=creatorOpenid,
                                         projectStatus=u"方案设计阶段",
                                         mainProject=mainProject,
                                         projectCity=projectCity,
                                         projectStreetBlock=projectStreetBlock,
                                         createTimeStamp=createTimeStamp)
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
        'projectStatus': None,
        'mainProject': None,
        'createTimeStamp': None
    }
    for (key, value) in attrs.items():
        if key in request.form:
            attrs[key] = request.form[key]

    projectId = controller.updateProject(projectId=projectId,
                                         projectName=attrs['projectName'],
                                         creatorOpenid=attrs['creatorOpenid'],
                                         projectStatus=attrs['projectStatus'],
                                         mainProject=attrs['mainProject'],
                                         createTimeStamp=attrs['createTimeStamp'])
    # if attrs['updateImg']:
    #     projectId = str(projectId).zfill(6)
    #     projectImgDir = os.path.join(projectImgsDir, projectId)
    #     # if we have got the directory already, delete it and remake one
    #     if projectId in os.listdir(projectImgsDir):
    #         shutil.rmtree(projectImgDir)
    #     os.mkdir(projectImgDir)
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
    return json.dumps(controller.getProjectDict(projectId))


#@blue.route('/downloadImg/<imgFileName>')
#def downloadImg(imgFileName):
#    imageFileName = imgFileName
#    projectImgDir = os.path.join(picDir, imageFileName)
#    filename = imageFileName + '.jpg'
#    return send_from_directory(projectImgDir, filename, as_attachment=True)


#@blue.route('/downloadImg/<test>')
#def downloadImg(test):
#    imageFileName = test
#    filename = imageFileName + '.jpg'
#    print(filename)
#    print(picDir)
#    # return test
#    return send_from_directory(picDir, filename, as_attachment=True)



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
    openid = request.form['openid']
    return controller.deleteProject(projectId, openid)


@blue.route('/project/getPossibleImageFileNames', methods=['POST'])
def getPossibleImageFileNames():
    print(request.form)
    uploadedChoice = request.form['imageName']
    uploadedChoice = uploadedChoice.encode('utf-8')
    fileNames = None
    
    return getRealImage(uploadedChoice)
    # return getFakeImage(uploadedChoice)


def getRealImage(uploadedChoice):
    pic_list = list(map(lambda x: x.split('.')[0],
                        os.listdir(picDir)))
    print(pic_list)
    print("MYCHOICE ===== ", uploadedChoice)
    distance_list = list(zip(pic_list, list(map(lambda x:
                                                Levenshtein.distance(uploadedChoice, x), pic_list))))

    sorted_distance = sorted(distance_list, key=lambda x: x[1])

    chosen_pic = sorted_distance[0][0]
    return chosen_pic + ".jpg"


def getFakeImage(uploadedChoice):
    for root, dirs, files in os.walk(picDir):
       fileNames = files
    alphas = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
    if uploadedChoice in fileNames:
        return uploadedChoice
    else:
        for alpha in alphas:
            uploadedChoice = uploadedChoice.split(alpha)[0]
            for filename in fileNames:
               if filename.split(alpha)[0] == uploadedChoice:
                    return filename

@blue.route('/project/exitProject', methods=['POST'])
def exitProject():
    from db_control import controller
    openid = request.form['openid']
    projectId = request.form['projectId']
    return controller.exitProject(openid, projectId)


@blue.route('/project/vote', methods=['POST'])
def voteProject():
    from db_control import controller
    print(request.form)
    projectId = request.form['projectId']
    imageFileName = request.form['imageFileName']
    return controller.voteProject(projectId, imageFileName)


@blue.route('/project/pickImage', methods=['POST'])
def pickImage():
    from db_control import controller
    projectId = request.form['projectId']
    imageFileName = request.form['imageFileName']
    return controller.pickImage(projectId, imageFileName)


@blue.route('/project/queryVotes', methods=['POST'])
def queryVotes():
    from db_control import controller
    projectId = request.form['projectId']
    votesDict = controller.getVotesResult(projectId)
    return json.dumps(votesDict)


@blue.route('/project/addMessage', methods=['POST'])
def addMessage():
    from db_control import controller
    projectId = request.form['projectId']
    message_content = request.form['message_content']
    return controller.addMessage(projectId=projectId, message_content=message_content)


@blue.route('/project/queryProjectOwnsSchemes', methods=['POST'])
def queryProjectOwnsSchemes():
    from db_control import controller
    projectId = request.form['projectId']
    print(projectId)
    return json.dumps(controller.queryProjectOwnsSchemes(projectId))


@blue.route('/project/addScheme', methods=['POST'])
def addScheme():
    from db_control import controller
    projectId = request.form['projectId']
    imageFileName = request.form['imageFileName']
    return controller.addScheme(projectId=projectId, imageFileName=imageFileName)


@blue.route('/project/queryCandidateScheme', methods=['POST'])
def queryCandidateScheme():
    from db_control import controller
    projectId = request.form['projectId']
    return json.dumps(controller.queryCandidateScheme(projectId))


@blue.route('/project/queryUserOwnsProjects', methods=['POST'])
def queryUserOwnsProjects():
    from db_control import controller
    openid = request.form['openid']
    startFrom = int(request.form['startFrom'])
    limitation = int(request.form['limitation'])
    return json.dumps(controller.queryUserOwnsProjects(openid=openid, startFrom=startFrom, limitation=limitation))


@blue.route('/project/queryUserParticipatesProjects', methods=['POST'])
def queryUserParticipatesProjects():
    from db_control import controller
    openid = request.form['openid']
    startFrom = int(request.form['startFrom'])
    limitation = int(request.form['limitation'])
    return json.dumps(controller.queryUserParticipatesProjects(openid=openid, startFrom=startFrom, limitation=limitation))


@blue.route('/project/setCandidate', methods=['POST'])
def setCandidate():
    #set the highest votes as the candidate
    from db_control import controller
    projectId = request.form['projectId']
    return controller.addCandidate(projectId=projectId)

@blue.route('/project/queryWorkersAvatar', methods=['POST'])
def queryWorkersAvatar():
    from db_control import controller
    projectId = request.form['projectId']
    return json.dumps(controller.queryWorkersAvatar(projectId))
