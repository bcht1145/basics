import requests
from psutil import *
import time
flora_api = {}  # 顾名思义,FloraBot的API,载入(若插件已设为禁用则不载入)后会赋值上


def occupying_function(*values):  # 该函数仅用于占位,并没有任何意义
    pass


send_msg = occupying_function


def init():  # 插件初始化函数,在载入(若插件已设为禁用则不载入)或启用插件时会调用一次,API可能没有那么快更新,可等待,无传入参数
    global send_msg
    print(flora_api)
    send_msg = flora_api.get("SendMsg")
    print("main_基础功能,加载成功")


def api_update_event():  # 在API更新时会调用一次(若插件已设为禁用则不调用),可及时获得最新的API内容,无传入参数
    pass

def send_image(image_path: str,msg: str | None, uid: str | int, gid: str | int | None, mid: str | int | None = None):  # 发送图片函数,image_path: 图片路径,uid: QQ号,gid: 群号,mid: 消息编号
    url = f"http://{flora_api.get("FrameworkAddress")}:"
    image_url = f"file:///D:\_文件夹工作室\_QQbot\QQBOT2\image\{image_path}"
    data = {}
    if mid is not None:  # 当消息编号不为None时,则发送的消息为回复
        data.update({"message": f"[CQ:image,file={image_url},type=show,id=40000][CQ:reply,id={mid}]{msg}"})
    else:  # 反之为普通消息
        data.update({"message": f"[CQ:image,file={image_url},type=show,id=40000]{msg}"})
    if gid is not None:  # 当群号不为None时,则发送给群聊
        url += f"/send_group_msg"
        data.update({"group_id": gid})
    else:  # 反之为私聊
        url += f"/send_private_msg"
        data.update({"user_id": uid})
    try:
        requests.post(url, json=data, timeout=5)  # 提交发送消息
    except requests.exceptions.RequestException:
        pass
#自制的，在up评论区里有^

def event(data: dict):  # 事件函数,FloraBot每收到一个事件都会调用这个函数(若插件已设为禁用则不调用),传入原消息JSON参数
    print(data)
    uid = data.get("user_id")  # 事件对象QQ号
    gid = data.get("group_id")  # 事件对象群号
    mid = data.get("message_id")  # 消息ID
    msg = data.get("raw_message")  # 消息内容
    if msg is not None:
        msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
        print(uid, gid, mid, msg)
        if uid in flora_api.get('Administrator'):
            pass
        if msg == "/运行情况":#就是运行情况
            cu = "CPU使用率："+str(cpu_percent(interval=2))+"\n内存使用率："+str(virtual_memory()[2])
            send_msg(cu,uid,gid)
        if msg == "/一言":#一言，指的是随机一句话，v1.hitokoto.cn为api（站长说他不喜欢爬虫，所以流量不要太大，也不要乱爬！）
            url = "https://v1.hitokoto.cn/?encode=json"
            response = requests.get(url)
            response_json = response.json()
            hitokoto = response_json.get("hitokoto")
            fron = response_json.get("from")
            send_msg(hitokoto+"\n——"+fron,uid,gid)
        if msg == "/获取色图":#向api.lolicon.app获取随机色图（因为代码原因，有些可能为404，所以照片损坏qwq）
            send_msg("正在获取\n因技术原因或请求人数过多\n可能导致缓慢",uid,gid)
            url = "https://api.lolicon.app/setu/v2"
            data = {
                "r18":0,
                "num":3
            }
            response = requests.post(url, json=data)
            r = 0
            json_data = response.json()
            json_data_2 = json_data.get("data")
            for i in json_data_2:
                urls = i.get("urls")
                urlss = urls.get("original")
                responses = requests.get(urlss)
                image_data = responses.content
                if i.get("ext")=="jpg":######这里要在FloraBot.py同文件夹里创建一个image文件夹，不然会报错######
                    with open("./image/image"+str(r)+".jpg", "wb") as image_file:
                        image_file.write(image_data)
                elif i.get("ext")=="png":
                    with open("./image/image"+str(r)+".png", "wb") as image_file:
                        image_file.write(image_data)
                r+=1
            r = 0
            for i in json_data_2:
                mag = "批处理文件请求第"+str(r)+"号\n标题："+i.get("title")+"\npid："+str(i.get("pid"))+"\nR18："+str(i.get("r18"))
                if i.get("ext")=="jpg":
                    send_image("image"+str(r)+".jpg",mag,uid,gid,mid)
                elif i.get("ext")=="png":
                    send_image("image"+str(r)+".png",mag,uid,gid,mid)
                r+=1
                time.sleep(0.5)
            send_msg("因QQ屏蔽或技术原因\n可能无法发送某些图片",uid,gid)
    