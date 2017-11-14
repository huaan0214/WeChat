import itchat
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime,timedelta
from tuling import getResponse

itchat.auto_login(hotReload=True)

sched=BackgroundScheduler()#后台调度器初始化
setTime=[]#初始化定时时间
def setLargeTime(): 
    largeTime=(datetime.now()+timedelta(days=30)).strftime('%Y,%m,%d,%H,%M,%S')#default定时时间最大为当前时间+30天
    for each in largeTime.split(',',5):
        setTime.append(int(each))#把datetime转换成str再转换为int ，初始化最大定时设定时间
setLargeTime()

getTime=datetime(setTime[0],setTime[1],setTime[2],setTime[3],setTime[4],setTime[5])#获取int型时间，用来定时
msgToUser='您已登录小助手,每次选择功能请回复:设置'#default发送内容
numberOfTimes=0#轰炸次数
rate=1#轰炸频率1S default

#用于功能选择
setting=0#1进入设置，0退出设置
function=0#0无功能，1,2 分别对应其他功能
ok=0#设置完成标志
rbtFlag=0#判定是否选择机器人回复
#功能对象初始化为用户自己,发送问候语
toUserNickName=itchat.get_friends()[0]['NickName']
toUserName_Info=itchat.search_friends(toUserNickName)
toUserName=toUserName_Info[0]['UserName']
itchat.send(msgToUser,toUserName)

#定时发送
def my_job():
    nowTime=str(datetime.now())#获取当前时间
    itchat.send(msgToUser,toUserName)#发送消息


#每一秒刷新一次值，如果有输入就会更新
def refresh():
    global ok,function
    getTime=datetime(setTime[0],setTime[1],setTime[2],setTime[3],setTime[4],setTime[5])
    #如果设置完成则执行下面其中一个（输入有更新的）
    if ok==1:
        ok=0
        if function==1:
            function=0
            trigger1 = DateTrigger(run_date=getTime)
            setLargeTime()
            sched.add_job(my_job,trigger1)
        if function==2:
            function=0
            trigger2 = IntervalTrigger(seconds=rate,start_date=(datetime.now()),end_date=(datetime.now()+timedelta(seconds=rate*(numberOfTimes-1))))
            sched.add_job(my_job,trigger2)
trigger0 = IntervalTrigger(seconds=1)
sched.add_job(refresh,trigger0)               
#微信消息分析   
@itchat.msg_register('Text')
def msgAbout(msg):
    global setting,function,ok,rbtFlag
    global toUserNickName,setTime, msgToUser,toUserName
    global numberOfTimes,rate
    if(msg['FromUserName']==msg['ToUserName']):#我自己发消息
        #print(msg)
        #setting==0,为开始设置
        if(setting==0):
            if(msg['Text']=='设置'):
                setting=1
                return '请回复数字选择功能：\n1.定时发送消息\n2.消息轰炸\n3.让好友和机器人聊天'
            else:
                return '输入有误,开启功能回复:设置'
        #setting==1，function==0，开始功能选择    
        if(setting==1 and function==0 and rbtFlag==0):
            if msg['Text']=='1':
                function=1
                return '请回复:接收人+设置时间+消息内容\nexp:耿华安+2017,10,23,13,20,0+消息内容。中间用+连接,时间格式为:\n 年,月,日,时,分,秒'
            elif msg['Text']=='2':
                function=2
                return '请回复:接收人+间隔（秒）+次数+消息内容\nexp:耿华安+3+10+爆炸'
            elif msg['Text']=='3':
                function=3
                return '请回复:接收人（退出聊天机器人请回复:关闭）\n(ps:无聊的话回复你自己昵称试试)'
            else:
                function=0
                return '功能选择有误，请重新回复'
         #功能选择1   
        if(setting==1 and function==1):
            try:
                toUserNickName=msg['Text'].split('+',2)[0]
                inputTime=msg['Text'].split('+',2)[1]
                msgToUser=msg['Text'].split('+',2)[2]
            except :
                setting=1
                function=1
                return '请按照格式输入'

            try:
                toUserName_Info=itchat.search_friends(toUserNickName)#获取好友信息
                toUserName=toUserName_Info[0]['UserName']#取出tuUserName  
            except:
                setting=1
                function=1
                return '查无此人,请回复备注或昵称'
                
            if(len(inputTime)):
                setTime.clear()
            try:
                for t in inputTime.split(',',5):
                    setTime.append(int(t))
            except:   
                setting=1
                function=1
                return '时间输入无法匹配,请按照格式回复'
            
            ok=1
            setting=0
            return '设置OK!\n接收人:'+toUserNickName+'\n设定时间:'+inputTime+'\n内容:'+ msgToUser
        #功能选择2
        if(setting==1 and function==2):
            try:
                toUserNickName=msg['Text'].split('+',3)[0]
                rate=int(msg['Text'].split('+',3)[1])
                numberOfTimes=int(msg['Text'].split('+',3)[2])
                msgToUser=msg['Text'].split('+',3)[3]
            except :
                setting=1
                function=2
                return '请按照格式输入'
            try:
                toUserName_Info=itchat.search_friends(toUserNickName)#获取好友信息
                toUserName=toUserName_Info[0]['UserName']#取出tuUserName  
            except:
                setting=1
                function=2
                return '查无此人,请回复备注或昵称'
                    
            ok=1
            setting=0
            return '设置OK\n接收人:'+toUserNickName+'\n内容'+ msgToUser+'\n次数:'+str(numberOfTimes)
        #功能选择3
        if(setting==1 and function==3):
            
            try:
                toUserName_Info=itchat.search_friends(msg['Text'])#获取好友信息
                toUserName=toUserName_Info[0]['UserName']#取出tuUserName  
            except:
                setting=1
                function=3
                return '查无此人,请回复备注或昵称'
            function=0
            rbtFlag=1
            return '设置OK,开始与'+toUserName_Info[0]['NickName']+'发起消息,让机器人回复吧'
        #关闭机器人
        if msg['Text']=='关闭':
            rbtFlag=0
            setting=0
            return '聊天机器人已关闭,回复‘设置’可选择其他功能'
    if(rbtFlag):
        if(msg['FromUserName']==toUserName):
            res=getResponse(msg["Text"])#获取图灵机器人的回复
            try:#这里主要防止有的回复有链接；如果不存在链接执行except
                itchat.send(res["text"]+res['url'],toUserName)#讲机器人的回复发给该用户
            except KeyError:
                itchat.send(res["text"],toUserName)#讲机器人的回复发给该用户    
            
        
sched.start()
itchat.run()
sched.shutdown()
print('已退出')
