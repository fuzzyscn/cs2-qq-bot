import os
import time
import json
import websocket#先用 pip install websocket-client 安装websocket模块 QQ机器人 正向WS服务器监听地址：6700 代码115行可以改
import threading

ip = '127.0.0.1'
password = 'rconpassword'#rcon密码
qqNum = 2561417364
qqQunNum = 314498023
serverIp = 'csgo2.v6.army'

def sendJsonToQQ(msg):
    msgData = {
        "action": "send_private_msg",
        "params": {
            "user_id": qqNum,
            "message": msg
        },
        #"echo": "123"
    }
    wsQQ.send(json.dumps(msgData))
    
def sendJsonToQQun(msg):
    msgData = {
        "action": "send_group_msg",
        "params": {
            "group_id": qqQunNum,
            "message": msg
        },
        #"echo": "123"
    }
    wsQQ.send(json.dumps(msgData))
    
def on_qq_message(ws, message):
    msg = json.loads(message)
    if 'message_type' in msg:
        print(msg['message_type'].replace('private', '私聊命令')+'||'+msg['sender']['nickname'] + ': '+msg['raw_message'])
        if msg['message_type'] == 'private':
            privateCommand = ' '+msg['raw_message'].replace(' ', '_')#私聊命令中不能有空格
            response = os.popen('rcon.exe -a '+ip+':27015 -p '+password+privateCommand).read()
            string = ''
            if response:
                string = ' 返回：'+response
            sendJsonToQQ('管理员：'+msg['sender']['nickname']+' 使用了命令:'+privateCommand+string)
        elif msg['message_type'] == 'group':
            if msg['raw_message'].find('服务器') != -1 or msg['raw_message'].find('查询') != -1 or msg['raw_message'].find('在线') != -1 or msg['raw_message'].find('人数') != -1:#监测群消息的关键词
                response = os.popen('rcon.exe -a '+ip+':27015 -p '+password+' status').read()
                lines = response.split('\n')
                lineNum = len(lines)
                BotNum = 0
                NoChan = 0
                PlayerNum = 0
                if lineNum > 23:
                    for i in range(21, lineNum-2):
                        if lines[i].find('BOT') != -1:
                            BotNum = BotNum + 1
                        elif lines[i].find('[NoChan]') != -1:
                            NoChan = NoChan + 1
                        else:
                            PlayerNum = PlayerNum + 1
                            
                    sendJsonToQQun('当前在线 '+ str(PlayerNum) +' 人，BOT:' + str(BotNum) + '个！')
                else:
                    sendJsonToQQun('当前无人在线！按~控制台输入：connect '+serverIp+' 进服')

def on_qq_error(ws, error):
    print('### QQ机器人服务器出现错误：### ' + str(error))

def on_qq_close(ws):
    print('### 与QQ机器人服务器断开连接 ###')
    
def on_qq_open(ws):
    print('\n ### QQ机器人连接成功啦！###')
    
def main():
    msg = input("更换命令 例如:bot_add bot_kick:")
    if msg != '':
        msg = msg.replace(' ', '_')
        response = os.popen('rcon.exe -a '+ip+':27015 -p '+password+' '+msg).read()
        string = ''
        if response:
            string = ' 返回：'+response
        sendJsonToQQ('后台使用了命令：'+msg+string)
    main()
    
def check_status_forever():
    command = " status"
    while True:
        time.sleep(120)#检测间隔时间一分钟 代码127 128行开启此检测线程
        response = os.popen('rcon.exe -a '+ip+':27015 -p '+password+command).read()
        lines = response.split('\n')
        lineNum = len(lines)
        BotNum = 0
        NoChan = 0
        PlayerNum = 0
        if lineNum > 23:
            for i in range(21, lineNum-2):
                if lines[i].find('BOT') != -1:
                    BotNum = BotNum + 1
                elif lines[i].find('[NoChan]') != -1:
                    NoChan = NoChan + 1
                else:
                    PlayerNum = PlayerNum + 1
                    
            if PlayerNum >= 1:
                sendJsonToQQun('当前在线 '+ str(PlayerNum) +' 人，BOT:' + str(BotNum) + '个！')
        else:
            #sendJsonToQQ('服务器当前无人在线！')
            playerLine = lines[11].split(',')
            print('当前假的在线' + playerLine[0].replace('players', '玩家').replace('humans', ''))#不确定是否还有用 先留着
    
if __name__ == '__main__':
    websocket.enableTrace(False)
    wsQQ = websocket.WebSocketApp('ws://127.0.0.1:6700/',#QQ机器人 正向WS服务器监听地址
        on_message = on_qq_message,
        on_error = on_qq_error,
        on_close = on_qq_close,
        on_open = on_qq_open)
    
    def runWsQQ():
        wsQQ.run_forever()
        
    ThreadWsQQ = threading.Thread(target=runWsQQ)
    ThreadWsQQ.start()
    
    ThreadCheckGtaSev = threading.Thread(target=check_status_forever)
    ThreadCheckGtaSev.start()
    
    main()