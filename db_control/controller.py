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
                  mainProject=False):
    """
    :parameter imagesPath: stores all paths of the project's images
    :return: projectId
    """
    project = Project(projectName,
                      creatorOpenid,
                      workersOpenid,
                      workersNumber,
                      projectStatus,
                      mainProject)
    db.session.add(project)
    db.session.flush()
    projectId = project.id
    db.session.commit()
    return projectId


def updateProject(projectId=None,
                  projectName=None,
                  creatorOpenid=None,
                  workersOpenid=None,
                  workersNumber=None,
                  projectStatus=None,
                  mainProject=None):
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
    db.session.add(p)
    db.session.commit()
    return projectId


def query_if_mine_or_participated(openid, projectId):
    if not projectId:
        return "projectId None"
    projectId_int = int(projectId)
    print(projectId)
    p = Project.query.filter_by(id=projectId_int).first()
    if p.creatorOpenid == openid:
        return "mine"
    elif openid in p.workersOpenid.split(','):
        return "worker"
    else:
        return "no one"


