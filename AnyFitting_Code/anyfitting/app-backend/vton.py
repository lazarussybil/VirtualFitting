####################################################
#                    Packages                      #
####################################################
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json, pymysql, io, time
from db_cos.database_func import *
from db_cos.down_upload import *
from api import *
from wsgiref.simple_server import make_server

app=Flask(__name__)
CORS(app, resources=r'/*')
parsing_model = init_model_api()

####################################################
#                    Responses                     #
####################################################

'''

@app.route('/',methods=['POST','GET'])
def main():
    # Connection of Databases
    conn=pymysql.Connect(host='localhost',port=3306,user='root',passwd='123456',db='VaccineSys')
    cur=conn.cursor()
    sql=request.json['Query'] #sql语句
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    # Translation the data
    key_data = [i for i in range(0,len(data))]
    value_data = [i for i in range(0,len(data[0]))]
    for i in range(0,len(data)):
        for j in range (0,len(data[0])):
            if (j==1):
                value_data[j] = int(data[i][1])
            else:
                value_data[j] = data[i][j]
    json_result = []
    json_result.append(key_data)
    json_result.append(value_data)
    json_str = json.dumps(json_result)
    # Return the query result by input
    return "{data}".format(data=json_str)


'''

# 现在所有的异常都被归到了flag=0里 这里面包括 type非法 邮箱已经存在
# 邮箱超过五十个字符 密码超过二十个字符 后面有时间就把它们分开来
@app.route('/user/register',methods=['POST','GET'])
def register_backend():
    type = request.args.get('type')
    mailbox = request.args.get('mailbox')
    passwd = request.args.get('password')
    flag = register(type,passwd,mailbox)
    result = json.loads('{"code":200,"message":"success","data":{"SFF":true}}')
    if (not flag):
        result = json.loads('{"code":400,"message":"operation fail","data":{"SFF":false}}')
    return result

# 同样 异常输入还没有考虑 现在只是单纯的用SFF来区分成功和不成功 
# TODO id还没有嵌套进返回 然后异常没考虑
@app.route('/user/login',methods=['POST','GET'])
def login_backend():
    mailbox = request.args.get('mailbox')
    passwd = request.args.get('password')
    exist = login(mailbox,passwd)
    # print(exist)
    try:
        if (exist[0]==1):
            return json.loads('{"code":200,"message":"success","data":{"SFF":true,"ID":'+str(exist[1])+'}}')
        else:
            return json.loads('{"code":400,"message":"fail","data":{"SFF":false,"ID":null}}')
    except Exception:
        return json.loads('{"code":400,"message":"fail","data":{"SFF":false,"ID":null}}')

# 前端做了吗？ 没有
@app.route('/user/forgetpasswd',methods=['POST','GET'])
def forgetpasswd_backend():
    mailbox = request.args.get('mailbox')
    return json.loads('{"code":400,"message":"fail","data":{"SFF":false,"ID":null}}')

# result里可能有None？
@app.route('/user/info/display',methods=['POST','GET'])
def display_backend():
    try:
        uid = request.args.get('id')
        result = display(uid)
        return json.loads('{"code":200,"message":"success","data":{"mailbox":"'+str(result[0])+'","nickname":"'+str(result[1])+'","figure":"'+str(result[2])+'","birthday":"'+str(result[3])+'","sex":"'+str(result[4])+'"}}')
    except Exception:
        return json.loads('{"code":400,"message":"Wrong Uid","data":null}')

@app.route('/user/info/image',methods=['POST','GET'])
def get_img():
    try:
        uid = request.args.get('uid')
        result = tryon_figure(uid)
        print(result)
        return json.loads('{"code":200,"message":"success","data":{"human_url":"'+str(result)+'"}}')
    except Exception:
        return json.loads('{"code":400,"message":"fail","data":null}')

# llx的数据库有问题 让他赶紧改
@app.route('/user/info/update',methods=['PUT','POST','GET'])
def update_backend():
    id = request.args.get('id')
    mailbox = request.args.get('mailbox')
    passwd = request.args.get('password')
    nickname = request.args.get('nickname')
    picture = request.args.get('picture')
    birthday = request.args.get('birthday')
    sex = request.args.get('sex')
    flag = update(id,mailbox,nickname,picture,birthday,sex)
    if (flag):
        return json.loads('{"code":200,"message":"success","data":null}')
    else:
        return json.loads('{"code":400,"message":"fail","data":null}')

# 头像图片不需要？
@app.route('/user/upload/profilephoto',methods=['POST','GET'])
def profilephoto():
    return (json.loads('"SFF:T"'))

# name和label都还没确定 待定 以及非法输入问题
@app.route('/user/upload/clothesphoto',methods=['POST','GET'])
def clothesphoto():
    id = request.args.get('id')
    url = request.args.get('url')
    flag = userupload(id,url,url,'{"label1":"male"}')
    if (flag):
        return json.loads('{"code":200,"message":"success","data":null}')
    else:
        return json.loads('{"code":400,"message":"fail","data":null}')

@app.route('/shopkeeper/upload/clothesphoto',methods=['POST','GET'])
def keeper_clothesphoto():
    id = request.args.get('id')
    url = request.args.get('image')
    name = str(time.time())
    flag = MUpload(id,url,name,'{"label1":"male"}')
    if (flag):
        return json.loads('{"code":200,"message":"success","data":null}')
    else:
        return json.loads('{"code":400,"message":"fail","data":null}')

# name和label都还没确定 待定 以及非法输入问题
@app.route('/user/upload/pictures',methods=['POST','GET'])
def pictures():
    try:
        image = request.files['image']
        imgname = image.filename
        path = 'Database/val/temp/'+imgname
        image.save(path)
        upload_cos(path,imgname)
        url = 'https://csc4001-1258905014.cos.ap-shanghai.myqcloud.com/'+imgname
        return json.loads('{"code":200,"message":"success","data":{"cloth_url":"'+url+'"}}')
    except Exception:
        return json.loads('{"code":400,"message":"fail","data":null}')

# 商家和个人？也没有非法输入处理 我要杀了李龙翔 返回值对吗？？？
@app.route('/user/likelist',methods=['POST','GET'])
def likelist_backend():
    id = request.args.get('userid')
    try:
        result = likelist(id)
        dict = { }
        dict['code'] = 200
        dict['message'] = "success"
        dict['data'] = result.tolist()
        dict_json = json.dumps(dict)
        return dict_json
    except Exception:
        return json.loads('{"code":400,"message":"fail","data":{"clothes":null}}')

# 用户喜欢一件衣服
@app.route('/user/like',methods=['POST','GET'])
def like_backend():
    uid = request.args.get('id')
    cloth_url = request.args.get('cloth_url')
    try:
        flag = like(uid,cloth_url)
        if (flag):
            return json.loads('{"code":200,"message":"success","data":null}')
        else:
            return json.loads('{"code":400,"message":"fail","data":null}')
    except Exception:
        return json.loads('{"code":400,"message":"error","data":null}')

# 用户喜欢一件衣服
@app.route('/user/affair',methods=['POST','GET'])
def affair_backend():
    uid = request.args.get('id')
    cloth_url = request.args.get('cloth_url')
    ctype = '1'
    try:
        if (cloth_url[len(cloth_url)-1]=='_'):
            ctype = '2'
        print(uid,cloth_url,ctype)
        flag = affair(uid,cloth_url,ctype)
        if (flag):
            return json.loads('{"code":200,"message":"success","data":null}')
        else:
            return json.loads('{"code":400,"message":"fail","data":null}')
    except Exception:
        return json.loads('{"code":400,"message":"error","data":null}')

# 格式和文档里不一样
@app.route('/user/recordlist',methods=['POST','GET'])
def recordlist_backend():
    id = request.args.get('id')
    result = recordlist(id)
    if (result.all==None):
        return json.loads('{"code":400,"message":"No record exists","data":null}')
    else:
        dict = { }
        dict['code'] = 200
        dict['message'] = "success"
        dict['data'] = result.tolist()
        dict['recordnum'] = result.size
        dict_json = json.dumps(dict)
        return dict_json

# 应该没什么问题
@app.route('/tryon/tryon',methods=['POST','GET'])
def tryon():
    try:
        cloth_url = request.args.get('cloth_url')
        human_url = request.args.get('human_url')
        cloth_name = cloth_url[cloth_url.rfind('/')+1:len(cloth_url)]
        human_name = human_url[human_url.rfind('/')+1:len(human_url)]
        cloth = download_cos(cloth_name)
        human = download_cos(human_name)
        processed_cloth,mask = upload_cloth_api(cloth)
        result = tryon_cloth_api(parsing_model,processed_cloth,human,mask)
        img_byte = io.BytesIO()
        result.save(img_byte,format='PNG')
        byte_str = img_byte.getvalue()
        ti = time.time()
        filename = str(ti)+'.png'
        binary_upload_cos(byte_str,filename)
        header_url = 'https://csc4001-1258905014.cos.ap-shanghai.myqcloud.com/'+filename
        
        return json.loads('{"code":200,"message":"success","data":{"tryon_url":"'+header_url+'"}}')
    except Exception:
        return json.loads('{"code":400,"message":"No record exists","data":null}')

@app.route('/recommendation/top',methods=['POST','GET'])
def recommendation_backend():
    uid = request.args.get('uid')
    try:
        tmp = recommendation(uid)
        result = []
        for i in tmp:
            result.append(list(i))
        for i in range(0,len(result)):
            result[i][0] = i+1
        dict = {}
        dict['code'] = 200
        dict['message'] = 'success'
        dict['data'] = result
        return json.dumps(dict)
    except Exception:
        return json.loads('{"code":400,"message":"No record exists","data":null}')

@app.route('/recommendation/recommendation',methods=['POST','GET'])
def recommend_backend():
    try:
        result = []
        count = 1
        while (count<6):
            tmp = randomRec(21)
            if (not (tmp in result)):
                result.append(tmp)
                count += 1
        dict = {}
        dict['code'] = 200
        dict['message'] = 'success'
        dict['cloth'] = result
        return json.dumps(dict)
    except Exception:
        return json.loads('{"code":400,"message":"No record exists","cloth":null}')

@app.route('/tryon/datavis',methods=['POST','GET'])
def datavis_backend():
    uid = request.args.get('uid')
    try:
        dataVisLatest(uid)
        dataVis(uid)
        ti = time.time()
        filename1 = 'fig1_'+str(ti)+'.png'
        filename2 = 'fig2_'+str(ti)+'.png'
        upload_cos("db_cos/1.png",filename1)
        upload_cos("db_cos/2.png",filename2)
        header_url = 'https://csc4001-1258905014.cos.ap-shanghai.myqcloud.com/'
        analysis = [header_url+filename1,header_url+filename2]
        dict = {}
        dict['code'] = 200
        dict['message'] = 'success'
        dict['data'] = list(analysis)
        return json.dumps(dict)
    except Exception:
        return json.loads('{"code":400,"message":"No record exists","data":null}')

'''

@app.route('/user/feedback',methods=['POST','GET'])
def feedback():
    return (json.loads('"SFF:T"'))

@app.route('/tryon/like',methods=['POST','GET'])
def like():
    return (json.loads('"SFF:T"'))

@app.route('/tryon/getclothes',methods=['POST','GET'])
def getclothes():
    return (json.loads('{"ClothesURL":"https://csc4001-1258905014.cos.ap-shanghai.myqcloud.com/README"}'))

@app.route('/tryon/select',methods=['POST','GET'])
def select():
    return (json.loads('{"ClothesURL":"https://csc4001-1258905014.cos.ap-shanghai.myqcloud.com/README"}'))

@app.route('/tryon/upload',methods=['POST','GET'])
def upload():
    return (json.loads('"SFF:T"'))

@app.route('/recommendation/top',methods=['POST','GET'])
def top():
    return (json.loads('{"ClothesID":"1","ClothesName":"xinfei","ClothesURL":"https://csc4001-1258905014.cos.ap-shanghai.myqcloud.com/README","Label":"1"}'))

'''

####################################################
#                    Main Func                     #
####################################################
if __name__ =="__main__":
    server = make_server('127.0.0.1', 6002, app)
    server.serve_forever()    
    app.run() 
