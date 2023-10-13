####################################################
#                    Packages                      #
####################################################
import json
import pymysql
import numpy as np
import traceback
import pandas as pd
import matplotlib.pyplot as plt
from  matplotlib import cm

####################################################
#                    Connection                    #
####################################################
db = pymysql.connect(
    host = "rm-bp1rwi5w2f4irf5q5ro.mysql.rds.aliyuncs.com",
    user = "csc4001",
    password = "csc4001@",
    port = 3306,
    db = "csc4001")
cursor = db.cursor()

####################################################
#                  Tool Functions                  #
####################################################
def curl_to_cid(u_id, ctype, url):
    if ctype == "1":
        res = select_stat('`u_clothing_id`',' `wardrobe`', ' where `picture`="{}" and u_id={};'.format(url,u_id))
        if res==():
            return None
        else:
            return res[0][0]
    elif ctype == '2':
        res = select_stat('`clothing_id`','`clothing`',' where `picture`="{}"'.format(url))
        if res==():
            return None
        else:
            return res[0][0]


def execution(command_str):
    try:
        cursor.execute(command_str)
        db.commit()
        return 1
    except pymysql.Error as e:
        print(e.args[0], e.args[1])
        db.rollback()
        return 0


def select_stat(content, table, spe_command = ''):
    command_str = "select "+content+" from "+table+spe_command+";"
    #with cursor(as_dict=as_dict) as cursor:
    print(command_str)
    execution(command_str)
    results = cursor.fetchall()
    return results


def insert_stat(table, content):
    command_str = "insert into "+table+" values ("+content+");"
    print(command_str)
    flag = execution(command_str)
    return flag


def delete_stat(table, spe_command = ''):
    command_str = "delete from"+table+spe_command+";"
    print(command_str)
    flag = execution(command_str)
    return flag
    

def update_stat(table, content, spe_command = ''):
    command_str = "update "+table+" set "+content+spe_command+";"
    print(command_str)
    flag = execution(command_str)
    return flag
    
####################################################
#                   Api Functions                  #
####################################################
# user/register
def register(accttype, password, mailbox): 
    res = select_stat('count(*)','`authority`',' where `mailbox` = "{}" group by `mailbox`'.format(mailbox))
    print(res)
    #print(res[0][0])
    if res!=():
        return 4
    insert_stat('`authority`', 'null, "{}", "{}", "{}", 1,1'.format(password, mailbox, accttype))
    cursor.execute("select last_insert_id()")
    res = cursor.fetchone()
    index = res[0]
    if (accttype=="1"):
        flag = insert_stat('`user`', '{}, "User{}", "{}", null, null'.format(index,str(index),DEFAULT_AVATAR))
    else:
        flag = insert_stat("`merchant`",'{},"Merchant{}","{}", 0.0, 0'.format(index,str(index),DEFAULT_AVATAR))
    return flag

# user/login
def login(account, password): 
    # if type(account)==int:
    #     res = select_stat('count(*),`u_id`, type','`authority`', ' where `u_id`={}'.format(account))
    if type(account)==str:
        try:
            res = select_stat('count(*)', '`authority`', ' where `mailbox`="{}" and `password`="{}" group by `mailbox`'.format(account, password))
            print(res)
            if res==(): 
                return (0,None,None)
            else:
                res2 = select_stat('`id`, `type`','`authority`', ' where `mailbox`="{}" and `password`="{}"'.format(account, password))
                return np.insert(res[0],1,(res2[0]))
        except: 
            return (0,None,None)

# user/forgetpasswd
def forgetpasswd(mailbox, new):
    flag = update_stat('`authority`','`password` = "{}"'.format(new) ,' where `mailbox` = "{}"'.format(mailbox))
    return flag

# user/info/display
def display(u_id):
    res = select_stat('`mailbox`,`type`','`authority`',' where `id`={}'.format(u_id))
    mailbox=res[0][0]
    accttype=res[0][1]
    if accttype=='1':
        res = select_stat('*', '`user`', ' where `id`={}'.format(u_id))
        nickname = res[0][1]
        figure = res[0][2]
        birthday = res[0][3]
        sex = res[0][4]
        return mailbox,nickname,figure,birthday,sex

# user/info/update
def update(u_id, mailbox, nickname,picture,birthday,sex):
    flag1 = update_stat('`authority`','`mailbox`="{}"'.format(mailbox), ' where `id`={}'.format(u_id))
    flag2 = update_stat('`user`','`nickname`="{}", `picture`="{}", birthday="{}", sex="{}"'.format(nickname,picture,birthday,sex), ' where `id` = {}'.format(u_id))
    return (flag1&flag2)

# user/info/update/profilephoto
def profilephoto(u_id, picture):
    res = select_stat('type','authority',' where id = {}'.format(u_id))
    accttype = res[0][0]
    if accttype=='1':
        flag = update_stat('`user`','`picture`="{}"'.format(picture), ' where `id`={}'.format(u_id))
    # elif accttype=='2':
    #     flag = update_stat('`merchant`','`picture`="{}"'.format(picture), ' where `id`={}'.format(u_id))
    return flag

# user/info/upload/clothesphoto
# def clothesphoto(u_id, u_cloth_url, name, label):
#     flag = insert_stat('`wardrobe`','null, {}, curtime(), "{}", "{}", {}'.format(u_id,u_cloth_url,name,label))
#     return flag

# user/likelist
def likelist(u_id):
    container = [[0,'','','']]
    container_np = np.array(container, dtype=object)
    res = select_stat('2,`u_clothing_id`,`name`,`picture`','`wardrobe`',' where `u_id` = {}'.format(u_id))
    container_np = np.insert(container_np,len(container_np),res,axis=0)
    res = select_stat('`clothing_id`', '`favorites`',' where u_id={}'.format(u_id))
    if res!=(): 
        clothing_id = res[0]
    # print(clothing_id)
        for c_id in clothing_id:
            res = select_stat('1,`clothing_id`,`name`,`picture`','`clothing`',' where `clothing_id`={}'.format(c_id))
            # print(res)
            container_np = np.insert(container_np,len(container_np),res,axis=0)
    container_np = np.delete(container_np,0,0)
    return container_np

# user/recordlist
def recordlist(u_id):
    res = select_stat('clo.`name`,clo.`picture`,pub.`effect`','`history_pub` as pub, `clothing` as clo' , ' where clo.clothing_id = pub.clothing_id and pub.u_id ={} order by `timepoint`'.format(u_id))
    res2 = select_stat('war.`name`,war.`picture`,pri.`effect`','`history_pri` as pri, `wardrobe` as war', ' where war.u_clothing_id = pri.u_clothing_id and pri.u_id={} order by `timepoint`'.format(u_id))
    res = np.insert(res, len(res), res2, axis=0)
    return res

# user/feedback
def feedback(u_id, comment):
    flag = insert_stat('`feedback`','{}, curtime(), "{}"'.format(u_id, comment))
    return flag

# tryon/like
def like(u_id, picture):
    clothing_id = curl_to_cid(u_id,'2',picture)
    if clothing_id==None: # clothing belongs to others
        return 0
    res = select_stat('count(*)','`favorites`',' where u_id={} and clothing_id={} group by u_id'.format(u_id,clothing_id))
    if res!=(): # already like
        return 2
    flag = insert_stat('`favorites`','{},{},curtime()'.format(u_id, clothing_id))
    return flag

# tryon/select
def select(u_id, labels):
    if labels!='':
        res = ''
        # res = select_stat('`clothing_id`,`name`,`picture`','`clothing`',' where json_contains(`labels`,{}'.format(labels))
    else:
        res = select_stat('`clothing_id`,`name`,`picture`','`clothing`')
    return res

# tryon/userupload
def userupload(u_id,picture,name, labels):
# def clothesphoto(u_id, u_cloth_url, name, label):
    flag = insert_stat(" `wardrobe`","null, {}, curtime(), '{}', '{}', '{}'".format(u_id,picture,name,labels))
    return flag

# tryon/try
def tryon_figure(u_id):
    res = select_stat('`picture`','`user`',' where `id` = {}'.format(u_id))
    return res[0][0]

def tryon_updatehistory(u_id, picture, ctype, effect, timepoint = 'curtime()'):
    clothing_id = curl_to_cid(u_id,ctype,picture)
    if ctype == '1':
        res = select_stat('count(*)','`wardrobe`',' where `u_id`={} and `u_clothing_id`={} group by `u_id`'.format(u_id,clothing_id))
        if res==(): 
            return 3
        flag = insert_stat('`history_pri`','null,{},{},{},"{}"'.format(u_id, clothing_id, timepoint,effect))
    elif ctype == '2':
        flag1 = insert_stat('`history_pub`','null,{},{},{},"{}"'.format(u_id,clothing_id,timepoint,effect))
        res = select_stat('`popularity`','`clothing`',' where `clothing_id`={}'.format(clothing_id))
        if res==(): return 0
        cur_pop = int(res[0][0])
        flag2 = update_stat('`clothing`',' `popularity`= {}'.format(cur_pop+1), ' where `clothing_id`={}'.format(clothing_id))
        flag = flag1&flag2
    return flag

# tryon/recommendation 
def recommendation(u_id):
    res = select_stat('`clothing_id`,`name`,`picture`,`popularity`','`clothing`',' order by `popularity` desc limit 0,10')
    return res

# reflesh popularity
def refleshpop():
    flag =update_stat('`clothing`','`popularity`=0')
    return flag

# randomRec
def randomRec(u_id):
    res = select_stat('T1.`clothing_id`,T1.`name`,T1.`picture`,T1.`popularity`', \
         '`clothing` as T1 join (select round( rand() * ((select max(`clothing_id`) from `clothing`)-(select min(`clothing_id`) from `clothing`)) + (select min(`clothing_id`) from `clothing`)) as `clothing_id`) as T2', \
         ' where T1.`clothing_id` >= T2.`clothing_id` order by T1.`clothing_id` limit 1;')
    return res[0][2]

# Merchant upload
def MUpload(m_id, picture, name, label, brand='default'):
    res = insert_stat('`clothing`',"null,'{}',{},0,'{}',curtime(),'{}','{}'".format(brand,m_id,picture,name,label))
    return res

# User drop like
def affair(u_id, picture,ctype):
    clothing_id = curl_to_cid(u_id,ctype,picture)
    res = delete_stat('`favorites`',' where `u_id`={} and `clothing_id`={}'.format(u_id,clothing_id))
    return res

def dataVis(m_id):
    res = select_stat('name,popularity' ,'`clothing`',' where m_id={} order by popularity desc'.format(m_id))
    res_pd = pd.DataFrame(res, columns=['name', 'popularity'])
    #res_pd = res_pd.groupby('`clothing_id`').size()
    labels = res_pd.name
    sizes = res_pd.popularity
    print(labels)
    print(sizes)
    # explode = [0]* sizes.shape[0] # only "explode" the 2nd slice (i.e. 'Hogs')
    # explode[0]=0.1
    fig, ax = plt.subplots()
    colors = cm.rainbow(np.arange(len(sizes))/len(sizes))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=170, colors=colors)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    fig.savefig('db_cos/2.png')

def dataVisLatest(m_id):
    cursor.execute('select * from `history_pub`')
    res = cursor.fetchall()
    print(res)
    res = select_stat('T1.date as date, count(*) as popularity','(select h_id, clothing_id, date(timepoint) as date from `history_pub` where DATE_SUB(CURDATE(), INTERVAL 6 DAY) <= date(`timepoint`)) as T1, `clothing` as T2', \
        ' where T1.clothing_id=T2.clothing_id and T2.m_id={} group by T1.date order by date'.format(m_id))
    res_pd = pd.DataFrame(res, columns=['date', 'popularity'])
    print(res_pd)
    plt.style.use('ggplot')

    fig,ax=plt.subplots(figsize=(10,8))
    ax.spines['left'].set_color('black')
    ax.spines['left'].set_linewidth(3)
    ax.spines['bottom'].set_color('black')
    ax.spines['bottom'].set_linewidth(3)

    plt.plot(res_pd.date, res_pd.popularity, linewidth=4, color='steelblue', marker='^',markersize=20, markeredgecolor='blue',markerfacecolor='darkorange')
    plt.title(' The popularity of all the clothings in the last 7 days')
    plt.xlabel('date')
    plt.ylabel('popularity')
    # frame = legend.get_frame()
    # frame.set_facecolor
    fig.savefig('db_cos/1.png', transparent=True)

DEFAULT_AVATAR = "default"

####################################################
#                  Test Connection                 #
####################################################