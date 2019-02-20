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
                  mainProject=False,
                  createTimeStamp=""):
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
                      createTimeStamp=createTimeStamp)
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
        # return "wrong"
        pass
    db.session.commit()
    return projectId


def updateProject(projectId=None,
                  projectName=None,
                  creatorOpenid=None,
                  workersOpenid=None,
                  workersNumber=None,
                  projectStatus=None,
                  mainProject=None,
                  createTimeStamp=None):
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
    if mainProject is False or mainProject is True:
        p.mainProject = mainProject
    if createTimeStamp:
        p.createTimeStamp = createTimeStamp
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
        'createTimeStamp': p.createTimeStamp
    }
    print("getProject", d)
    return d


def getMainProject():
    plist = Project.query.filter_by(mainProject=True).all()
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
        'createTimeStamp': p.createTimeStamp
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
            'createTimeStamp': p.createTimeStamp
        }
        u = User.query.filter_by(openid=p.creatorOpenid).first()
        tempD.update({'creatorNickName': u.nickName})
        pDictArray.append(tempD.copy())
    print("查询到的plist", pDictArray)
    return pDictArray


def deleteProject(projectId):
    plist = Project.query.filter_by(id=projectId).all()
    if len(plist) != 1:
        return "projectId wrong"
    p = plist[0]
    db.session.delete(p)
    db.session.commit()
    return "delete success"