from mintAPI import *
import json, codecs, sys, time, datetime, threading, LineService
import traceback, re, random, requests, time, sys, ast, os
#from humanfriendly import format_timespan, format_size, format_number, format_length
from multiprocessing import Process

from thrift.unverting import *
from thrift.TMultiplexedProcessor import *
from thrift.TSerialization import *
from thrift.TRecursive import *
from thrift import transport, protocol, server
from thrift.protocol import TCompactProtocol
from thrift.transport import THttpClient
from ttypes import LoginRequest

CLIENTAPP = "IOSIPAD\t8.12.2\tPASUNX\t11.2.5"
APP = "DESKTOPMAC\t10.10.2-YOSEMITE-x64\tMAC 4.5.0"
OAAPP = "BIZANDROID\t8.10.1\tiPhone OS\t11.2.5"

try:
    client = LINE(sys.argv[1], appName=APP)
except:
    #print("[AUTO LOGIN] Login Fail")
    sys.exit()

startTime = time.time()

helper1 = None
helper2 = None
helper3 = None

pr = client.getProfile()
cl = pr.mid

try:
    if sys.argv[3]:
        print("[AUTO LOGIN] " + pr.displayName)
    else:
        print("[LOGIN] " + pr.displayName)
except:
    print("[LOGIN] " + pr.displayName)

h1, h2, h3 = None, None, None
KR = None

KickerLogin = False
KickerKey = "dion"
dionMID = [cl]
dionMIDWithOutCL = []

fightmode = {"gid":{}}

poll = OEPoll(client)
kickerPoll = None

ReaderChecker = {"readRom":{}}

RealTimeStatus = False
StatusConut, StatusUpdate, OldStatus = 0, False, pr.statusMessage

#saved = {"readPoint":{},"readMember":{},"setTime":{},"ROM":{},"invite":{},"changesetting":{},"protectkick":{},"blacklist":{},"autoread":false,"kicker":{"1":"#","2":"#","3":"#"}}

try:
    dionLoad = codecs.open(cl+".json","r","utf-8")
    dion = json.load(dionLoad)
except:
    if os.path.exists(cl+".json"):
        os.remove(cl+".json")
    time.sleep(0.5)
    f = open(cl+'.json', 'a+')
    f.write('{"readPoint":{},"readMember":{},"setTime":{},"ROM":{},"invite":{},"changesetting":{},"protectkick":{},"blacklist":{},"autoread":false,"kicker":{"1":"#","2":"#","3":"#"}}')
    f.close()
    dionLoad = codecs.open(cl+".json","r","utf-8")
    dion = json.load(dionLoad)

kickerHelpMessage = """----------- จัดการบัญชี -----------
- [OWNER] {key}:ban (@) แบนสมาชิก
- [OWNER] {key}:unban (@) ปลดแบนสมาชิก
- {key}:clearban ล้างบัญชีดำ
- {key}:checkban ตรวจสอบบัญชีดำ

----------- การตั้งค่า -----------
- [OWNER] {key}:preventkick:on/off เปิด/ปิดป้องกันการเตะ
- [OWNER] {key}:preventinvite:on/off เปิด/ปิดป้องกันการเชิญสมาชิก
- {key}:setting ตรวจสอบการตั้งค่า"""

kickerHelp2Message = """----------- จัดการบัญชี -----------
- [ADMIN] {key}:ban (@) แบนสมาชิก
- [ADMIN] {key}:unban (@) ปลดแบนสมาชิก
- {key}:clearban ล้างบัญชีดำ
- {key}:checkban ตรวจสอบบัญชีดำ

----------- จัดการ ADMIN -----------
- [OWNER] {key}:adminadd [@] เพิ่มแอดมิน
- [OWNER] {key}:admindel [@] ลบแอดมิน
- {key}:admin ตรวจสอบแอดมิน

----------- การตั้งค่า -----------
- [ADMIN] {key}:preventkick:on/off เปิด/ปิดป้องกันการเตะ
- [ADMIN] {key}:preventinvite:on/off เปิด/ปิดป้องกันการเชิญสมาชิก
- {key}:setting ตรวจสอบการตั้งค่า"""

userDetail = """----------- รายละเอียดบัญชี -----------
ชื่อผู้ใช้: {bName}
ID ผู้ใช้: {bMID}
เวลาทำงาน: {bRuntime}
เวลาคงเหลือ: {timeleft}

""".format(bName="{bName}",bMID=cl,bRuntime="{bRuntime}",timeleft="{tl}")

ty = sys.argv[2]

selfHelpMessage = """คำสั่งทั้งหมด [FLK VERSION]
DION CHAN NEW VERSION

{detail}----------- คำสั่งพื้นฐาน -----------
- /me (@) ส่งคอนแทค
- /mid (@) ส่ง Mid
- /ping เช็ค Ping
- /speed เช็คความเร็ว
- /runtime เช็คเวลาล็อกอิน
- /reject ลบค้างเชิญ
- /say [จำนวน] [ข้อความ] ส่งข้อความ
- /unsend [จำนวน] ยกเลิกข้อความ
- /post [ข้อความ] โพสต์

----------- คำสั่งในกลุ่ม -----------
- /bye [@] เตะ
- /call [จำนวน] เชิญคอล
- /ginfo ข้อมูลกลุ่ม
- /gname (ชื่อกลุ่ม) ดู/เปลี่ยนชื่อกลุ่ม
- /gid ขอ ID กลุ่ม
- /gcreator ดูผู้สร้างกลุ่ม
- /gctime เวลาที่สร้างกลุ่ม
- /gurl ขอ URL กลุ่ม
- /url ตรวจสอบ URL
- /toggleurl เปิด/ปิด URL
- /stag [จำนวน] [@] สแปมแท็ก
- /tagall แท็กสมาชิกทั้งหมด
- /reader ดูบัญชีที่อ่านข้อความ

----------- คำสั่งพิเศษ -----------
- /hypnotize [@] [ข้อความ] สะกดจิต
- /news ข่าวใหม่
- /youtube [ข้อความ] ค้นหา

----------- Keyword -----------
- /keyadd [คีย์เวิร์ด];;[ตอบกลับ] เพิ่มคีย์เวิร์ด
- /keydel [คีย์เวิร์ด] ลบคีย์เวิร์ด
- /keyreset ลบการตอบกลับอัตโนมัติทั้งหมด
- /keylist ดูการตอบกลับออัตโนมัติทั้งหมด

----------- คำสั่งตั้งค่า -----------
- /block on/off เปิด/ปิด บล็อกอัตโนมิัิ
- /pcall on/off เปิด/ปิด ป้องกันสแปมคอล
- /autoread on/off เปิด/ปิด อ่านอัตโนมัติ
- /detail on/off เปิด/ปิด แสดงรายละเอียดบัญชี
- /greet [[ข้อความ]/off] ข้อความทักทายเพื่อนใหม่
- /tag [[ข้อความ]/off] ข้อความตอบกลับเมื่อคนแท็ก
- /wc [[ข้อความ]/off] สมาชิกเข้า
- /lv [[ข้อความ]/off] สมาชิกออก

----------- บัญชี -----------
- /ban (@) เพิ่มบัญชีดำ
- /unban (@) ลบบัญชีดำ
- /cancel ยกเลิกเพิ่ม/ลบบัญชีดำ
- /clearban ล้างบัญชีดำ
- /kickban เตะบัญชีดำ
- /banlist ดูบัญชีดำทั้งหมด
- /conban ส่งคอนแทคบัญชีดำ

----------- ระบบป้องกัน -----------
* ป้องกันแยกกลุ่ม
- /pkick on/off เปิด/ปิด ป้องกันเตะ
- /pinv on/off เปิด/ปิด ป้องกันเชิญ
- /pset ตรวจสอบการป้องกัน

----------- Kicker -----------
- /k:login ล็อกอิน Kicker
- /k:logout Kicker ออกจากระบบ
- /k:inv เชิญ Kicker
- /k:join เรียก Kicker
- /k:leave Kicker ออก
- /k:kick (@) Kicker เตะ

----------- ออกจากระบบ -----------
- /logout ออกจากระบบ"""

kickerHelp2Message = """----------- การตั้งค่า -----------
- [OWNER] {key}:preventkick:on/off เปิด/ปิดป้องกันการเตะ
- [OWNER] {key}:preventinvite:on/off เปิด/ปิดป้องกันการเชิญสมาชิก
- {key}:setting ตรวจสอบการตั้งค่า"""

save = """
- /k:key [prefix] เปลี่ยน Key
- {k}:help ดูคำสั่ง Kicker

- /k:login ล็อกอิน Kicker
- /k:logout Kicker ออกจากระบบ
- /k:invite เชิญ Kicker
- /k:join เรียก Kicker
- /k:leave Kicker ออก

----------- Auto Like -----------
- /autolike on/off เปิด/ปิด ไลค์โพสต์อัตโนมัติ
- /comment [[ข้อความ]/off] คอมเม้น
"""

def mentionMembersX(to, mids=[],result="บัญชีที่อ่านข้อความ\n"):
    parsed_len = len(mids)//20+1
    mention = '@[dionchan]\n'
    no = 0
    for point in range(parsed_len):
        mentionees = []
        for mid in mids[point*20:(point+1)*20]:
            no += 1
            result += '%i. %s' % (no, mention)
            slen = len(result) - 12
            elen = len(result) + 3
            mentionees.append({'S': str(slen), 'E': str(elen - 4), 'M': mid})
        if result:
            if result.endswith('\n'): result = result[:-1]
            client.sendMessage(to, result, {'MENTION': json.dumps({'MENTIONEES': mentionees})}, 0)
        result = ''

def mentionMembers(to, mids=[]):
    if cl in mids: mids.remove(cl)
    parsed_len = len(mids)//20+1
    result = ''
    mention = '@[dionchan]\n'
    no = 0
    for point in range(parsed_len):
        mentionees = []
        for mid in mids[point*20:(point+1)*20]:
            no += 1
            result += '%i. %s' % (no, mention)
            slen = len(result) - 12
            elen = len(result) + 3
            mentionees.append({'S': str(slen), 'E': str(elen - 4), 'M': mid})
        if result:
            if result.endswith('\n'): result = result[:-1]
            client.sendMessage(to, result, {'MENTION': json.dumps({'MENTIONEES': mentionees})}, 0)
        result = ''

def qrLogin(msgEvent, Heads):

    Headers = {
        'User-Agent': "Line/5.8.0",
        'X-Line-Application': "DESKTOPMAC\t5.8.0\tPASUNX-{}\t10.0.0".format(msgEvent._from),
        "x-lal": "ja-US_US",
    }

    Headers.update({'x-lpqs' : '/api/v4/TalkService.do'})

    transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4/TalkService.do')
    transport.setCustomHeaders(Headers)

    protocol = TCompactProtocol.TCompactProtocol(transport)

    clientX = LineService.Client(protocol)

    qr = clientX.getAuthQrcode(keepLoggedIn=1, systemName="PASUNX-OS")

    link = "line://au/q/" + qr.verifier

    client.sendMessage(msgEvent.to, Heads + "\n" +  link)

    Headers.update({"x-lpqs" : '/api/v4/TalkService.do', 'X-Line-Access': qr.verifier})

    json.loads(requests.session().get('https://gd2.line.naver.jp/Q', headers=Headers).text)

    Headers.update({'x-lpqs' : '/api/v4p/rs'})

    transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4p/rs')
    transport.setCustomHeaders(Headers)
    protocol = TCompactProtocol.TCompactProtocol(transport)
    clientX = LineService.Client(protocol)

    req = LoginRequest()
    req.type = 1
    req.verifier = qr.verifier
    req.e2eeVersion = 1

    res = clientX.loginZ(req)
    tm = res.authToken
    time.sleep(1)
    return tm

def botAddF(wA, aT):
    for i in aT:
        wA.findAndAddContactsByMid(i)

def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        client.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        print(error)


def sendMessageCustom(to, text, icon, name):
    khieCool = {
        'MSG_SENDER_ICON': icon,
        'MSG_SENDER_NAME':  name,
    }
    client.sendMessage(to, text, contentMetadata=khieCool)

wait = {"ub":{},"ab":{}}

def dionProcess(msgEvent, op):
    global KR
    global StatusConut
    global StatusUpdate
    global kickerPoll
    global KickerKey
    global KickerLogin
    global dion
    global helper1
    global helper2
    global helper3
    global cl
    global h1
    global h2
    global h3
    global dionMID
    global startTime
    global KR
    try:
        if msgEvent.text == None:
            return
        if msgEvent.text in ["/pset","/news","/gname","/clearban","/kickban","/ban","/unban","/k:join","/k:logout","/k:login","/me","/speed","/mid","/url","/geturl","/toggleurl","/logout","/tagall","/ginfo","/gname"]:
            f=codecs.open(cl+'.json','w','utf-8')
            json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)
        if msgEvent.contentType == 13:
            if msgEvent.to in wait["ab"]:
                if msgEvent.contentMetadata["mid"] in dion["blacklist"]:
                    client.sendMessage(msgEvent.to,"ผู้ใช้นี้อยู่ในบัญชีดำอยู่แล้ว")
                    del wait["ab"][msgEvent.to]
                else:
                    dion["blacklist"][msgEvent.contentMetadata["mid"]] = True
                    del wait["ab"][msgEvent.to]
                    client.sendMessage(msgEvent.to,"เพิ่มผู้ใช้นี้เข้าบัญชีดำแล้ว")
                    f=codecs.open(cl+'.json','w','utf-8')
                    json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)
            if msgEvent.to in wait["ub"]:
                if msgEvent.contentMetadata["mid"] not in dion["blacklist"]:
                    client.sendMessage(msgEvent.to,"ผู้ใช้นี้ไม่ได้อยู่ในบัญชีดำ")
                    del wait["ub"][msgEvent.to]
                else:
                    del dion["blacklist"][msgEvent.contentMetadata["mid"]]
                    del wait["ub"][msgEvent.to]
                    client.sendMessage(msgEvent.to,"ลบผู้ใช้นี้ออกจากบัญชีดำเรียบร้อยแล้ว")
                    f=codecs.open(cl+'.json','w','utf-8')
                    json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)
        if msgEvent.text == None:
            return
        while msgEvent.text.startswith(" ") or msgEvent.text.startswith("\n"):
            msgEvent.text = msgEvent.text[1:]
        while msgEvent.text.endswith(" ") or msgEvent.text.endswith("\n"):
            msgEvent.text = msgEvent.text[:-1]
        if msgEvent.text.lower().startswith("/post"):
            cmd = msgEvent.text.split(" ")
            textToPost = msgEvent.text.replace(cmd[0] + " ","")
            if cmd[0].lower() == "/post":
                post = client.createPost(textToPost)
                if post["message"] == "success":
                    client.sendMessage(msgEvent.to, "โพสต์ข้อความว่า '"+textToPost+"' แล้ว")
                    client.sendMessage(msgEvent.to, "https://line.me/R/home/post?userMid={}&postId={}".format(post["result"]["feed"]["post"]["userInfo"]["mid"],post["result"]["feed"]["post"]["postInfo"]["postId"]))
                else:
                    client.sendMessage(msgEvent.to, "โพสต์ไม่สำเร็จ")
        elif msgEvent.text.lower().startswith("/keyadd"):
            if "kw" not in dion:
                dion["kw"] = {}
            toD = msgEvent.text.split(" ")
            kwD = msgEvent.text.replace(toD[0] + " ","").split(";;")
            if toD[0].lower() == "/keyadd":
                dion["kw"][kwD[0]] = kwD[1]
                client.sendMessage(msgEvent.to, "ตั้งคีย์เวิร์ด '"+kwD[0]+"'เรียบร้อยแล้ว")
            f=codecs.open(cl+'.json','w','utf-8')
            json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)
        elif msgEvent.text.lower().startswith("/keydel"):
            if "kw" not in dion:
                dion["kw"] = {}
            if dion["kw"] == {}:
                return client.sendMessage(msgEvent.to, "ไม่มีคีย์เวิร์ดที่ตั้งไว้")
            toD = msgEvent.text.split(" ")
            kwD = msgEvent.text.replace(toD[0] + " ","")
            if toD[0].lower() == "/keydel":
                if kwD in dion["kw"]:
                    del dion["kw"][kwD]
                    client.sendMessage(msgEvent.to, "ลบคีย์เวิร์ด '"+kwD+"' เรียบร้อยแล้ว")
                else:
                    client.sendMessage(msgEvent.to, "ไม่พบคีย์เวิร์ดที่จะลบ")
            f=codecs.open(cl+'.json','w','utf-8')
            json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)
        elif msgEvent.text.lower() == "/keylist":
            if "kw" not in dion:
                dion["kw"] = {}
            if dion["kw"] == {}:
                return client.sendMessage(msgEvent.to, "ไม่มีคีย์เวิร์ดที่ตั้งไว้")
            else:
                txt = "คียเวิร์ดทั้งหมด"
                for x in dion["kw"]:
                    txt += "\n" + x + "\n" + dion["kw"][x] + "\n"
                client.sendMessage(msgEvent.to, txt)
            f=codecs.open(cl+'.json','w','utf-8')
            json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)
        elif msgEvent.text.lower() == "/keyreset":
            dion["kw"] = {}
            client.sendMessage(msgEvent.to, "รีเซ็ทคีย์ทั้งหมดเรียบร้อยแล้ว")
            f=codecs.open(cl+'.json','w','utf-8')
            json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)
        elif msgEvent.text.lower() == "/gcreator":
            if msgEvent.toType != 2: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            group = client.getCompactGroup(msgEvent.to)
            try:
                ccreator = group.creator.mid
                gcreator = group.creator.displayName
            except:
                ccreator = None
                gcreator = 'ไม่พบผู้สร้างกลุ่ม'
            if ccreator == None:
                return client.sendMessage(msgEvent.to, "ไม่พบผู้สร้างกลุ่ม")
            client.sendContact(msgEvent.to, ccreator)
        elif msgEvent.text.lower() == "/gctime":
            if msgEvent.toType != 2: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            group = client.getCompactGroup(msgEvent.to)
            created = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(int(group.createdTime) / 1000))
            client.sendMessage(msgEvent.to, "เวลาสร้างกลุ่ม:\n"+created)
        elif msgEvent.text.lower() == "/gid":
            if msgEvent.toType != 2: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            client.sendMessage(msgEvent.to, msgEvent.to)
        elif msgEvent.text.lower().startswith("/k:kick"):
            if msgEvent.toType != 2: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            if KickerLogin == False: return client.sendMessage(msgEvent.to, 'Kicker ยังไม่ได้ล็อกอิน')
            group = client.getGroup(msgEvent.to)
            groupMemberMids = [i.mid for i in group.members if i.mid in dionMID]
            key = eval(msgEvent.contentMetadata["MENTION"])
            tMid = [i["M"] for i in key["MENTIONEES"]]
            for i in tMid:
                if h1 in groupMemberMids:
                    try:
                        helper1.kickoutFromGroup(msgEvent.to, [i])
                    except:
                        groupMemberMids.remove(h1)
                elif h2 in groupMemberMids:
                    try:
                        helper2.kickoutFromGroup(msgEvent.to, [i])
                    except:
                        groupMemberMids.remove(h2)
                elif h3 in groupMemberMids:
                    try:
                        helper3.kickoutFromGroup(msgEvent.to, [i])
                    except:
                        groupMemberMids.remove(h3)
        elif msgEvent.text.lower() == "/k:inv":
            if msgEvent.toType != 2: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            if KickerLogin == False: return client.sendMessage(msgEvent.to, 'Kicker ยังไม่ได้ล็อกอิน')
            group = client.getGroup(msgEvent.to)
            groupMemberMids = [i.mid for i in group.members if i.mid in dionMID]
            notInGroup = []
            if h1 not in groupMemberMids:
                notInGroup.append(h1)
            if h2 not in groupMemberMids:
                notInGroup.append(h2)
            if h3 not in groupMemberMids:
                notInGroup.append(h3)
            if notInGroup != []:
                client.inviteIntoGroup(msgEvent.to, notInGroup)
            else:
                return client.sendMessage(msgEvent.to, "Kicker อยู่ในกลุ่มอยู่แล้ว")
            if h1 not in groupMemberMids:
                helper1.acceptGroupInvitation(msgEvent.to)
            if h2 not in groupMemberMids:
                helper2.acceptGroupInvitation(msgEvent.to)
            if h3 not in groupMemberMids:
                helper3.acceptGroupInvitation(msgEvent.to)
        elif msgEvent.text.lower() == "/k:logout":
            if KickerLogin == False: return client.sendMessage(msgEvent.to, "Kicker ยังไม่ได้ล็อกอิน")
            helper1 = None
            helper2 = None
            helper3 = None
            dionMID = [cl]
            KickerLogin = False
            KR = None
            client.sendMessage(msgEvent.to, "Kicker ออกจากระบบเรียบร้อยแล้ว")
        elif msgEvent.text.lower() == "/k:join":
            if msgEvent.toType != 2: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            if KickerLogin == False: return client.sendMessage(msgEvent.to, 'Kicker ยังไม่ได้ล็อกอิน')
            group = client.getGroup(msgEvent.to)
            groupMemberMids = [i.mid for i in group.members if i.mid in dionMID]
            iSet = False
            if groupMemberMids == []:
                return client.sendMessage(msgEvent.to, "Kicker อยู่ในกลุ่มอยู่แล้ว")
            if group.preventedJoinByTicket == True:
                iSet = True
                group.preventedJoinByTicket = False
                client.updateGroup(group)
            Ticket = client.reissueGroupTicket(group.id)
            if h1 not in groupMemberMids:
                helper1.acceptGroupInvitationByTicket(msgEvent.to, Ticket)
            if h2 not in groupMemberMids:
                helper2.acceptGroupInvitationByTicket(msgEvent.to, Ticket)
            if h3 not in groupMemberMids:
                helper3.acceptGroupInvitationByTicket(msgEvent.to, Ticket)
            if iSet == True:
                group.preventedJoinByTicket = True
                client.updateGroup(group)

        elif msgEvent.text.lower() == "/k:leave":
            if msgEvent.toType != 2: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            if KickerLogin == False: return client.sendMessage(msgEvent.to, 'Kicker ยังไม่ได้ล็อกอิน')
            group = client.getGroup(msgEvent.to)
            groupMemberMids = [i.mid for i in group.members if i.mid in dionMID]
            if h1 in groupMemberMids:
                helper1.leaveGroup(group.id)
            if h2 in groupMemberMids:
                helper2.leaveGroup(group.id)
            if h3 in groupMemberMids:
                helper3.leaveGroup(group.id)
        elif msgEvent.text.lower() == "/k:login":
            if KickerLogin == True:
                try:
                    prof = helper1.getProfile()
                except:
                    KickerLogin = False
                try:
                    prof = helper2.getProfile()
                except:
                    KickerLogin = False
                try:
                    prof = helper3.getProfile()
                except:
                    KickerLogin = False
            if KickerLogin == True: return client.sendMessage(msgEvent.to, "Kicker ล็อกอินเรียบร้อยแล้ว")
            if helper1 == None:
                tokenn = qrLogin(msgEvent, "ล็อกอิน KICKER [1/3]:")
                dion["kicker"]["1"] = tokenn
                time.sleep(2)
                helper1 = LINE(tokenn, appName=APP)
                h1 = helper1.profile.mid
                print("[LOGIN] " + client.profile.displayName + " KICKER [1/3]")
            if helper2 == None:
                tokenn = qrLogin(msgEvent, "ล็อกอิน KICKER [2/3]:")
                dion["kicker"]["2"] = tokenn
                time.sleep(2)
                helper2 = LINE(tokenn, appName=APP)
                h2 = helper2.profile.mid
                print("[LOGIN] " + client.profile.displayName + " KICKER [2/3]")
            if helper3 == None:
                tokenn = qrLogin(msgEvent, "ล็อกอิน KICKER [3/3]:")
                dion["kicker"]["3"] = tokenn
                time.sleep(2)
                helper3 = LINE(tokenn, appName=APP)
                h3 = helper3.profile.mid
                print("[LOGIN] " + client.profile.displayName + " KICKER [3/3]")
            f=codecs.open(cl+'.json','w','utf-8')
            json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)
            dionMID = [cl,h1,h2,h3]
            dionMIDWithOutCL = [h1,h2,h3]
            KickerLogin = True
            client.sendMessage(msgEvent.to, "Kicker ล็อกอินเรียบร้อยแล้ว")
        elif msgEvent.text.lower()  == "/conban":
            if dion["blacklist"] == {}:
                return client.sendMessage(msgEvent.to,'ไม่มีบัญชีดำ')
            for i in dion["blacklist"]:
                client.sendContact(msgEvent.to, i)
        if msgEvent.text.lower()  == "/clearban":
            if dion["blacklist"] == {}:
                return client.sendMessage(msgEvent.to,'ไม่มีบัญชีดำ')
            dion["blacklist"] = {}
            client.sendMessage(msgEvent.to,'ล้างบัญชีดำเรียบร้อยแล้ว')
        elif msgEvent.text.lower() == "/cancel":
            if wait["ub"][msgEvent.to] == True:
                client.sendMessage(msgEvent.to, "ยกเลิกปลดแบนเรียบร้อยแล้ว")
                del wait["ub"][msgEvent.to]
            if wait["ab"][msgEvent.to] == True:
                del wait["ab"][msgEvent.to]
                client.sendMessage(msgEvent.to, "ยกเลิกแบนเรียบร้อยแล้ว")
        elif msgEvent.text.lower() == "/unban":
            if msgEvent.to in wait["ab"]:
                del wait["ab"][msgEvent.to]
            wait["ub"][msgEvent.to] = True
            client.sendMessage(msgEvent.to, "ส่งคอนแทคเพื่อปลดแบน\nพิมพ์ '/cancel' เพื่อยกเลิกปลดแบน")
        elif msgEvent.text.lower() == "/ban":
            if msgEvent.to in wait["ub"]:
                del wait["ub"][msgEvent.to]
            wait["ab"][msgEvent.to] = True
            client.sendMessage(msgEvent.to, "ส่งคอนแทคเพื่อแบน\nพิมพ์ '/cancel' เพื่อยกเลิกแบน")
        elif msgEvent.text.lower() == "/banlist":
            if dion["blacklist"] == {}:
                return client.sendMessage(msgEvent.to,'ไม่มีบัญชีดำ')
            txt="บัญชีที่อยู่ในบัญชีดำ:"
            a = 0
            for i in dion["blacklist"]:
                a = a + 1
                txt+="\n- {}. ".format(str(a)) + client.getContact(i).displayName
            client.sendMessage(msgEvent.to, txt)
        elif msgEvent.text.lower().startswith("/unban"):
            key = eval(msgEvent.contentMetadata["MENTION"])
            tMid = [i["M"] for i in key["MENTIONEES"]]
            for i in tMid:
                if i in dion["blacklist"]:
                    del dion["blacklist"][i]
                    client.sendMessage(msgEvent.to, "ลบ " + client.getContact(i).displayName + " ออกจากบัญชีดำเรียบร้อยแล้ว")
                else:
                    client.sendMessage(msgEvent.to, "" + client.getContact(i).displayName + " ไม่ได้อยู่ในบัญชีดำ")
        elif msgEvent.text.lower().startswith("/ban"):
            key = eval(msgEvent.contentMetadata["MENTION"])
            tMid = [i["M"] for i in key["MENTIONEES"]]
            for i in tMid:
                if i not in dion["blacklist"]:
                    dion["blacklist"][i] = True
                    client.sendMessage(msgEvent.to, "เพิ่ม " + client.getContact(i).displayName + " เข้าบัญชีดำเรียบร้อยแล้ว")
                else:
                    client.sendMessage(msgEvent.to, "" + client.getContact(i).displayName + " อยู่ในบัญชีดำอยู่แล้ว")
        elif msgEvent.text.lower()  == "/kickban":
            if msgEvent.toType != 2: return client.sendMessage(msgEvent.to, "คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น")
            if dion["blacklist"] == {}:
                return client.sendMessage(msgEvent.to,'ไม่มีบัญชีดำ')
            group = client.getGroup(msgEvent.to)
            banInG = [i.mid for i in group.members if i.mid in dion["blacklist"]]
            if banInG == []:
                return client.sendMessage(msgEvent.to,'ไม่มีบัญชีดำในกลุ่มนี้')
            for i in banInG:
                client.kickoutFromGroup(msgEvent.to, [i])
        elif msgEvent.text.lower().startswith("/say"):
            spl = msgEvent.text.split(" ")
            try:
                amount = spl[1]
            except:
                return client.sendMessage(msgEvent.to,'วิธีการใช้งาน:\n/say [จำวนวน] [ข้อความ]')
            if amount.isdigit():
                amount = int(amount)
            else:
                return client.sendMessage(msgEvent.to,'วิธีการใช้งาน:\n/say [จำวนวน] [ข้อความ]')
            hMsg = msgEvent.text.replace(spl[0] + " " + str(amount) + " ", "")
            if len(hMsg.split(" ")) == 2:
                return client.sendMessage(msgEvent.to,'วิธีการใช้งาน:\n/say [จำวนวน] [ข้อความ]')
            for i in range(amount):
                client.sendMessage(msgEvent.to, hMsg)
        elif msgEvent.text.lower() == '/tagall':
            members = []
            if msgEvent.toType == 1:
                room = client.getCompactRoom(msgEvent.to)
                members = [member.mid for member in room.members]
            elif msgEvent.toType == 2:
                group = client.getCompactGroup(msgEvent.to)
                members = [member.mid for member in group.members]
            else:
                return client.sendMessage(msgEvent.to, "คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น")
            if members:
                mentionMembers(msgEvent.to, members)
        elif msgEvent.text.lower().startswith("X/comment"):
            seto = msgEvent.text.split(" ")
            setTo = msgEvent.text.replace(seto[0] + " ","")
            dion["comment"] = setTo
            if setTo != "off":
                client.sendMessage(msgEvent.to, "คอมเม้นของคุณคือ '" + setTo + "'")
            else:
                client.sendMessage(msgEvent.to, "ปิดแล้ว")
            f=codecs.open(cl+'.json','w','utf-8')
            json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)
        elif msgEvent.text.lower() == "X/comment":
            ia = ""
            if "comment" in dion:
                if dion["comment"] != "off":
                    ia = "คอมเม้นของคุณคือ '" + dion["comment"] + "'\n\n"
            client.sendMessage(msgEvent.to, ia+"วิธีใช้งาน\n/comment AUTOLIKE\n\nใส่ off เพื่อปิด")
        elif msgEvent.text.lower() == "/tag":
            ia = ""
            if "detectMention" in dion:
                if dion["detectMention"] != "off":
                    ia = "ข้อความแท็กของคุณคือ '" + dion["detectMention"] + "'\n\n"
            client.sendMessage(msgEvent.to, ia+"วิธีใช้งาน\n/tag แท็กทำไม?{name}{tag}\n\n* {tag} หมายถึงแท็กกลับ\n* {name} หมายถึงชื่อคนแท็ก\nใส่ off เพื่อปิด")
        elif msgEvent.text.lower() == "/greet":
            ia = ""
            if "greet" in dion:
                if dion["greet"] != "off":
                    ia = "ข้อความทักทายเพื่อนใหม่ของคุณคือ '" + dion["welcome"] + "'\n\n"
            client.sendMessage(msgEvent.to, ia+"วิธีใช้งาน\n/greet สวัสดี {name}\n\n* {name} หมายถึง ชื่อคนที่แอด\n* {contact} หมายถึง คอนแทคที่คนที่แอด\nใส่ off เพื่อปิด")
        elif msgEvent.text.lower() == "/wc":
            ia = ""
            if "welcome" in dion:
                if dion["welcome"] != "off":
                    ia = "ข้อความสมาชิกเข้าของคุณคือ '" + dion["welcome"] + "'\n\n"
            client.sendMessage(msgEvent.to, ia+"วิธีใช้งาน\n/wc ยินดีต้อนรับ {name} เข้าสู่กลุ่ม {gname}{contact}\n\n* {gname} หมายถึง กลุ่ม\n* {name} หมายถึงชื่อสมาชิก\n* {contact} หมายถึง Contact สมาชิก\nใส่ off เพื่อปิด")
        elif msgEvent.text.lower() == "/lv":
            ia = ""
            if "leave" in dion:
                if dion["leave"] != "off":
                    ia = "ข้อความสมาชิกออกของคุณคือ '" + dion["leave"] + "'\n\n"
            client.sendMessage(msgEvent.to, ia+"วิธีใช้งาน\n/lv {name} ได้ออกจากลุ่ม {gname} แล้ว{contact}\n\n* {gname} หมายถึง กลุ่ม\n* {name} หมายถึงชื่อสมาชิก\n* {contact} หมายถึง Contact สมาชิก\nใส่ off เพื่อปิด")
        elif msgEvent.text.lower().startswith("/bye"):
            if msgEvent.toType == 2:
                group = client.getGroup(msgEvent.to)
                key = eval(msgEvent.contentMetadata["MENTION"])
                tMid = [i["M"] for i in key["MENTIONEES"]]
                for i in tMid:
                    client.kickoutFromGroup(msgEvent.to, [i])
            else:
                client.sendMessage(msgEvent.to, "คำสั่งนี้ใช้ได้เฉพาะในกลุ่ม")
        elif msgEvent.text.lower().startswith("/greet"):
            seto = msgEvent.text.split(" ")
            setTo = msgEvent.text.replace(seto[0] + " ","")
            dion["greet"] = setTo
            if setTo != "off":
                client.sendMessage(msgEvent.to, "ตั้งข้อความทักทายเพื่อนใหม่ว่า '" + setTo + "'")
            else:
                client.sendMessage(msgEvent.to, "ปิดแล้ว")
            f=codecs.open(cl+'.json','w','utf-8')
            json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)
        elif msgEvent.text.lower().startswith("/wc"):
            seto = msgEvent.text.split(" ")
            setTo = msgEvent.text.replace(seto[0] + " ","")
            dion["welcome"] = setTo
            if setTo != "off":
                client.sendMessage(msgEvent.to, "ตั้งข้อความเมื่อมีสมาชิกเข้าว่า '" + setTo + "'")
            else:
                client.sendMessage(msgEvent.to, "ปิดแล้ว")
            f=codecs.open(cl+'.json','w','utf-8')
            json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)

        elif msgEvent.text.lower().startswith("/lv"):
            seto = msgEvent.text.split(" ")
            setTo = msgEvent.text.replace(seto[0] + " ","")
            dion["leave"] = setTo
            if setTo != "off":
                client.sendMessage(msgEvent.to, "ตั้งข้อความเมื่อมีสมาชิกออกว่า '" + setTo + "'")
            else:
                client.sendMessage(msgEvent.to, "ปิดแล้ว")
            f=codecs.open(cl+'.json','w','utf-8')
            json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)

        elif msgEvent.text.lower().startswith("/tag"):
            seto = msgEvent.text.split(" ")
            setTo = msgEvent.text.replace(seto[0] + " ","")
            dion["detectMention"] = setTo
            if setTo != "off":
                client.sendMessage(msgEvent.to, "ตั้งข้อความเมื่อมีคนแท็กว่า '" + setTo + "'")
            else:
                client.sendMessage(msgEvent.to, "ปิดแล้ว")
            f=codecs.open(cl+'.json','w','utf-8')
            json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)

        elif msgEvent.text.lower().startswith("/unsend"):
            try:
                iWant = msgEvent.text.split(" ")[1]
            except:
                return client.sendMessage(msgEvent.to, 'วิธีการใช้งาน\n/unsend [จำนวน]')
            if iWant.isdigit():
                amount = int(iWant)
            else:
                return client.sendMessage(msgEvent.to, 'วิธีการใช้งาน\n/unsend [จำนวน]')
            nowGet = 0
            M = client.getRecentMessagesV2(msgEvent.to, amount)
            MsgID = []
            for x, i in enumerate(M):
                if x != 0:
                    if i._from == cl:
                        MsgID.append(i.id)
                        if len(MsgID) == amount:
                            break
            IDS = 0
            for i in MsgID:
                try:
                    client.unsendMessage(i)
                    IDS = IDS + 1
                except:
                    continue
            client.sendMessage(msgEvent.to, "ยกเลิก {} ข้อความเรียบร้อยแล้ว".format(IDS))
        elif msgEvent.text.lower() == "/reader":
            if msgEvent.toType == 0: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            try:
                if msgEvent.to not in ReaderChecker["readRom"]:
                    ReaderChecker["readRom"][msgEvent.to] = {}
                ReaderMid = [i for i in ReaderChecker["readRom"][msgEvent.to]]
                if ReaderMid != []:
                    mentionMembersX(msgEvent.to, ReaderMid)
                else:
                    client.sendMessage(msgEvent.to, 'ไม่มีบัญชีที่อ่านข้อความตอนนี้')
            except Exception as E:
                print(E)
        elif msgEvent.text.lower() == "/reject":
            client.sendMessage(msgEvent.to, "กรุณารอสักครู่")
            groupIdsInvited = client.getGroupIdsInvited()
            for groupIds in groupIdsInvited:
                client.acceptGroupInvitation(groupIds)
                time.sleep(0.9)
                client.leaveGroup(groupIds)
                time.sleep(0.9)
            client.sendMessage(msgEvent.to, "ลบค้างเชิญเรียบร้อยแล้ว")

        elif msgEvent.text.lower().startswith("/youtube"):
            separate = msgEvent.text.split(" ")
            search = msgEvent.text.replace(separate[0] + " ","")
            url = requests.get("http://api.w3hills.com/youtube/search?keyword={}&api_key=86A7FCF3-6CAF-DEB9-E214-B74BDB835B5B".format(search))
            data = url.json()
            no = 0
            result = "ยูทูป " + search + ""
            for anu in data["videos"]:
                no += 1
                result += "\n\n{}. {}\n{}".format(str(no),str(anu["title"]),str(anu["webpage"]))
            client.sendMessage(msgEvent.to, result)
        elif msgEvent.text.lower() == "/news":
            try:
                country = "th"
                user_agent = {'User-agent': 'Mozilla/5.0'}
                url = requests.get("https://newsapi.org/v2/top-headlines?country={}&apiKey=763b6fc67a594a4e9e0f9d29303f83dd".format(country))
                data = url.json()
                result="ข่าวใหม่"
                n = 0
                for anu in data["articles"]:
                    if len(result) > 1500:
                        client.sendMessage(msgEvent.to, result)
                        return
                    else:
                        n = n + 1
                        result+="\n\n" + anu["title"] + "\n"+anu["url"]
                client.sendMessage(msgEvent.to, result)
            except Exception as Error:
                print(Error)
                client.sendMessage(msgEvent.to, "ERROR")
        elif msgEvent.text.lower().startswith("/urljson"):
            try:
                separate = msgEvent.text.split(" ")
                text = msgEvent.text.replace(separate[0] + " ","")
                r = requests.get(text)
                data = r.text
                myarf = json.loads(data)
                fn2 = json.dumps(myarf, sort_keys=True, indent=4)
                k = len(fn2)//10000
                for fn1 in range(k+1):
                    client.sendMessage(msgEvent.to,'{}'.format(fn2[fn1*10000 : (fn1+1)*10000]))
            except:
                client.sendMessage(msgEvent.to, "ERROR")
        elif msgEvent.text.lower() == "/runtime":
            totalTime = time.time() - startTime
            mins, secs = divmod(totalTime,60)
            hours, mins = divmod(mins,60)
            days, hours = divmod(hours, 24)
            resTime = "%02d วัน %02d ชั่วโมง %02d นาที %02d วินาที" % (days, hours, mins, secs)
            #resTime = format_timespan(totalTime)
            client.sendMessage(msgEvent.to, resTime)
        elif msgEvent.text.lower() == "/pset":
            if msgEvent.toType == 0: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            if "pinv" not in dion:
                dion["pinv"] = {}
            if "pkick" not in dion:
                dion["pkick"] = {}
            rt = "การป้องกันของกลุ่มนี้"
            if msgEvent.to in dion["pinv"]: rt += "\nป้องกันเชิญ: เปิด"
            else: rt += "\nป้องกันเชิญ: ปิด"
            if msgEvent.to in dion["pkick"]: rt += "\nป้องกันเตะ: เปิด"
            else: rt += "\nป้องกันเตะ: ปิด"
            client.sendMessage(msgEvent.to, rt)
        elif msgEvent.text.lower().startswith("/pinv"):
            if msgEvent.toType == 0: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            if "pinv" not in dion:
                dion["pinv"] = {}
            try:
                sT = msgEvent.text.lower().split(" ")[1]
            except:
                if msgEvent.to in dion["pinv"]:
                    client.sendMessage(msgEvent.to, "ป้องกันเตะเปิดอยู่\n\n/pkick off เพื่อปิด")
                else:
                    client.sendMessage(msgEvent.to, "ป้องกันเตะปิดอยู่\n\n/pkick on เพื่อเปิด")
                return
            if sT == "on":
                if msgEvent.to in dion["pinv"]:
                    client.sendMessage(msgEvent.to, "เปิดอยู่แล้ว")
                else:
                    dion["pinv"][msgEvent.to] = True
                    client.sendMessage(msgEvent.to, "เปิดแล้ว")
            elif sT == "off":
                if msgEvent.to not in dion["pinv"]:
                    client.sendMessage(msgEvent.to, "ปิดอยู่แล้ว")
                else:
                    del dion["pinv"][msgEvent.to]
                    client.sendMessage(msgEvent.to, "ปิดแล้ว")
            else:
                client.sendMessage(msgEvent.to, "ไม่พบคำสั่ง")
        elif msgEvent.text.lower().startswith("/pkick"):
            if msgEvent.toType == 0: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            if "pkick" not in dion:
                dion["pkick"] = {}
            try:
                sT = msgEvent.text.lower().split(" ")[1]
            except:
                if msgEvent.to in dion["pkick"]:
                    client.sendMessage(msgEvent.to, "ป้องกันเตะเปิดอยู่\n\n/pkick off เพื่อปิด")
                else:
                    client.sendMessage(msgEvent.to, "ป้องกันเตะปิดอยู่\n\n/pkick oon เพื่อเปิด")
                return
            if sT == "on":
                if msgEvent.to in dion["pkick"]:
                    client.sendMessage(msgEvent.to, "เปิดอยู่แล้ว")
                else:
                    dion["pkick"][msgEvent.to] = True
                    client.sendMessage(msgEvent.to, "เปิดแล้ว")
            elif sT == "off":
                if msgEvent.to not in dion["pkick"]:
                    client.sendMessage(msgEvent.to, "ปิดอยู่แล้ว")
                else:
                    del dion["pkick"][msgEvent.to]
                    client.sendMessage(msgEvent.to, "ปิดแล้ว")
            else:
                client.sendMessage(msgEvent.to, "ไม่พบคำสั่ง")
        elif msgEvent.text.lower().startswith("/pcall"):
            if "pcall" not in dion:
                dion["pcall"] = False
            try:
                sT = msgEvent.text.lower().split(" ")[1]
            except:
                if dion["pcall"] == False:
                    client.sendMessage(msgEvent.to, "ป้องกันสแปมคอลปิดอยู่\n\n/pcall on เพื่อเปิด")
                else:
                    client.sendMessage(msgEvent.to, "ป้องกันสแปมคอลเปิดอยู่\n\n/pcall off เพื่อปิด")
                return
            if sT == "on":
                if dion["pcall"] == True:
                    client.sendMessage(msgEvent.to, "เปิดอยู่แล้ว")
                else:
                    dion["pcall"] = True
                    client.sendMessage(msgEvent.to, "เปิดแล้ว")
            elif sT == "off":
                if dion["pcall"] == False:
                    client.sendMessage(msgEvent.to, "ปิดอยู่แล้ว")
                else:
                    dion["pcall"] = False
                    client.sendMessage(msgEvent.to, "ปิดแล้ว")
            else:
                client.sendMessage(msgEvent.to, "ไม่พบคำสั่ง")
        elif msgEvent.text.lower().startswith("X/autolike"):
            if "autolike" not in dion:
                dion["autolike"] = False
            try:
                sT = msgEvent.text.lower().split(" ")[1]
            except:
                if dion["autolike"] == False:
                    client.sendMessage(msgEvent.to, "ไลค์อัตโนมัติปิดอยู่\n\n/autolike on เพื่อเปิด")
                else:
                    client.sendMessage(msgEvent.to, "ไลค์อัตโนมัติเปิดอยู่\n\n/autolike off เพื่อปิด")
                return
            if sT == "on":
                if dion["autolike"] == True:
                    client.sendMessage(msgEvent.to, "เปิดอยู่แล้ว")
                else:
                    dion["autolike"] = True
                    client.sendMessage(msgEvent.to, "เปิดแล้ว")
            elif sT == "off":
                if dion["autolike"] == False:
                    client.sendMessage(msgEvent.to, "ปิดอยู่แล้ว")
                else:
                    dion["autolike"] = False
                    client.sendMessage(msgEvent.to, "ปิดแล้ว")
            else:
                client.sendMessage(msgEvent.to, "ไม่พบคำสั่ง")
        elif msgEvent.text.lower().startswith("/autoread"):
            if "autoread" not in dion:
                dion["autoread"] = False
            try:
                sT = msgEvent.text.lower().split(" ")[1]
            except:
                if dion["autoread"] == False:
                    client.sendMessage(msgEvent.to, "อ่านอัตโนมัติปิดอยู่\n\n/autoread on เพื่อเปิด")
                else:
                    client.sendMessage(msgEvent.to, "อ่านอัตโนมัติเปิดอยู่\n\n/autoread off เพื่อปิด")
                return
            if sT == "on":
                if dion["autoread"] == True:
                    client.sendMessage(msgEvent.to, "เปิดอยู่แล้ว")
                else:
                    dion["autoread"] = True
                    client.sendMessage(msgEvent.to, "เปิดแล้ว")
            elif sT == "off":
                if dion["autoread"] == False:
                    client.sendMessage(msgEvent.to, "ปิดอยู่แล้ว")
                else:
                    dion["autoread"] = False
                    client.sendMessage(msgEvent.to, "ปิดแล้ว")
            else:
                client.sendMessage(msgEvent.to, "ไม่พบคำสั่ง")
        elif msgEvent.text.lower().startswith("/block"):
            if "block" not in dion:
                dion["block"] = False
            try:
                sT = msgEvent.text.lower().split(" ")[1]
            except:
                if dion["block"] == False:
                    client.sendMessage(msgEvent.to, "บล็อกอัตโนมัตปิดอยู่\n\n/block on เพื่อเปิด")
                else:
                    client.sendMessage(msgEvent.to, "บล็อกอัตโนมัติเปิดอยู่\n\n/block off เพื่อปิด")
                return
            if sT == "on":
                if dion["block"] == True:
                    client.sendMessage(msgEvent.to, "เปิดอยู่แล้ว")
                else:
                    dion["block"] = True
                    client.sendMessage(msgEvent.to, "เปิดแล้ว")
            elif sT == "off":
                if dion["block"] == False:
                    client.sendMessage(msgEvent.to, "ปิดอยู่แล้ว")
                else:
                    dion["block"] = False
                    client.sendMessage(msgEvent.to, "ปิดแล้ว")
            else:
                client.sendMessage(msgEvent.to, "ไม่พบคำสั่ง")
        elif msgEvent.text.lower().startswith("/hypnotize"):
            if msgEvent.toType == 0: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            try:
                key = eval(msgEvent.contentMetadata["MENTION"])
                tMid = [i["M"] for i in key["MENTIONEES"]]
                tText = msgEvent.text.replace(msgEvent.text.split(" ")[0]+" ", "")
                for i in tMid:
                    tText = tText.replace("@" + client.getContact(i).displayName + " ", "")
                for i in tMid:
                    con = client.getContact(i)
                    pic = "http://dl.profile.line.naver.jp/{}".format(con.pictureStatus)
                    sendMessageCustom(msgEvent.to, tText, pic, con.displayName)
                client.unsendMessage(msgEvent.id)
            except Exception as E:
                print(E)
        elif msgEvent.text.lower().startswith("/gname"):
            if msgEvent.toType != 2: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            group = client.getCompactGroup(msgEvent.to)
            gname = msgEvent.text.split(" ")
            if len(gname) == 1:
                return client.sendMessage(msgEvent.to, group.name)
            gname = msgEvent.text.replace(gname[0] + " ", "")
            if len(gname) > 50:
                return client.sendMessage(msgEvent.to, 'ERROR')
            group.name = gname
            client.updateGroup(group)
            client.sendMessage(msgEvent.to, "เปลี่ยนชื่อกลุ่มเป็น '%s' เรียบร้อยแล้ว" % gname)
        elif msgEvent.text.lower() == '/ginfo':
            if msgEvent.toType != 2: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            group = client.getCompactGroup(msgEvent.to)
            try:
                ccreator = group.creator.mid
                gcreator = group.creator.displayName
            except:
                ccreator = None
                gcreator = 'ไม่พบผู้สร้างกลุ่ม'
            if not group.invitee:
                pendings = 0
            else:
                pendings = len(group.invitee)
            qr = 'ปิด' if group.preventedJoinByTicket else 'เปิด'
            if group.preventedJoinByTicket:
                ticket = 'URL ปิดอยู่'
            else:
                ticket = 'https://line.me/R/ti/g/' + str(client.reissueGroupTicket(group.id))
            created = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(int(group.createdTime) / 1000))
            path = 'http://dl.profile.line-cdn.net/' + group.pictureStatus
            res = ''
            res += 'ชื่อกลุ่ม: ' + group.name
            res += '\nGID: ' + group.id
            res += '\nผู้สร้างกลุ่ม: ' + gcreator
            res += '\nเวลาสร้างกลุ่ม: ' + created
            res += '\nสมาชิกทั้งหมด: ' + str(len(group.members))
            res += '\nค้างเชิญทั้งหมด: ' + str(pendings)
            res += '\nสถานะ URL: ' + qr
            res += '\nURL: ' + ticket
            client.sendMessage(group.id, res)
        elif msgEvent.text.lower().startswith("/stag"):
            if msgEvent.toType == 0: return client.sendMessage(msgEvent.to, 'คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น')
            try:
                key = eval(msgEvent.contentMetadata["MENTION"])
                tMid = [i["M"] for i in key["MENTIONEES"]]
                tRan = msgEvent.text.replace(msgEvent.text.split(" ")[0], "")
                for i in tMid:
                    tRan = tRan.replace(client.getContact(i).displayName, "")
                tRan = tRan.replace("@","")
                tRan = tRan.replace(" ","")
                try:
                    tRan = int(tRan)
                except:
                    tRan = int(msgEvent.text.split(" ")[1])
                for i in range(tRan):
                    client.sendMessageWithMention(msgEvent.to, ":)", tMid)
            except Exception as E:
                print(E)
                client.sendMessage(msgEvent.to, "ERROR")
        elif msgEvent.text.lower().startswith("/rcall"):
            if msgEvent.toType == 1:
                try:
                    process = msgEvent.text.split(" ")[1]
                    process = int(process)
                except:
                    client.sendMessage(msgEvent.to, "วิธีใช้งาน:\n/call [จำนวน]")
                    return
                key = eval(msgEvent.contentMetadata["MENTION"])
                members = [i["M"] for i in key["MENTIONEES"]]
                client.sendMessage(msgEvent.to, "กรุณารอสักครู่")
                if process:
                    client.acquireGroupCallRoute(msgEvent.to)
                    for x in range(process):
                        try:
                            client.inviteIntoGroupCall(msgEvent.to, contactIds=members)
                        except Exception as e:
                            client.sendMessage(msgEvent.to,str(e))
                client.sendMessage(msgEvent.to, "เชิญคอลเรียบร้อยแล้ว".format(str(process)))
            else:
                client.sendMessage(msgEvent.to,"คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น")
        elif msgEvent.text.lower().startswith("/call"):
            if msgEvent.toType == 2:
                try:
                    process = msgEvent.text.split(" ")[1]
                    process = int(process)
                except:
                    client.sendMessage(msgEvent.to, "วิธีใช้งาน:\n/call [จำนวน]")
                    return
                group = client.getGroup(msgEvent.to)
                members = [member.mid for member in group.members]
                client.sendMessage(msgEvent.to, "กรุณารอสักครู่")
                if process <= 1000:
                    client.acquireGroupCallRoute(msgEvent.to)
                    for x in range(process):
                        try:
                            client.inviteIntoGroupCall(msgEvent.to, contactIds=members)
                        except Exception as e:
                            client.sendMessage(msgEvent.to,str(e))
                client.sendMessage(msgEvent.to, "เชิญคอลเรียบร้อยแล้ว".format(str(process)))
            else:
                client.sendMessage(msgEvent.to,"คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น")
        elif msgEvent.text.lower() == "/logout":
            client.sendMessage(msgEvent.to, "กำลังออกจากระบบ...")
            sys.exit(cl)
        elif msgEvent.text.lower() == "/ping":
            startTime = time.time()
            di = client.sendMessage(msgEvent.to, "ping")
            totalTime = str(((time.time() - startTime) - 0.004)*1000)
            if totalTime.startswith("-"):
                totalTime = str(((time.time() - startTime) - 0.003)*1000)
            if totalTime.startswith("-"):
                totalTime = str(((time.time() - startTime)-0.002)*1000)
            totalTime = totalTime.split(".")[0]
            if random.choice([1,2,3,4]) != 1:
                client.sendMessage(msgEvent.to, "Pong! ("+totalTime+" ms)")
                client.unsendMessage(di.id)
            else:
                pass
        elif msgEvent.text.lower() == "/speed":
            startTime = time.time()
            di = client.sendMessage(msgEvent.to, "speed")
            totalTime = str((time.time() - startTime - 0.004))[:7]
            if totalTime.startswith("-"):
                totalTime = str((time.time() - startTime - 0.003))[:7]
            if totalTime.startswith("-"):
                totalTime = str((time.time() - startTime)-0.002)[:7]
            if random.choice([1,2,3,4]) != 1:
                client.sendMessage(msgEvent.to, totalTime+" วินาที")
                client.unsendMessage(di.id)
            else:
                #print(random.choic([1,2,3,4]))
                pass
        elif msgEvent.text.lower() == "/me":
            client.sendContact(msgEvent.to, msgEvent._from)
        elif "/me @" in msgEvent.text.lower():
            if msgEvent.toType != 2:
                client.sendContact(msgEvent.to, msgEvent.to)
                return
            try:
                key = eval(msgEvent.contentMetadata["MENTION"])
                tMid = [i["M"] for i in key["MENTIONEES"]]
                for i in tMid:
                    client.sendContact(msgEvent.to, i)
            except:
                client.sendMessage(msgEvent.to, "ERROR")
        elif msgEvent.text.lower() == "/mid":
            client.sendMessage(msgEvent.to, msgEvent._from)
        elif "/mid @" in msgEvent.text.lower():
            if msgEvent.toType != 2:
                client.sendMessage(msgEvent.to, msgEvent.to)
                return
            try:
                key = eval(msgEvent.contentMetadata["MENTION"])
                tMid = [i["M"] for i in key["MENTIONEES"]]
                for i in tMid:
                    client.sendMessage(msgEvent.to, i)
            except:
                client.sendMessage(msgEvent.to, "ERROR")
        elif msgEvent.text.lower().startswith("/detail"):
            if "detail" not in dion:
                dion["detail"] = True
            try:
                sT = msgEvent.text.lower().split(" ")[1]
            except:
                if dion["detail"] == False:
                    client.sendMessage(msgEvent.to, "รายละเอียดบัญชีปิดอยู่\n\n/detail on เพื่อเปิด")
                else:
                    client.sendMessage(msgEvent.to, "รายละเอียดบัญชีเปิดอยู่\n\n/detail off เพื่อปิด")
                return
            if sT == "on":
                if dion["detail"] == True:
                    client.sendMessage(msgEvent.to, "เปิดอยู่แล้ว")
                else:
                    dion["detail"] = True
                    client.sendMessage(msgEvent.to, "เปิดแล้ว")
            elif sT == "off":
                if dion["detail"] == False:
                    client.sendMessage(msgEvent.to, "ปิดอยู่แล้ว")
                else:
                    dion["detail"] = False
                    client.sendMessage(msgEvent.to, "ปิดแล้ว")
            else:
                client.sendMessage(msgEvent.to, "ไม่พบคำสั่ง")
        elif msgEvent.text.lower() == "/help":
            if "detail" not in dion:
                dion["detail"] = True
            if dion["detail"] == True:
                totalTime = time.time() - startTime
                mins, secs = divmod(totalTime,60)
                hours, mins = divmod(mins,60)
                days, hours = divmod(hours, 24)
                resTime = ""
                if days != 00:
                    resTime += "%2d วัน " % (days)
                if hours != 00:
                    resTime += "%2d ชั่วโมง " % (hours)
                if mins != 00:
                    resTime += "%2d นาที " % (mins)
                resTime += "%2d วินาที" % (secs)
                totalTime = int(ty) - totalTime
                mins, secs = divmod(totalTime,60)
                hours, mins = divmod(mins,60)
                days, hours = divmod(hours, 24)
                mounts, days = divmod(days, 30)
                years, mounts = divmod(mounts, 12)
                res2Time = ""
                if years != 00:
                    res2Time += "%2d ปี " % (mounts)
                if mounts != 00:
                    res2Time += "%2d เดือน " % (mounts)
                if days != 00:
                    res2Time += "%2d วัน " % (days)
                if hours != 00:
                    res2Time += "%2d ชั่วโมง " % (hours)
                if mins != 00:
                    res2Time += "%2d นาที " % (mins)
                res2Time += "%2d วินาที" % (secs)
                detailShow = userDetail.format(bName=client.getProfile().displayName,bRuntime=resTime,tl=res2Time)
                hMsg = selfHelpMessage.format(detail=detailShow)
            else:
                hMsg = selfHelpMessage.format(detail="")
            client.sendMessage(msgEvent.to, hMsg)
        elif msgEvent.text.lower() == "/toggleurl":
            if msgEvent.toType == 2:
                group = client.getGroup(msgEvent.to)
                if group.preventedJoinByTicket == True:
                    group.preventedJoinByTicket = False
                else:
                    group.preventedJoinByTicket = True
                client.updateGroup(group)
            else:
                client.sendMessage(msgEvent.to, "คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น")
        elif msgEvent.text.lower() == "/gurl":
            if msgEvent.toType == 2:
                group = client.getGroup(msgEvent.to)
                if group.preventedJoinByTicket == True:
                    client.sendMessage(group.id, "URL ปิดอยู่")
                    return
                Ticket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(group.id)))
                client.sendMessage(msgEvent.to, Ticket)
            else:
                client.sendMessage(msgEvent.to, "คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น")
        elif msgEvent.text.lower() == "/url":
            if msgEvent.toType == 2:
                group = client.getGroup(msgEvent.to)
                if group.preventedJoinByTicket == True:
                    client.sendMessage(msgEvent.to, "URL ปิดอยู่")
                    return
                client.sendMessage(msgEvent.to, "URL เปิดอยู่")
            else:
                client.sendMessage(msgEvent.to, "คำสั่งนี้ใช้ได้เฉพาะในกลุ่มเท่านั้น")
        ReaderChecker["readRom"][msgEvent.to] = {}
    except Exception as Error:
        print(Error)


def dionMainCore(op):
    global KickerLogin
    global StatusConut
    global StatusUpdate
    try:
        if op.type == 12:
            if KickerLogin == True:
                if h1 in op.param2:
                    helper1.acceptGroupInvitation(op.param1)
                if h2 in op.param2:
                    helper2.acceptGroupInvitation(op.param1)
                if h3 in op.param2:
                    helper3.acceptGroupInvitation(op.param1)
                if cl in op.param2:
                    client.acceptGroupInvitation(op.param1)
        """if op.type == 0:
            if "autolike" not in dion:
                dion["autolike"] = False
            if dion["autolike"] == True:
                a = client.getFeed()
                for i in a["result"]["feeds"]:
                    c = i["post"]["postInfo"]["postId"]
                    d = i["post"]["userInfo"]["mid"]
                    if i["post"]["postInfo"]["liked"] == False:
                        try:
                            x = client.likePost(d,c,1001)
                            print(x)
                            if "comment" in dion:
                                b = client.createComment(d,c,dion["comment"])
                                print(b)
                        except Exception as E:
                            print(E)"""
        if op.type == 5:
            if "block" in dion:
                client.sendMessage(op.param1, "ระบบบล็อกอัตโนมัติเปิดอยู่\nระบบได้บล็อกคุณแล้ว")
                time.sleep(0.7)
                client.blockContact(op.param1)
            elif "greet" in dion:
                if dion["greet"] != "off":
                    try:
                        contact = client.getContact(op.param1)
                        sMsg = dion["greet"]
                        sMsg = sMsg.replace("{name}",contact.displayName)
                        sMsg = sMsg.replace("{contact}","")
                        client.sendMessage(op.param1, sMsg)
                        if "{contact}" in dion["greet"]:
                            client.sendContact(op.param1, contact.mid)
                    except:
                        pass
        if op.type == 13:
            if "pinv" not in dion:
                dion["pinv"] = {}
            if op.param2 in dion["blacklist"] or op.param3 in dion["blacklist"]:
                if KickerLogin == False:
                    try:
                        client.kickoutFromGroup(op.param1, [op.param2])
                    except:
                        pass
                else:
                    try:
                        helper3.kickoutFromGroup(op.param1, [op.param2])
                        helper3.cancelGroupInvitation(op.param1, [op.param3])
                    except:
                        try:
                            helper2.kickoutFromGroup(op.param1, [op.param2])
                            helper2.cancelGroupInvitation(op.param1, [op.param3])
                        except:
                            try:
                                helper1.kickoutFromGroup(op.param1, [op.param2])
                                helper1.cancelGroupInvitation(op.param1, [op.param3])
                            except:
                                pass
            elif op.param1 in dion["pinv"] and op.param2 not in dionMID and op.param3 not in dionMID:
                dion["blacklist"][op.param2] = True
                dion["blacklist"][op.param3] = True
                try:
                    helper3.kickoutFromGroup(op.param1, [op.param2])
                    helper3.cancelGroupInvitation(op.param1, [op.param3])
                except:
                    try:
                        helper2.kickoutFromGroup(op.param1, [op.param2])
                        helper2.cancelGroupInvitation(op.param1, [op.param3])
                    except:
                        try:
                            helper1.kickoutFromGroup(op.param1, [op.param2])
                            helper1.cancelGroupInvitation(op.param1, [op.param3])
                        except:
                            pass
        if op.type == 17:
            if op.param2 in dion["blacklist"]:
                if KickerLogin == False:
                    try:
                        client.kickoutFromGroup(op.param1, [op.param2])
                    except:
                        pass
                else:
                    try:
                        helper3.kickoutFromGroup(op.param1, [op.param2])
                    except:
                        try:
                            helper2.kickoutFromGroup(op.param1, [op.param2])
                        except:
                            try:
                                helper1.kickoutFromGroup(op.param1, [op.param2])
                            except:
                                pass
            elif op.param2 not in dionMID:
                if "welcome" in dion:
                    if dion["welcome"] != "off":
                        try:
                            contact = client.getContact(op.param2)
                            group = client.getGroup(op.param1)
                            sMsg = dion["welcome"]
                            sMsg = sMsg.replace("{name}",contact.displayName)
                            sMsg = sMsg.replace("{contact}","")
                            sMsg = sMsg.replace("{gname}",group.name)
                            client.sendMessage(op.param1, sMsg)
                            if "{contact}" in dion["welcome"]:
                                client.sendContact(op.param1, contact.mid)
                        except:
                            pass
        if op.type == 19:
            if "pkick" not in dion:
                dion["pkick"] = {}
            if op.param1 in dion["pkick"] and op.param2 not in dionMID:
                dion["blacklist"][op.param2] = True
                if KickerLogin == True:
                    try:
                        helper3.kickoutFromGroup(op.param1, [op.param2])
                    except:
                        try:
                            helper2.kickoutFromGroup(op.param1, [op.param2])
                        except:
                            try:
                                helper1.kickoutFromGroup(op.param1, [op.param2])
                            except:
                                pass
                else:
                    client.kickoutFromGroup(op.param1, [op.param2])
            if op.param3 in dionMID and KickerLogin == True:
                dion["blacklist"][op.param2] = True
                if op.param3 in dionMIDWithOutCL and op.param2 not in dionMID:
                    try:
                        group = client.getGroup(op.param1)
                        groupMemberMids = [i.mid for i in group.members if i.mid in dionMID]
                        titanBlackList = [i.mid for i in group.members if i.mid in dion["blacklist"]]
                        notInGroup = []
                        if h3 not in groupMemberMids:
                            notInGroup.append(h3)
                        if h2 not in groupMemberMids:
                            notInGroup.append(h2)
                        if h1 not in groupMemberMids:
                            notInGroup.append(h1)
                        if notInGroup != []:
                            if h1 in groupMemberMids:
                                try:
                                    helper1.inviteIntoGroup(group.id, notInGroup)
                                except:
                                    if h2 in groupMemberMids:
                                        try:
                                            helper2.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            if h3 in groupMemberMids:
                                                try:
                                                    helper3.inviteIntoGroup(group.id, notInGroup)
                                                except:
                                                    pass
                                    elif h3 in groupMemberMids:
                                        try:
                                            helper3.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            pass
                            elif h2 in groupMemberMids:
                                try:
                                    helper2.inviteIntoGroup(group.id, notInGroup)
                                except:
                                    if h1 in groupMemberMids:
                                        try:
                                            helper1.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            if h3 in groupMemberMids:
                                                try:
                                                    helper3.inviteIntoGroup(group.id, notInGroup)
                                                except:
                                                    pass
                                    elif h3 in groupMemberMids:
                                        try:
                                            helper3.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            pass
                            elif h3 in groupMemberMids:
                                try:
                                    helper3.inviteIntoGroup(group.id, notInGroup)
                                except:
                                    if h2 in groupMemberMids:
                                        try:
                                            helper2.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            if h3 in groupMemberMids:
                                                try:
                                                    helper3.inviteIntoGroup(group.id, notInGroup)
                                                except:
                                                    pass
                                    elif h3 in groupMemberMids:
                                        try:
                                            helper3.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            pass
                        for mid in titanBlackList:
                            try:
                                helper3.kickoutFromGroup(op.param1, [mid])
                            except:
                                try:
                                    helper2.kickoutFromGroup(op.param1, [mid])
                                except:
                                    try:
                                        helper1.kickoutFromGroup(op.param1, [mid])
                                    except:
                                        pass
                        if h3 not in groupMemberMids:
                            helper3.acceptGroupInvitation(op.param1)
                        if h2 not in groupMemberMids:
                            helper2.acceptGroupInvitation(op.param1)
                        if h1 not in groupMemberMids:
                            helper1.acceptGroupInvitation(op.param1)
                    except Exception as Error:
                        print(Error)
                elif cl in op.param3:
                    try:
                        try:
                            group = helper1.getGroup(op.param1)
                        except:
                            try:
                                group = helper2.getGroup(op.param1)
                            except:
                                try:
                                    group = helper3.getGroup(op.param1)
                                except:
                                    return
                        groupMemberMids = [i.mid for i in group.members if i.mid in dionMID]
                        titanBlackList = [i.mid for i in group.members if i.mid in dion["blacklist"]]
                        notInGroup = []
                        if h3 not in groupMemberMids:
                            notInGroup.append(h3)
                        if h2 not in groupMemberMids:
                            notInGroup.append(h2)
                        if h1 not in groupMemberMids:
                            notInGroup.append(h1)
                        if cl not in groupMemberMids:
                            notInGroup.append(cl)
                        if notInGroup != []:
                            if h1 in groupMemberMids:
                                try:
                                    helper1.inviteIntoGroup(group.id, notInGroup)
                                except:
                                    if h2 in groupMemberMids:
                                        try:
                                            helper2.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            if h3 in groupMemberMids:
                                                try:
                                                    helper3.inviteIntoGroup(group.id, notInGroup)
                                                except:
                                                    pass
                                    elif h3 in groupMemberMids:
                                        try:
                                            helper3.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            pass
                            elif h2 in groupMemberMids:
                                try:
                                    helper2.inviteIntoGroup(group.id, notInGroup)
                                except:
                                    if h1 in groupMemberMids:
                                        try:
                                            helper1.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            if h3 in groupMemberMids:
                                                try:
                                                    helper3.inviteIntoGroup(group.id, notInGroup)
                                                except:
                                                    pass
                                    elif h3 in groupMemberMids:
                                        try:
                                            helper3.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            pass
                            elif h3 in groupMemberMids:
                                try:
                                    helper3.inviteIntoGroup(group.id, notInGroup)
                                except:
                                    if h1 in groupMemberMids:
                                        try:
                                            helper1.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            if h2 in groupMemberMids:
                                                try:
                                                    helper2.inviteIntoGroup(group.id, notInGroup)
                                                except:
                                                    pass
                                    elif h2 in groupMemberMids:
                                        try:
                                            helper2.inviteIntoGroup(group.id, notInGroup)
                                        except:
                                            pass
                        for mid in titanBlackList:
                            try:
                                helper3.kickoutFromGroup(op.param1, [mid])
                            except:
                                try:
                                    helper2.kickoutFromGroup(op.param1, [mid])
                                except:
                                    try:
                                        helper1.kickoutFromGroup(op.param1, [mid])
                                    except:
                                        pass
                        if h3 not in groupMemberMids:
                            helper3.acceptGroupInvitation(op.param1)
                        if h2 not in groupMemberMids:
                            helper2.acceptGroupInvitation(op.param1)
                        if h1 not in groupMemberMids:
                            helper1.acceptGroupInvitation(op.param1)
                        if cl not in groupMemberMids:
                            client.acceptGroupInvitation(op.param1)
                    except Exception as Error:
                        print(Error)
        if op.type == 15:
            if op.param2 not in dionMID and op.param2 not in dion["blacklist"]:
                if "leave" in dion:
                    if dion["leave"] == True:
                        try:
                            contact = client.getContact(op.param2)
                            group = client.getGroup(op.param1)
                            sMsg = dion["leave"]
                            sMsg = sMsg.replace("{name}",contact.displayName)
                            sMsg = sMsg.replace("{contact}","")
                            sMsg = sMsg.replace("{gname}",group.name)
                            client.sendMessage(op.param1, sMsg)
                            if "{contact}" in dion["leave"]:
                                client.sendContact(op.param1, contact.mid)
                        except:
                            pass
        if op.type == 55:
            if op.param1 not in ReaderChecker["readRom"]:
                ReaderChecker["readRom"][op.param1] = {}
            if op.param2 not in ReaderChecker["readRom"][op.param1]:
                ReaderChecker["readRom"][op.param1][op.param2] = True
        if op.type == 26:
            msg = op.message
            if msg.contentMetadata is None:
                return
            elif msg.toType == 0:
                if msg.contentType == 6:
                    if "pcall" in dion:
                        if dion["pcall"] == True:
                            try:
                                client.sendMessage(msg._from,"ระบบป้องกันสแปมคอลเปิดอยู่\nระบบได้บล็อกคุณแล้ว")
                                time.sleep(1)
                                client.blockContact(msg._from)
                            except:
                                pass
            if msg.text is None:
                return
            if "kw" not in dion:
                dion["kw"] = {}
            while msg.text.startswith(" ") or msg.text.startswith("\n"):
                msg.text = msg.text[1:]
            while msg.text.endswith(" ") or msg.text.endswith("\n"):
                msg.text = msg.text[:-1]
            for x in dion["kw"]:
                if msg.text == x:
                    if msg.toType == 0:
                        client.sendMessage(msg._from, dion["kw"][x])
                    else:
                        client.sendMessage(msg.to, dion["kw"][x])
            if 'MENTION' in msg.contentMetadata.keys()!= None and msg.toType == 2:
                key = eval(msg.contentMetadata["MENTION"])
                tMid = [i["M"] for i in key["MENTIONEES"]]
                try:
                    if "detectMention" in dion and cl in tMid:
                        if dion["detectMention"] != "off":
                            contact = client.getContact(msg._from)
                            sMsg = dion["detectMention"]
                            sMsg = sMsg.replace("{tag}","")
                            sMsg = sMsg.replace("{pic}","")
                            sMsg = sMsg.replace("{name}",contact.displayName)
                            client.sendMessage(msg.to, sMsg)
                            if "{tag}" in dion["detectMention"]:
                                sendMessageWithMention(msg.to, contact.mid)
                except Exception as E:
                    print(E)
        if op.type == 26:
            msg = op.message
            try:
                if dion["autoread"] == True:
                    if msg.toType == 2:
                        client.sendChatChecked(msg.to, msg.id)
                    elif msg.toType == 1:
                        client.sendChatChecked(msg.to, msg.id)
                    else:
                        client.sendChatChecked(msg._from, msg.id)
            except:
                dion["autoread"] = False
        if op.type == 25:
            msg = op.message
            if op.type == 25 or msg._from == "u541bbaba15d68f3a652106a0de5a3e94":
                dionProcess(msg, op)
    except Exception as Error:
        #if Error.resason
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)

def dionKickerRuning():
    global KR
    while True:
        if KR != None:
            ops = kickerPoll.singleTrace(count=25)
            if ops != None:
                for op in ops:
                    try:
                        dionCore(op)
                    except Exception as Error:
                        print(Error)
                    kickerPoll.setRevision(op.revision)
        else:
            break

try:
    if "kicker" not in dion:
        dion["kicker"] = {"1":"#","2":"#","3":"#"}
    if dion["kicker"]["1"] != "#":
        helper1 = LINE(dion["kicker"]["1"], appName=APP)
        h1 = helper1.profile.mid
        print("[AUTO LOGIN] " + client.profile.displayName + " KICKER [1/3]")
    if dion["kicker"]["2"] != "#":
        helper2 = LINE(dion["kicker"]["2"], appName=APP)
        h2 = helper2.profile.mid
        print("[AUTO LOGIN] " + client.profile.displayName + " KICKER [2/3]")
    if dion["kicker"]["3"] != "#":
        helper3 = LINE(dion["kicker"]["3"], appName=APP)
        h3 = helper3.profile.mid
        print("[AUTO LOGIN] " + client.profile.displayName + " KICKER [3/3]")
    if h1 != None and h2 != None and h3 != None:
        dionMIDWithOutCL = [h1,h2,h3]
        KickerLogin = True
        dionMID = [cl,h1,h2,h3]

except Exception as Err:
    dion["kicker"]["1"] = "#"
    dion["kicker"]["2"] = "#"
    dion["kicker"]["3"] = "#"

while __name__ == "__main__":
    ops = poll.singleTrace(count=25)
    if ops != None:
        for op in ops:
            try:
                dionMainCore(op)
            except Exception as Error:
                if Error.resason == "LOG_OUT":
                    f=codecs.open(cl+'.json','w','utf-8')
                    json.dump(dion, f, sort_keys=True, indent=4, ensure_ascii=False)
                    sys.exit()
                else:
                    print(Error)
            poll.setRevision(op.revision)


while __name__ == "__main__x":
    try:
        Ops = client.singleTrace(50)#client.fetchOps(client,poll.rev, count=5)
    except EOFError:
        raise Exception("It might be wrong revision\n" + str(poll.rev))
    except Exception as E:
        print(E)
        sys.exit()
        

    for Op in Ops:
        if (Op.type != OpType.END_OF_OPERATION):
            poll.rev = max(poll.rev, Op.revision)
            dionMainCore(op)
