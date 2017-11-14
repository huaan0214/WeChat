import requests

def getResponse(_info):
	#print(_info)
	apiUrl = 'http://www.tuling123.com/openapi/api'
	data = {
    	'key'    : '51d8e1c9a609462996adf007bb8f2343', # 如果这个Tuling Key不能用，那就换一个
    	'info'   : _info, # 这是我们发出去的消息
    	'userid' : 'wechat-robot', # 这里你想改什么都可以
	}
	# 我们通过如下命令发送一个post请求
	r = requests.post(apiUrl, data=data).json()

	# 让我们打印一下返回的值，看一下我们拿到了什么
	return r
'''
while(1):
        
        rrr=str(input('输入查询信息：'))
        print(getResponse(rrr))
'''
#print(getResponse("早上好"))
