# -*- coding: utf-8 -*-
from manage import User
from manage import Project
from manage import db


def insertUser(openid,
               userIdentity,
               avatarUrl,
               nickName,
               ownedProjects,
               participatedProjects):
    """
    :return: user id
    """
    u = User(openid=openid,
             userIdentity=userIdentity,
             avatarUrl=avatarUrl,
             nickName=nickName,
             ownedProjects=ownedProjects,
             participatedProjects=participatedProjects)
    db.session.add(u)
    db.session.flush()
    db.session.commit()
    return openid


def updateUser(openid,
               userIdentity,
               avatarUrl,
               nickName,
               ownedProjects,
               participatedProjects):
    """
    :param openid: col
    :param avatarUrl: col
    :param nickName: col
    :param ownedProjects: col
    :param participatedProjects: col
    :return: openid
    """
    ls = User.query.filter_by(openid=openid).all()
    print(ls)
    if len(ls) != 1:
        return "wrong"
    u = ls[0]
    if avatarUrl:
        u.avatarUrl = avatarUrl
    if userIdentity:
        u.userIdentity = userIdentity
    if nickName:
        u.nickName = nickName
    if ownedProjects:
        u.ownedProjects = ownedProjects
    if participatedProjects:
        u.participatedProjects = participatedProjects
    db.session.add(u)
    db.session.commit()
    return openid


def queryUser(openid=None):
    """
    :param openid: query openid
    :return: instance of User
    """
    if not openid:
        return None
    else:
        return User.query.filter_by(openid=openid).first()


def check_if_user_existed(openid=None):
    if not openid:
        return False
    else:
        return len(User.query.filter_by(openid=openid).all()) == 1


def insertProject(projectName="",
                  creatorOpenid="",
                  workersOpenid="",
                  workersNumber=0,
                  projectStatus="",
<<<<<<< HEAD
                  mainProject=False,
                  createTimeStamp="",
                  imageFileName=""):
=======
                  mainProject=0,
                  createTimeStamp=""):
>>>>>>> 71453a33b7f813ee4e55977059a8ba944527c4cf
    """
    :parameter imagesPath: stores all paths of the project's images
    :return: projectId
    """
    project = Project(projectName=projectName,
                      creatorOpenid=creatorOpenid,
                      workersOpenid=workersOpenid,
                      workersNumber=workersNumber,
                      projectStatus=projectStatus,
                      mainProject=mainProject,
                      createTimeStamp=createTimeStamp,
                      imageFileName=imageFileName)
    db.session.add(project)
    db.session.flush()
    projectId = project.id
    projectId = str(projectId).zfill(6)
    ulist = User.query.filter_by(openid=creatorOpenid).all()
    if len(ulist) == 1:
        u = ulist[0]
        u.ownedProjects += (projectId + ",")
        db.session.add(u)
    else:
        # in case with test, we pass
        return "wrong"
        
    db.session.commit()
    return projectId


def updateProject(projectId=None,
                  projectName=None,
                  creatorOpenid=None,
                  workersOpenid=None,
                  workersNumber=None,
                  projectStatus=None,
                  mainProject=None,
                  createTimeStamp=None,
                  imageFileName=None):
    """
    :param projectId: primary key
    :param projectName: col
    :param creatorOpenid: col
    :param workersOpenid: col
    :param workersNumber: col
    :param projectStatus: col
    :param mainProject: col
    :return: projectId
    """
    if not projectId:
        return "projectId None"
    projectId_int = int(projectId)
    p = Project.query.filter_by(id=projectId_int).first()
    if projectName:
        p.projectName = projectName
    if creatorOpenid:
        p.creatorOpenid = creatorOpenid
    if workersOpenid:
        p.workersOpenid = workersOpenid
    if projectStatus:
        p.projectStatus = projectStatus
    if workersNumber:
        p.workersNumber = workersNumber
    if mainProject is not None:
        p.mainProject = mainProject
    if createTimeStamp:
        p.createTimeStamp = createTimeStamp
    if imageFileName:
        p.imageFileName = imageFileName
    db.session.add(p)
    db.session.commit()
    return projectId


def query_if_mine_or_participated(openid, projectId):
    if not projectId:
        return "projectId None"
    projectId_int = int(projectId)
    print(projectId)
    plist = Project.query.filter_by(id=projectId_int).all()
    if len(plist) != 1:
        return "wrong"
    p = plist[0]
    if p.creatorOpenid == openid:
        return "creator"
    elif openid in p.workersOpenid.split(','):
        return "worker"
    else:
        return "no one"


def joinProject(openid, projectId):
    if not projectId or not openid:
        return "id None"
    projectId_int = int(projectId)
    print("projectId", projectId)
    print("openid", openid)
    plist = Project.query.filter_by(id=projectId_int).all()
    if len(plist) != 1:
        return "projectId wrong"
    ulist = User.query.filter_by(openid=openid).all()
    if len(ulist) != 1:
        return "user openid wrong"
    p = plist[0]
    p.workersOpenid += (openid + ",")
    p.workersNumber += 1
    u = ulist[0]
    u.participatedProjects += (projectId + ",")
    db.session.add(p)
    db.session.add(u)
    db.session.commit()
    return "success"


def getProject(projectId):
    projectId_int = int(projectId)
    p = Project.query.filter_by(id=projectId_int).first()
    d = {
        'projectId': projectId,
        'projectName': p.projectName,
        'creatorOpenid': p.creatorOpenid,
        'workersOpenid': p.workersOpenid,
        'workersNumber': p.workersNumber,
        'projectStatus': p.projectStatus,
        'mainProject': p.mainProject,
        'createTimeStamp': p.createTimeStamp,
        'imageFileName': p.imageFileName
    }
    print("getProject", d)
    return d


def getMainProject():
    plist = Project.query.filter_by(mainProject=1).all()
    if len(plist) == 0:
        return "no main project"
    p = plist[0]
    d = {
        'projectId': str(p.id).zfill(6),
        'projectName': p.projectName,
        'creatorOpenid': p.creatorOpenid,
        'workersOpenid': p.workersOpenid,
        'workersNumber': p.workersNumber,
        'projectStatus': p.projectStatus,
        'mainProject': p.mainProject,
        'createTimeStamp': p.createTimeStamp,
        'imageFileName': p.imageFileName
    }
    u = User.query.filter_by(openid=p.creatorOpenid).first()
    d.update({'creatorNickName': u.nickName})
    print("getMainProject", d)
    return d


def query_batch_projects(order_by, start, end):
    print("start", start)
    print("end", end)
    if(order_by == "createTimeStamp"):
        plist = Project.query.order_by(Project.createTimeStamp.desc()).all()[start: end]
    else:
        return "no such order_by standard"
    pDictArray = []
    for p in plist:
        tempD = {
            'projectId': str(p.id).zfill(6),
            'projectName': p.projectName,
            'creatorOpenid': p.creatorOpenid,
            'workersOpenid': p.workersOpenid,
            'workersNumber': p.workersNumber,
            'projectStatus': p.projectStatus,
            'mainProject': p.mainProject,
            'createTimeStamp': p.createTimeStamp,
            'imageFileName': p.imageFileName
        }
        u = User.query.filter_by(openid=p.creatorOpenid).first()
        tempD.update({'creatorNickName': u.nickName})
        pDictArray.append(tempD.copy())
    print("plist", pDictArray)
    return pDictArray


def deleteProject(projectId, openid):
    """
    :param projectId: the projectId to be deleted
    :param openid: the projectId's owner openid
    :return: result success or not
    """
    plist = Project.query.filter_by(id=projectId).all()
    ulist = User.query.filter_by(openid=openid).all()
    print(projectId, openid)
    print(plist, ulist)
    if len(plist) != 1 or len(ulist) != 1:
        return "something wrong"
    p = plist[0]
    u = ulist[0]
    ownedProjectsStr = u.ownedProjects
    ownedProjectsStr = removeSubproject(ownedProjectsStr, projectId)
    if ownedProjectsStr:
        u.ownedProjects = ownedProjectsStr
    else:
        return "something wrong deletingProject"
    db.session.add(u)
    db.session.delete(p)
    db.session.commit()
    return "delete success"


def removeSubproject(projectIds, projectId):
    if projectIds.find(projectId) == -1:
        return None
    splited = projectIds.split(projectId)
    if len(splited) != 2:
        return None
    if splited[0] == '' and splited[1] == '':
        projectIds = ""
    elif splited[0] == '' and splited[1] != '':
        projectIds = splited[1][1:]
    elif splited[1] == '' and splited[0] != '':
        projectIds = splited[0][:-1]
    elif splited[0] != '' and splited[0] != '':
        projectIds = splited[0][:-1] + splited[1]
    else:
        return None
    return projectIds


def exitProject(openid, projectId):
    """
    :param openid: participator
    :param projectId: project to be exited
    :return: result success or not
    """
    plist = Project.query.filter_by(id=projectId).all()
    ulist = User.query.filter_by(openid=openid).all()
    print(projectId, openid)
    print(plist, ulist)
    if len(plist) != 1 or len(ulist) != 1:
        return "something wrong"
    p = plist[0]
    u = ulist[0]
    participatedProjectsStr = u.participatedProjects
    participatedProjectsStr = removeSubproject(participatedProjectsStr, projectId)
    if participatedProjectsStr:
        u.participatedProjects = participatedProjectsStr
    else:
        return "something wrong exitingProject"
    db.session.add(u)
    db.session.delete(p)
    db.session.commit()
<<<<<<< HEAD
    return "exit success"
=======
    return "delete success"
>>>>>>> 71453a33b7f813ee4e55977059a8ba944527c4cf
