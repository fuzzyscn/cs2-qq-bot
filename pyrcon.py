import time
import json
import websocket#先用 pip install websocket-client rcon安装websocket 和 rcon模块 QQ机器人 正向WS服务器监听地址：6700 代码115行可以改
import threading
from rcon.source import Client

ip = '101.35.246.92'
port = 27015
pw = ''#自行修改rcon密码

adminQqNum = 913803796
fuZhuQqNum = 2561417364
qqQunNum = 314498023
serverIp = '101点35点246点92'

def sendJsonToFuzhuQQ(msg):#通知服主
    msgData = {
        "action": "send_private_msg",
        "params": {
            "user_id": fuZhuQqNum,
            "message": msg
        },
        #"echo": "123"
    }
    wsQQ.send(json.dumps(msgData))

def sendJsonToAdminQQ(msg):#通知管理员
    msgData = {
        "action": "send_private_msg",
        "params": {
            "user_id": adminQqNum,
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
        #print(msg['message_type'].replace('private', '私聊命令')+'||'+msg['sender']['nickname'] + ': '+msg['raw_message'])
        if msg['message_type'] == 'private' and msg['user_id'] == adminQqNum:
            privateCommand = msg['raw_message']
            with Client(ip, port, passwd=pw) as client:
                response = client.run(privateCommand)
                string = ''
                if response:
                    string = ' 返回：' + response
                sendJsonToAdminQQ('管理员：'+msg['sender']['nickname']+' 使用了命令:'+privateCommand+string)
        elif msg['message_type'] == 'private' and msg['user_id'] == fuZhuQqNum:
            privateCommand = msg['raw_message']
            with Client(ip, port, passwd=pw) as client:
                response = client.run(privateCommand)
                string = ''
                if response:
                    string = ' 返回：' + response
                sendJsonToFuzhuQQ('服主：'+msg['sender']['nickname']+' 使用了命令:'+privateCommand+string)
        elif msg['message_type'] == 'group' and msg['group_id'] == qqQunNum:
            if msg['raw_message'].find('服务器') != -1 :#监测群消息的关键词
                with Client(ip, port, passwd=pw) as client:
                    response = client.run('status')
                    lines = response.split('\n')
                    lineNum = len(lines)
                    BotNum = 0
                    NoChan = 0
                    PlayerNum = 0
                    PlayerList = []
                    begin = 23
                    map = '暂无'
                    if lineNum > 23:
                        if lines[13].find('de_nuke') != -1:
                            begin = 25
                            map = '核子危机'
                        elif lines[13].find('de_vertigo') != -1:
                            begin = 25
                            map = '陨命大厦'
                        elif lines[13].find('de_dust2') != -1:
                            map = '炙热沙城II'
                        elif lines[13].find('de_overpass') != -1:
                            begin = 25
                            map = '死亡游乐园'
                        elif lines[13].find('de_mirage') != -1:
                            map = '荒漠迷城'
                        elif lines[13].find('cs_office') != -1:
                            map = '办公室'
                        elif lines[13].find('de_inferno') != -1:
                            begin = 24
                            map = '炼狱小镇'
                        elif lines[13].find('de_anubis') != -1:
                            map = '阿努比斯'
                        elif lines[13].find('de_ancient') != -1:
                            map = '远古遗迹'
                        elif lines[13].find('cs_italy') != -1:
                            map = '意大利小镇'
                        print(map)
                        for i in range(begin, lineNum-2):#22 -2 
                            if lines[i].find('BOT') != -1:
                                BotNum = BotNum + 1
                            elif lines[i].find('[NoChan]') != -1:
                                NoChan = NoChan + 1
                            else:
                                print(lines[i])
                                playerName = lines[i].split("'")
                                PlayerList.append(playerName[1])
                                PlayerNum = PlayerNum + 1
                                
                        if PlayerNum >= 1:
                            PLString = ' '
                            for name in PlayerList:
                                PLString = PLString + name + ' '
                            sendJsonToQQun('地图：'+map+' 在线 '+ str(PlayerNum) +' 人:' + PLString)
                        else:
                            sendJsonToQQun('地图：'+map+' 当前无人在线！按~控制台输入：connect '+serverIp+' 进跑图服 版本号13942')
                    else:
                        print('地图：'+map+'当前无人在线！')
            elif msg['raw_message'].find('ip') != -1:
                sendJsonToQQun('按~控制台输入：connect '+serverIp+' 进跑图服 版本号13942')
def on_qq_error(ws, error):
    print('### QQ机器人服务器出现错误：### ' + str(error))

def on_qq_close(ws):
    print('### 与QQ机器人服务器断开连接 ###')
    
def on_qq_open(ws):
    print('\n ### QQ机器人连接成功啦！###')
    
def main():
    msg = input("输入命令 例如:bot_add bot_kick:")
    if msg != '':
        with Client(ip, port, passwd=pw) as client:
            response = client.run(msg)
            string = ''
            if response:
                string = ' 返回：'+response
            sendJsonToFuzhuQQ('后台使用了命令：'+msg+string)
            #print('后台使用了命令：'+msg+string)
    main()
    
def check_status_forever():
    while True:
        time.sleep(120)#检测间隔时间2分钟 检测时间过短可能会在换地图期间出bug
        with Client(ip, port, passwd=pw) as client:
            response = client.run('status')#利用status命令获取在线人数等信息
            lines = response.split('\n')
            lineNum = len(lines)
            BotNum = 0
            NoChan = 0
            PlayerNum = 0
            begin = 23
            map = '暂无'
            if lineNum > 23:
                if lines[13].find('de_nuke') != -1:
                    begin = 25#处理部分status输出长短不一致问题
                    map = '核子危机'
                elif lines[13].find('de_vertigo') != -1:
                    begin = 25
                    map = '陨命大厦'
                elif lines[13].find('de_dust2') != -1:
                    map = '炙热沙城II'
                elif lines[13].find('de_overpass') != -1:
                    begin = 25
                    map = '死亡游乐园'
                elif lines[13].find('de_mirage') != -1:
                    map = '荒漠迷城'
                elif lines[13].find('cs_office') != -1:
                    map = '办公室'
                elif lines[13].find('de_inferno') != -1:
                    begin = 24
                    map = '炼狱小镇'
                elif lines[13].find('de_anubis') != -1:
                    map = '阿努比斯'
                elif lines[13].find('de_ancient') != -1:
                    map = '远古遗迹'
                elif lines[13].find('cs_italy') != -1:
                    map = '意大利小镇'
                #print(map)
                for i in range(begin, lineNum-2):#22 -2
                    if lines[i].find('BOT') != -1:
                        BotNum = BotNum + 1
                    elif lines[i].find('[NoChan]') != -1:
                        NoChan = NoChan + 1
                    else:
                        print(lines[i])
                        PlayerNum = PlayerNum + 1
                        
                if PlayerNum >= 1:
                    sendJsonToFuzhuQQ('当前在线 '+ str(PlayerNum) +' 人，BOT:' + str(BotNum) + '个！地图：'+map)
                    response = client.run('sv_cheats')
                    if response.find('false') != -1:
                        client.run('exec sb')
                        client.run('hostname CS2 Fuzzys 跑图服 CHINA上海 QQ群:314498023')
                        client.run('say 欢迎游玩Fuzzys的上海跑图服 QQ群:314498023')
                        client.run('say 已为您开启跑图模式，可自行投票换地图哦🐀')
                        print('已开启跑图模式')
            else:
                playerLine = lines[11].split(',')
                print('当前假的在线' + playerLine[0].replace('players', '玩家').replace('humans', '人类'))#不确定是否还有用 先留着
    
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