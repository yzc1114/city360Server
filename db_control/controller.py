# -*- coding: utf-8 -*-
from manage import *
from manage import db


def getProject(projectId):
    assert projectId is not None
    projectId = int(projectId)
    plist = Project.query.filter_by(id=projectId).all()
    print(plist)
    if len(plist) != 1:
        return None
    return plist[0]

def getUser(openid):
    assert openid is not None
    ulist = User.query.filter_by(openid=openid).all()
    print(openid)
    if len(ulist) != 1:
        return None
    return ulist[0]


def insertUser(openid,
               userIdentity,
               avatarUrl,
               nickName):
    """
    :return: open id
    """
    u = User(openid=openid,
             userIdentity=userIdentity,
             avatarUrl=avatarUrl,
             nickName=nickName)
    print("inserting user", userIdentity)
    db.session.add(u)
    db.session.flush()
    db.session.commit()
    return openid


def updateUser(openid,
               userIdentity,
               avatarUrl,
               nickName):
    """
    :param openid: col
    :param avatarUrl: col
    :param nickName: col
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
                  projectStatus="",
                  mainProject=False,
                  createTimeStamp="",
                  projectCity="",
                  projectStreetBlock=""):
    """
    :return: projectId
    """
    project = Project(projectName=projectName,
                      creatorOpenid=creatorOpenid,
                      projectStatus=projectStatus,
                      mainProject=mainProject,
                      createTimeStamp=createTimeStamp,
                      projectCity=projectCity,
                      projectStreetBlock=projectStreetBlock)
    db.session.add(project)
    db.session.flush()
    projectId = project.id
    projectId = str(projectId).zfill(6)
    ulist = User.query.filter_by(openid=creatorOpenid).all()
    if len(ulist) == 1:
        u = ulist[0]
        # add User_Owns_Project
        u_o_p = User_Owns_Projects(user_id=u.id, project_id=projectId)
        db.session.add(u_o_p)
        db.session.flush()
    else:
        # in case with test, we pass
        return "wrong"
        
    db.session.commit()
    return projectId


def updateProject(projectId=None,
                  projectName=None,
                  creatorOpenid=None,
                  projectStatus=None,
                  mainProject=None,
                  createTimeStamp=None):
    """
    :param projectId: primary key
    :param projectName: col
    :param creatorOpenid: col
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
    if projectStatus:
        p.projectStatus = projectStatus
    if mainProject is not None:
        p.mainProject = mainProject
    if createTimeStamp:
        p.createTimeStamp = createTimeStamp
    db.session.add(p)
    db.session.commit()
    return projectId


def query_if_mine_or_participated(openid, projectId):
    u = getUser(openid=openid)
    p = getProject(projectId=projectId)
    if u is None or p is None:
        return "wrong"
    u_o_p_list = User_Owns_Projects.query.filter_by(user_id=u.id, project_id=p.id).all()
    if len(u_o_p_list) == 1:
        return "creator"
    u_i_p_list = User_In_Projects.query.filter_by(user_id=u.id, project_id=p.id).all()
    if len(u_i_p_list) == 1:
        return "worker"
    return "no one"


def joinProject(openid, projectId):
    u = getUser(openid=openid)
    p = getProject(projectId=projectId)
    if u is None or p is None:
        return "wrong"
    # add User_In_Projects
    u_i_p = User_In_Projects(user_id=u.id, project_id=p.id)
    p.workersCount += 1
    db.session.add(u_i_p)
    db.session.add(p)
    db.session.commit()
    return "success"


def getProjectDict(projectId):
    projectId_int = int(projectId)
    p = Project.query.filter_by(id=projectId_int).first()
    p_o_s_list = Project_Owns_Schemes.query.filter_by(project_id=projectId_int).all()
    imageFileName = None
    for p_o_s in p_o_s_list:
        if p_o_s.for_show:
            imageFileName = p_o_s.imageFileName
            break
    d = {
        'projectId': projectId,
        'projectName': p.projectName,
        'creatorOpenid': p.creatorOpenid,
        'projectStatus': p.projectStatus,
        'mainProject': p.mainProject,
        'createTimeStamp': p.createTimeStamp,
        'imageFileName': imageFileName if imageFileName else "no image",
        'workersCount': p.workersCount
    }
    u = getUser(p.creatorOpenid)
    d.update({'creatorNickName': u.nickName})
    print("getProject", d)
    return d


def getMainProject():
    plist = Project.query.filter_by(mainProject=1).all()
    if len(plist) == 0:
        return "no main project"
    p = plist[0]
    p_o_s_list = Project_Owns_Schemes.query.filter_by(project_id=p.id).all()
    imageFileName = None
    for p_o_s in p_o_s_list:
        if p_o_s.for_show:
            imageFileName = p_o_s.imageFileName
            break
    d = {
        'projectId': str(p.id).zfill(6),
        'projectName': p.projectName,
        'creatorOpenid': p.creatorOpenid,
        'projectStatus': p.projectStatus,
        'mainProject': p.mainProject,
        'createTimeStamp': p.createTimeStamp,
        'imageFileName': imageFileName if imageFileName else "no image",
        'workersCount': p.workersCount
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
        p_o_s_list = Project_Owns_Schemes.query.filter_by(project_id=p.id).all()
        imageFileName = None
        for p_o_s in p_o_s_list:
            if p_o_s.for_show:
                imageFileName = p_o_s.imageFileName
                break
        tempD = {
            'projectId': str(p.id).zfill(6),
            'projectName': p.projectName,
            'creatorOpenid': p.creatorOpenid,
            'projectStatus': p.projectStatus,
            'mainProject': p.mainProject,
            'createTimeStamp': p.createTimeStamp,
            'imageFileName': imageFileName if imageFileName else "no image",
            'workersCount': p.workersCount
        }
        u = User.query.filter_by(openid=p.creatorOpenid).first()
        tempD.update({'creatorNickName': u.nickName})
        pDictArray.append(tempD.copy())
    print("plist", pDictArray)
    return pDictArray


def deleteProject(projectId, openid):
    """
    this function is for project owners
    :param projectId: the projectId to be deleted
    :param openid: the projectId's owner openid
    :return: result success or not
    """
    u = getUser(openid=openid)
    p = getProject(projectId=projectId)
    if u is None or p is None:
        return "wrong"

    u_o_p_list = User_Owns_Projects.query.filter_by(user_id=u.id, project_id=p.id).all()
    if len(u_o_p_list) != 1:
        return "wrong"
    u_o_p = u_o_p_list[0]
    # delete u_o_p
    db.session.delete(u_o_p)
    db.session.delete(p)
    db.session.commit()
    return "delete success"


def exitProject(openid, projectId):
    """
    this function is for participators
    :param openid: participator
    :param projectId: project to be exited
    :return: result success or not
    """
    u = getUser(openid=openid)
    p = getProject(projectId=projectId)
    if u is None or p is None:
        return "wrong"
    u_i_p_list = User_In_Projects.query.filter_by(user_id=u.id, project_id=p.id).all()
    if len(u_i_p_list) != 1:
        return "wrong"
    u_i_p = u_i_p_list[0]
    p.workersCount -= 1
    db.session.delete(u_i_p)
    db.session.add(p)
    db.session.commit()
    return "exit success"


def pickImage(projectId, imageFileName):
    """
    :param projectId
    :param ImageFileName
    :return: result success or not
    """
    p = getProject(projectId)
    p_o_s = Project_Owns_Schemes(project_id=p.id, imageFileName=imageFileName, votes=0)
    db.session.add(p_o_s)
    db.session.flush()
    db.session.commit()
    return "success"


def voteProject(projectId, imageFileName):
    """
        :param projectId
        :param imageFileName
        :return: result success or not
        """
    p = getProject(projectId)
    print("voting ", p)
    if not p:
        return "wrong"
    p_o_s_list = Project_Owns_Schemes.query.filter_by(project_id=p.id, imageFileName=imageFileName).all()
    print(p_o_s_list)
    if len(p_o_s_list) != 1:
        return "wrong"
    p_o_s = p_o_s_list[0]
    p_o_s.votes += 1
    db.session.add(p_o_s)
    db.session.commit()
    return "success"


def getVotesResult(projectId):
    """
    this function return a dict for each vote result of one scheme
    :param projectId: str
    :return: dict
    """
    p = getProject(projectId)
    if not p:
        return "wrong"
    p_o_s_list = Project_Owns_Schemes.query.filter_by(project_id=p.id).all()
    if len(p_o_s_list) == 0:
        return {"status": "no schemes found"}
    d = {"status": "success"}
    for p_o_s in p_o_s_list:
        d.update({p_o_s.imageFileName: p_o_s.votes})
    return d


def addMessage(projectId, message_content, openid):
    """
    this function add a message from a certain fuck'in user to the certain project
    :param projectId: str
    :param message_content: str
    :param openid: str
    :return: success or not
    """
    p = getProject(projectId)
    u = getUser(openid)
    if not p or not u:
        return "wrong"
    p_o_m = Project_Owns_Messages(project_id=p.id, message_content=message_content)
    db.session.add(p_o_m)
    db.session.flush()
    db.session.commit()
    return "success"


def queryProjectOwnsSchemes(projectId):
    print("qqq", projectId)
    p = getProject(projectId=projectId)
    print(p)
    if not p:
        return "wrong"
    p_o_s_list = Project_Owns_Schemes.query.filter_by(project_id=p.id).all()
    dicts = []
    for p_o_s in p_o_s_list:
        tempD = {
            'imageFileName': p_o_s.imageFileName,
            'projectId': p_o_s.project_id,
            'votes': p_o_s.votes
        }
        dicts.append(tempD.copy())
    return dicts


def addScheme(projectId, imageFileName):
    p = getProject(projectId=projectId)
    if not p:
        return "wrong"
    p_o_s = Project_Owns_Schemes(project_id=p.id, imageFileName=imageFileName)
    db.session.add(p_o_s)
    db.session.flush()
    db.session.commit()
    return "success"


def queryCandidateScheme(projectId):
    p = getProject(projectId)
    if not p:
        return "wrong"
    p_o_s_list = Project_Owns_Schemes.query.filter_by(project_id=p.id).all()
    for p_o_s in p_o_s_list:
        if p_o_s.for_show is True:
            temp_D = {
                "imageFileName": p_o_s.imageFileName
            }
            return temp_D
    return "wrong"


def queryUserOwnsProjects(openid, startFrom, limitation):
    u = getUser(openid=openid)
    if not u:
        return "wrong"
    u_o_p_list = User_Owns_Projects.query.filter_by(user_id=u.id).all()[startFrom: startFrom + limitation]
    p_ids = []
    for u_o_p in u_o_p_list:
        p_ids.append(str(u_o_p.project_id).zfill(6))
    return p_ids


def queryUserParticipatesProjects(openid, startFrom, limitation):
    u = getUser(openid=openid)
    if not u:
        return "wrong"
    u_i_p_list = User_In_Projects.query.filter_by(user_id=u.id).all()[startFrom: startFrom + limitation]
    p_ids = []
    for u_i_p in u_i_p_list:
        p_ids.append(str(u_i_p.project_id).zfill(6))
    return p_ids


def addCandidate(projectId):
    p = getProject(projectId)
    if not p:
        return "wrong"
    # find the highest votes
    p_o_s_list = Project_Owns_Schemes.query.filter_by(project_id=p.id).all()
    if len(p_o_s_list) == 0:
        return "success"
    p_o_s_list.sort(key=lambda p_o_s: p_o_s.votes)
    for p_o_s in p_o_s_list:
        p_o_s.for_show = False
    p_o_s_list[-1].for_show = True
    for p_o_s in p_o_s_list:
        db.session.add(p_o_s)
    db.session.commit()
    return "success"


def queryWorkersAvatar(projectId):
    p = getProject(projectId)
    if not p:
        return "wrong"
    u_i_p_list = User_In_Projects.query.filter_by(project_id=p.id).all()
    workersAvatarList = []
    for u_i_p in u_i_p_list:
        user_id = u_i_p.user_id
        u = User.query.filter_by(id=user_id).first()
        workersAvatarList.append(u.avatarUrl)
    return workersAvatarList
