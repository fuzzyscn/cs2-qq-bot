import time
import threading
from rcon.source import Client#先用 pip install rcon安装rcon模块 

ip = '101.35.246.92'
port = 27015
pw = ''#自行修改rcon密码 此版本只有自动开启跑图模式功能

def main():
    msg = input("输入命令 例如:status sv_cheats bot_kick:")
    if msg != '':
        with Client(ip, port, passwd=pw) as client:
            response = client.run(msg)
            string = ''
            if response:
                string = ' 返回：'+response
            print('后台使用了命令：'+msg+string)
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
                for i in range(begin, lineNum-2):#22 -2
                    if lines[i].find('BOT') != -1:
                        BotNum = BotNum + 1
                    elif lines[i].find('[NoChan]') != -1:
                        NoChan = NoChan + 1
                    else:
                        print(lines[i])
                        PlayerNum = PlayerNum + 1
                        
                if PlayerNum >= 1:
                    print('当前在线 '+ str(PlayerNum) +' 人，BOT:' + str(BotNum) + '个！地图：'+map)
                    response = client.run('sv_cheats')
                    if response.find('false') != -1:
                        client.run('exec paotu')
                        client.run('hostname CS2 Fuzzys 跑图服 CHINA上海 QQ群:314498023')#自行修改
                        client.run('say 欢迎游玩Fuzzys的上海跑图服 QQ群:314498023')#自行修改
                        client.run('say 已为您开启跑图模式，可自行投票换地图哦🐀')
                        print('已开启跑图模式')
            else:
                playerLine = lines[11].split(',')
                print('当前假的在线' + playerLine[0].replace('players', '玩家').replace('humans', '人类'))#不确定是否还有用 先留着
    
if __name__ == '__main__':
    ThreadCheckGtaSev = threading.Thread(target=check_status_forever)
    ThreadCheckGtaSev.start()
    
    main()