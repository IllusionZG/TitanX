antijsAmounts = 1
import platform

import os
import sys
import json

from tools import LiveJSON, FixJSON

__command__ = ['clear', 'cls']
for command in __command__:
    if os.system(command) == 0:
        break

print(platform.python_version())

def kickerBaseGenerator(amount):
    kickerBaseJson = {}
    for i in range(amount):
        kickerBaseJson[str(i+1)] = {'token': '#'}
    return kickerBaseJson

readerTemp = {}

print("""

\t\tTITANX BY PASUNX คนเดียว มีควยไรไหม
\t\t\tCOPYRIGHT(C) 2019

""")

settings = LiveJSON('settings.json')
FixJSON(settings, {'prefix':{'kicker':'x', 'self': '.'}, 'protect':{}, 'token': '#', 'kicker': {}, 'friend': False, "banlist":{}, "admin": {}, 'warmode':{}, "antijs": {}, "status":{}})
try:
    botAmounts = input("[@] Choice your bots amount (2/+) ")
    if not botAmounts.isdigit() and len(list(settings['kicker'])) < 2: exit("[@] bots amount must be a digit.")
    elif not botAmounts.isdigit(): botAmounts = len(list(settings['kicker']));print("[@] Loading bot amount by tokens..")
    if int(botAmounts) < 2: exit("[@] Your bots amount must be more than 2+")
    if int(botAmounts) >= 21 and SAFEMODE == True: exit(f"[@] ตั้ง {int(botAmounts)} ตัวบัคแอดเพื่อนนะครับ (SAFEMODE)")
    botAmounts = int(botAmounts)
except KeyboardInterrupt:
    exit("\n[@] Closed by user.")

KICKER = botAmounts
ANTIJS = antijsAmounts

print(f"[@] Running on {botAmounts+ANTIJS} bots. ({ANTIJS} GHOST)")

import random
import time
import traceback
import threading
import sys

from linepy import LINE, OEPoll

helpMessage = """-------- ᴛɪᴛᴀɴ x --------
ᴋɪᴄᴋᴇʀ ᴀᴍᴏᴜɴᴛ: {kk}

ꜱᴇʟꜰ ᴄᴏᴍᴍᴀɴᴅ:
- {s}ꜱᴛᴀᴛᴜꜱ
- {s}ᴄᴏɴᴛᴀᴄᴛ @
- {s}ᴍɪᴅ @
- {s}ᴘʀᴇꜰɪx ᴛᴇxᴛ

ᴋɪᴄᴋᴇʀ ᴄᴏᴍᴍᴀɴᴅ:
- {k} ʜᴇʟᴘ (ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅ)
- {k} ᴘʀᴇꜰɪx ᴛᴇxᴛ
- {k} ʟᴏɢ (ᴠɪᴇᴡ ʟᴏɢꜱ)
- {k} ꜱᴘᴇᴇᴅ
- {k} ʀᴇꜱᴘᴏɴꜱᴇ
- {k} ꜱᴛᴀᴛᴜꜱ
- {k} ᴊᴏɪɴ
- {k} ʟᴇᴀᴠᴇ
- {k} ᴋɪᴄᴋ @
- {k} ʙᴀɴ @, ɴᴀᴍᴇ (ʙᴀɴ)
- {k} ᴅᴇʟ @, ɴᴀᴍᴇ (ᴜɴʙᴀɴ)
- {k} ᴄʟᴇᴀʀ (ᴄʟᴇᴀʀ ʙᴀɴ)
- {k} ʟɪꜱᴛ (ʙᴀɴ ʟɪꜱᴛ)
- {k} ᴋɪʟʟ (ᴋɪᴄᴋ ʙᴀɴ)
- {k} ᴘʀᴏᴛᴇᴄᴛ
- {k} ᴀᴅᴍɪɴ ᴀᴅᴅ @, ɴᴀᴍᴇ
- {k} ᴀᴅᴍɪɴ ᴅᴇʟ @, ɴᴀᴍᴇ"""

kickerHelpMessage = """-------- ᴛɪᴛᴀɴ x --------
- {k} ʀᴇꜱᴘᴏɴꜱᴇ
- {k} ᴋɪᴄᴋ @
- {k} ʙᴀɴ @, ɴᴀᴍᴇ (ʙᴀɴ)
- {k} ᴅᴇʟ @, ɴᴀᴍᴇ (ᴜɴʙᴀɴ)
- {k} ᴄʟᴇᴀʀ (ᴄʟᴇᴀʀ ʙᴀɴ)
- {k} ʟɪꜱᴛ (ʙᴀɴ ʟɪꜱᴛ)
- {k} ᴋɪʟʟ (ᴋɪᴄᴋ ʙᴀɴ)
- {k} ᴘʀᴏᴛᴇᴄᴛ"""

logs = []

if len(settings["kicker"]) != KICKER:
    if len(settings["kicker"]) > KICKER:
        KICKER = KICKER
    else:
        for i in range(KICKER):
            if str(i+1) not in settings["kicker"]:
                settings["kicker"][str(i+1)] = {'token': '#'}
        settings["friend"] = False
		
if len(settings["antijs"]) != ANTIJS:
    if len(settings["antijs"]) > ANTIJS:
        ANTIJS = ANTIJS
    else:
        for i in range(ANTIJS):
            if str(i+1) not in settings["antijs"]:
                settings["antijs"][str(i+1)] = {'token': '#'}
        settings["friend"] = False

class InterpreterError(Exception): pass

def mentionMembers(to, mids, result):
    parsed_len = len(mids)//20+1
    mention = '@titanxasyn\n'
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

def command(text, prefix):
    if text.split(" ")[0][:len(prefix)] == prefix:
        _req = text.split(" ")
        _req.pop(0)
        return text.split(" ")[0][len(prefix):], [None] if len(_req) == 0 else _req
    return None, [None]

def toChar(text):
    normal = 'abcdefghijklmnopqrstuvwxyz'
    tochange = 'ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡxʏᴢ'
    for i in range(len(normal)):
        text = text.lower().replace(normal[i], tochange[i])
    return text

tempMessage = {}

def execute(op):
    global tempMessage
    global settings
    global kicker
    global logs
    global readerTemp

    if op.type == 32:
        if op.param3 in ghostMid:
            client.inviteIntoGroup(op.param1, [op.param3])
            client.kickoutFromGroup(op.param1, [op.param2])

    if op.type == 13:
        if op.param3 in botsMid:
            if op.param2 not in botsMid:
                for ki in kicker:
                    if kicker[ki].profile.mid == op.param3:
                        kicker[ki].acceptGroupInvitation(op.param1)
        elif ((op.param3 in settings["banlist"] or op.param2 in settings["banlist"]) == True and op.param2 not in botsMid ) == True:
            settings["banlist"][op.param2] = op.param1
            group = client.getGroup(op.param1)
            def func(op, group):
                banIg = []
                for member in group.members:
                    if member.mid in settings["banlist"] and member.mid != op.param2:
                        banIg.append(member.mid)
                bOn = []
                nInM = []
                nIn = []
                kicked = []
                canceled = []
                jWq = False
                bInvite = op.param3.split("\x1e")
                for ki in kicker:
                    if kicker[ki].profile.mid not in [member.mid for member in group.members]:
                        nInM.append(kicker[ki].profile.mid)
                        nIn.append(kicker[ki])
                    else:
                        bOn.append(kicker[ki])
                if bOn == []:
                    return
                else:
                    for ki in bOn:
                        try:
                            for _mid in bInvite:
                                if _mid not in canceled and ki.profile.mid not in settings["status"]:
                                    settings["banlist"][_mid] = op.param1
                                    ki.cancelGroupInvitation(group.id, [_mid])
                                    canceled.append(_mid)
                        except Exception as e:
                            error = str(e)
                            if "request blocked" in error:
                                error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                settings["status"][ki.profile.mid] = True
                            logs.append(error)
                            continue
                    for ki in bOn:
                        try:
                            if op.param2 not in kicked and ki.profile.mid not in settings["status"]:
                                ki.kickoutFromGroup(group.id, [op.param2])
                                kicked.append(op.param2)
                            for mid in banIg:
                                try:
                                    if mid not in kicked and ki.profile.mid not in settings["status"]:
                                        ki.kickoutFromGroup(group.id, [mid])
                                        kicked.append(mid)
                                except Exception as e:
                                    error = str(e)
                                    if "request blocked" in error:
                                        error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                    logs.append(error)
                                    break
                        except Exception as e:
                            error = str(e)
                            if "request blocked" in error:
                                error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                settings["status"][ki.profile.mid] = True
                            logs.append(error)
                            continue
                    if nInM != []:
                        for ki in bOn:
                            try:
                                if ki.profile.mid not in settings["status"]:
                                    ki.inviteIntoGroup(group.id, nInM)
                                    break
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                    settings["status"][ki.profile.mid] = True
                                logs.append(error)
                                continue
                        for ki in nIn:
                            try:
                                if jWq == False:
                                    ki.acceptGroupInvitation(group.id)
                                elif jWq is not None:
                                    ki.acceptGroupInvitationByTicket(group.id, jWq)
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                if "You are not related to group" in error and op.param1 not in settings["warmode"]:
                                    for iGB in bOn:
                                        try:
                                            if group.preventedJoinByTicket:
                                                group.preventedJoinByTicket = False
                                                iGB.updateGroup(group)
                                            jWq = iGB.reissueGroupTicket(group.id)
                                            ki.acceptGroupInvitationByTicket(group.id, jWq)
                                            break
                                        except:
                                            jWq = None
                                            continue
                                logs.append(error)
                                continue

                        for ki in bOn:
                            try:
                                if group.preventedJoinByTicket == False:
                                    group.preventedJoinByTicket = True
                                    ki.updateGroup(group)
                                else:
                                    break
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                logs.append(error)
                                continue
            th = threading.Thread(target=func, args=(op, group,))
            th.start()

        elif op.param1 in settings["protect"] and op.param2 not in botsMid:
            if isinstance(settings["protect"][op.param1], bool): return
            if settings["protect"][op.param1]["invite"] == True:
                if op.param1 in settings["admin"]:
                    if op.param2 in settings["admin"][op.param1]:
                        return
                settings["banlist"][op.param2] = op.param1
                settings["banlist"][op.param3] = op.param1
                return execute(op)

    if op.type == 17:
        if (op.param2 in settings["banlist"]) == True:
            settings["banlist"][op.param2] = op.param1
            if op.param2 in botsMid:
                return
            group = client.getGroup(op.param1)
            def func(op, group):
                banIg = []
                banIv = []
                if group.invitee is not None:
                    for contact in group.invitee:
                        if contact.mid in settings["banlist"] and contact.mid != op.param2:
                            banIv.append(contact.mid)
                for member in group.members:
                    if member.mid in settings["banlist"] and member.mid != op.param2:
                        banIg.append(member.mid)
                bOn = []
                nInM = []
                nIn = []
                kicked = []
                canceled = []
                jWq = False
                for ki in kicker:
                    if kicker[ki].profile.mid not in [member.mid for member in group.members]:
                        nInM.append(kicker[ki].profile.mid)
                        nIn.append(kicker[ki])
                    else:
                        bOn.append(kicker[ki])
                if bOn == []:
                    return
                else:
                    for ki in bOn:
                        try:
                            if op.param2 not in kicked and ki.profile.mid not in settings["status"]:
                                ki.kickoutFromGroup(group.id, [op.param2])
                                kicked.append(op.param2)
                            for mid in banIg:
                                try:
                                    if mid not in kicked and ki.profile.mid not in settings["status"]:
                                        ki.kickoutFromGroup(group.id, [mid])
                                        kicked.append(mid)
                                except Exception as e:
                                    error = str(e)
                                    if "request blocked" in error:
                                        error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                    logs.append(error)
                                    break
                        except Exception as e:
                            error = str(e)
                            if "request blocked" in error:
                                error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                settings["status"][ki.profile.mid] = True
                            logs.append(error)
                            continue
                    for ki in bOn:
                        try:
                            for _mid in banIv:
                                if _mid not in canceled and ki.profile.mid not in settings["status"]:
                                    settings["banlist"][_mid] = True
                                    ki.cancelGroupInvitation(group.id, [_mid])
                                    canceled.append(_mid)
                        except Exception as e:
                            error = str(e)
                            if "request blocked" in error:
                                error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                settings["status"][ki.profile.mid] = True
                            logs.append(error)
                            continue
                    if nInM != []:
                        for ki in bOn:
                            try:
                                if ki.profile.mid not in settings["status"]:
                                    ki.inviteIntoGroup(group.id, nInM)
                                    break
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                    settings["status"][ki.profile.mid] = True
                                logs.append(error)
                                continue
                        for ki in nIn:
                            try:
                                if jWq == False:
                                    ki.acceptGroupInvitation(group.id)
                                elif jWq is not None:
                                    ki.acceptGroupInvitationByTicket(group.id, jWq)
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                if "You are not related to group" in error and op.param1 not in settings["warmode"]:
                                    for iGB in bOn:
                                        try:
                                            if group.preventedJoinByTicket:
                                                group.preventedJoinByTicket = False
                                                iGB.updateGroup(group)
                                            jWq = iGB.reissueGroupTicket(group.id)
                                            ki.acceptGroupInvitationByTicket(group.id, jWq)
                                            break
                                        except:
                                            jWq = None
                                            continue
                                logs.append(error)
                                continue
                        for ki in bOn:
                            try:
                                if group.preventedJoinByTicket == False:
                                    group.preventedJoinByTicket = True
                                    ki.updateGroup(group)
                                else:
                                    break
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                logs.append(error)
                                continue
            th = threading.Thread(target=func, args=(op, group,))
            th.start()

    if op.type == 19:
        if (op.param3 in botsMid) == True or op.param2 in settings["banlist"]:
            if (op.param3 != client.profile.mid and op.param2 not in botsMid) == True:
                settings["banlist"][op.param2] = op.param1
                group = client.getGroup(op.param1)
                def func(op, group):
                    banIg = []
                    banIv = []
                    if group.invitee is not None:
                        for contact in group.invitee:
                            if contact.mid in settings["banlist"] and contact.mid != op.param2:
                                banIv.append(contact.mid)
                    for member in group.members:
                        if member.mid in settings["banlist"] and member.mid != op.param2:
                            banIg.append(member.mid)
                    bOn = []
                    nInM = []
                    kicked = []
                    nIn = []
                    canceled = []
                    jWq = False
                    for ki in kicker:
                        if kicker[ki].profile.mid not in [member.mid for member in group.members]:
                            nInM.append(kicker[ki].profile.mid)
                            nIn.append(kicker[ki])
                        else:
                            bOn.append(kicker[ki])
                    if bOn == []:
                        return
                    else:
                        for ki in bOn:
                            try:
                                if op.param2 not in kicked and ki.profile.mid not in settings["status"]:
                                    ki.kickoutFromGroup(group.id, [op.param2])
                                    kicked.append(op.param2)
                                for mid in banIg:
                                    try:
                                        if mid not in kicked and ki.profile.mid not in settings["status"]:
                                            ki.kickoutFromGroup(group.id, [mid])
                                            kicked.append(mid)
                                    except Exception as e:
                                        error = str(e)
                                        if "request blocked" in error:
                                            error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                            settings["status"][ki.profile.mid] = True
                                        logs.append(error)
                                        break
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                    settings["status"][ki.profile.mid] = True
                                logs.append(error)
                                continue
                        if nInM != []:
                            for ki in bOn:
                                try:
                                    if ki.profile.mid not in settings["status"]:
                                        ki.inviteIntoGroup(group.id, nInM)
                                        break
                                except Exception as e:
                                    error = str(e)
                                    if "request blocked" in error:
                                        error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                        settings["status"][ki.profile.mid] = True
                                    logs.append(error)
                                    continue
                        for ki in nIn:
                            try:
                                if jWq == False:
                                    ki.acceptGroupInvitation(group.id)
                                elif jWq is not None:
                                    ki.acceptGroupInvitationByTicket(group.id, jWq)
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                if "You are not related to group" in error and op.param1 not in settings["warmode"]:
                                    for iGB in bOn:
                                        try:
                                            if group.preventedJoinByTicket:
                                                group.preventedJoinByTicket = False
                                                iGB.updateGroup(group)
                                            jWq = iGB.reissueGroupTicket(group.id)
                                            ki.acceptGroupInvitationByTicket(group.id, jWq)
                                            break
                                        except:
                                            jWq = None
                                            continue
                                logs.append(error)
                                continue
                        if banIv != []:
                            for ki in bOn:
                                try:
                                    for _mid in banIv:
                                        if _mid not in canceled and ki.profile.mid not in settings["status"]:
                                            ki.cancelGroupInvitation(group.id, [_mid])
                                            canceled.append(_mid)
                                except Exception as e:
                                    error = str(e)
                                    if "request blocked" in error:
                                        error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                        settings["status"][ki.profile.mid] = True
                                    logs.append(error)
                                    continue
                        for ki in bOn:
                            try:
                                if group.preventedJoinByTicket == False:
                                    group.preventedJoinByTicket = True
                                    ki.updateGroup(group)
                                else:
                                    break
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                logs.append(error)
                                continue
                th = threading.Thread(target=func, args=(op, group,))
                th.start()

            if op.param3 == client.profile.mid:
                settings["banlist"][op.param2] = op.param1
                def func():
                    kicked = []
                    inv = False
                    for ki in kicker:
                        try:
                            kicker[ki].inviteIntoGroup(op.param1, [client.profile.mid])
                            client.acceptGroupInvitation(op.param1)
                            inv = True
                            break
                        except Exception as e:
                            error = str(e)
                            if "request blocked" in error:
                                error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                            logs.append(error)
                            continue
                    if inv:
                        for ki in kicker:
                            try:
                                if op.param2 not in kicked and kicker[ki].profile.mid not in settings["status"]:
                                    kicker[ki].kickoutFromGroup(op.param1, [op.param2])
                                    kicked.append(op.param2)
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    settings["status"][kicker[ki].profile.mid] = True
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                logs.append(error)
                                continue
                    if kicked == []:
                        for injs in antijs:
                            try:
                                antijs[injs].acceptGroupInvitation(op.param1)
                                gM = antijs[injs].getGroup(op.param1).members
                                nIG = []
                                for ki in kicker:
                                    if kicker[ki].profile.mid not in gM:
                                        nIG.append(kicker[ki].profile.mid)
                                nIG.append(client.profile.mid)
                                antijs[injs].inviteIntoGroup(op.param1, nIG)
                                try:
                                    for ki in kicker:
                                        if kicker[ki].profile.mid in nIG:
                                            kicker[ki].acceptGroupInvitation(op.param1)
                                    client.acceptGroupInvitation(op.param1)
                                except: pass
                                try:
                                    antijs[injs].kickoutFromGroup(op.param1, [op.param2])
                                    antijs[injs].leaveGroup(op.param1)
                                    client.inviteIntoGroup(op.param1, [antijs[injs].profile.mid])
                                except: pass
                            except: continue
                th = threading.Thread(target=func)
                th.start()

        elif op.param1 in settings["protect"] and op.param2 not in botsMid:
            if isinstance(settings["protect"][op.param1], bool): return
            if op.param1 in settings["admin"]:
                if op.param3 in settings["admin"][op.param1]:
                    settings["banlist"][op.param2] = op.param1
                    return execute(op)
            if settings["protect"][op.param1]["kick"] == True:
                if op.param1 in settings["admin"]:
                    if op.param2 in settings["admin"][op.param1]:
                        return
                settings["banlist"][op.param2] = op.param1
                return execute(op)

    if op.type == 11:
        if (op.param2 in settings["banlist"]) == True:
            if op.param2 not in botsMid:
                settings["banlist"][op.param2] = op.param1
                group = client.getGroup(op.param1)
                def func(op, group):
                    banIg = []
                    for member in group.members:
                        if member.mid in settings["banlist"] and member.mid != op.param2:
                            banIg.append(member.mid)
                    bOn = []
                    nInM = []
                    nIn = []
                    kicked = []
                    jWq = False
                    for ki in kicker:
                        if kicker[ki].profile.mid not in [member.mid for member in group.members]:
                            nInM.append(kicker[ki].profile.mid)
                            nIn.append(kicker[ki])
                        else:
                            bOn.append(kicker[ki])
                    if bOn == []:
                        return
                    else:
                        for ki in bOn:
                            try:
                                if op.param3 == '1':
                                    if settings["protect"][op.param1]["name"] != False:
                                        group.name = group.name if group.name == settings["protect"][op.param1]["name"] else settings["protect"][op.param1]["name"]
                                        if group.preventedJoinByTicket == False:
                                            group.preventedJoinByTicket = True
                                        ki.updateGroup(group)
                                        break
                                else:
                                    break
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                logs.append(error)
                                continue
                        for ki in bOn:
                            try:
                                if ki.profile.mid not in settings["status"]:
                                    if op.param2 not in kicked:
                                        ki.kickoutFromGroup(group.id, [op.param2])
                                        kicked.append(op.param2)
                                    for mid in banIg:
                                        try:
                                            if mid not in kicked:
                                                ki.kickoutFromGroup(group.id, [mid])
                                                kicked.append(mid)
                                        except:
                                            break
                            except Exception as e:
                                error = str(e)
                                if "request blocked" in error:
                                    error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                    settings["status"][ki.profile.mid] = True
                                logs.append(error)
                                continue
                        if nInM != []:
                            for ki in bOn:
                                try:
                                    if ki.profile.mid not in settings["status"]:
                                        ki.inviteIntoGroup(group.id, nInM)
                                        break
                                except Exception as e:
                                    error = str(e)
                                    if "request blocked" in error:
                                        error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                        settings["status"][ki.profile.mid] = True
                                    logs.append(error)
                                    continue
                            for ki in nIn:
                                try:
                                    if jWq == False:
                                        ki.acceptGroupInvitation(group.id)
                                    elif jWq is not None:
                                        ki.acceptGroupInvitationByTicket(group.id, jWq)
                                except Exception as e:
                                    error = str(e)
                                    if "request blocked" in error:
                                        error = "ʀᴇQᴜᴇꜱᴛ ʙʟᴏᴄᴋᴇᴅ"
                                    if "You are not related to group" in error and op.param1 not in settings["warmode"]:
                                        for iGB in bOn:
                                            try:
                                                if group.preventedJoinByTicket:
                                                    group.preventedJoinByTicket = False
                                                    iGB.updateGroup(group)
                                                jWq = iGB.reissueGroupTicket(group.id)
                                                ki.acceptGroupInvitationByTicket(group.id, jWq)
                                                break
                                            except:
                                                jWq = None
                                                continue
                                    logs.append(error)
                                    continue
                th = threading.Thread(target=func, args=(op, group,))
                th.start()
        elif op.param1 in settings["protect"] and op.param2 not in botsMid and op.param3 == '4':
            if isinstance(settings["protect"][op.param1], bool): return
            if "qr" not in settings["protect"][op.param1]: return
            if settings["protect"][op.param1]["qr"] == True:
                if op.param1 in settings["admin"]:
                    if op.param2 in settings["admin"][op.param1]:
                        return
                settings["banlist"][op.param2] = op.param1
                return execute(op)

        elif op.param1 in settings["protect"] and op.param2 not in botsMid and op.param3 == '1':
            if isinstance(settings["protect"][op.param1], bool): return
            if "name" not in settings["protect"][op.param1]: return
            if settings["protect"][op.param1]["name"] != False:
                if op.param1 in settings["admin"]:
                    if op.param2 in settings["admin"][op.param1]:
                        settings["protect"][op.param1]["name"] = client.getGroup(op.param1).name
                        return
                settings["banlist"][op.param2] = op.param1
                return execute(op)

    if op.type == 25 or op.type == 26:
        msg = op.message
        to = msg.to
        if msg.text == None:
            return
        if 'message_relation_server_message_id' in msg.contentMetadata:
            msg.text = msg.text if msg.contentMetadata['message_relation_server_message_id'] not in tempMessage else tempMessage[msg.contentMetadata['message_relation_server_message_id']]
        tempMessage[msg.id] = msg.text
        if msg.to not in settings["admin"]:
            settings["admin"][msg.to] = {}

        cmds = msg.text.split(" && ")
        if len(cmds) == 1: cmds = None
        if not cmds == None:
            for cmd in cmds:
                op.message.text = cmd
                execute(op)
            return
        cmd, req = command(msg.text, settings['prefix']['self'])
        p, kcmd = command(msg.text.lower(), settings['prefix']['kicker'])

        if msg.to not in settings["admin"]:
            settings["admin"] = {}
        allowed = True if msg._from in botsMid else True if msg._from in settings["admin"][msg.to] else False
        isself = msg._from in botsMid and msg._from == client.profile.mid

        if op.type == 25:
            if cmd is not None:
                if cmd.lower() == "reader":
                    if not to in readerTemp: return
                    mids = [mid for mid in readerTemp[to]]
                    mentionMembers(to, mids, "บัญชีที่อ่านข้อความ:\n")
                    del readerTemp[to]
                    
                if cmd.lower() == "help":
                    client.sendMessage(to, helpMessage.format(kk=str(KICKER), s=toChar(settings['prefix']['self']), k=toChar(settings['prefix']['kicker'])))

                if cmd.lower() == "prefix":
                    if req[0] == None:
                        message = f"ꜱᴇʟꜰ ᴘʀᴇꜰɪx ɪꜱ {toChar(settings['prefix']['self'])}"
                        return client.sendMessage(to, message)
                    settings['prefix']['self'] = req[0]
                    message = f"ꜱᴇʟꜰ ᴘʀᴇꜰɪx ɪꜱ ꜱᴇᴛ ᴛᴏ {toChar(settings['prefix']['self'])}"
                    return client.sendMessage(to, message)

                if msg.text.lower().startswith(f"{settings['prefix']['self']}exec"):
                    try:
                        exec(msg.text[len(f"{settings['prefix']['self']}exec\n"):].strip())
                    except SyntaxError as err:
                        error_class = err.__class__.__name__
                        detail = err.args[0]
                        line_number = err.lineno
                    except AssertionError as err:
                        return client.sendMessage(to, toChar("AssertionError"))
                    except Exception as err:
                        error_class = err.__class__.__name__
                        detail = err.args[0]
                        cl, exc, tb = sys.exc_info()
                        line_number = traceback.extract_tb(tb)[-1][1]
                    else:
                        return
                    client.sendMessage(to, toChar("%s at line %d: %s" % (error_class, line_number, detail)))

                if cmd.lower() == "contact" or cmd.lower() == "mid":
                    def sendContactOrMid(to, mids, cmd):
                        for mid in mids:
                            if len(mid) == len(client.profile.mid):
                                if cmd == "contact":
                                    client.sendContact(to, mid)
                                if cmd == "mid":
                                    client.sendMessage(to, mid)
                    if req[0] == None:
                        return sendContactOrMid(to, [client.profile.mid], cmd)
                    midslist = []
                    if "MENTION" in msg.contentMetadata:
                        midslist = [mention["M"] for mention in eval(msg.contentMetadata["MENTION"])["MENTIONEES"]]
                    midslist = midslist + req
                    sendContactOrMid(to, midslist, cmd)

                if cmd.lower() == "status" and req[0] == None:
                    try:
                        client.inviteIntoGroup(to, [client.profile.mid])
                        message = "ɪɴᴠɪᴛᴇ & ᴋɪᴄᴋ: ʀᴇᴀᴅʏ"
                    except: message = "ɪɴᴠɪᴛᴇ & ᴋɪᴄᴋ: ɴᴏᴛ ʀᴇᴀᴅʏ"
                    client.sendMessage(to, message)
            else:
                if to in readerTemp:
                    del readerTemp[to]

        if p is None: return
        if p.lower() != "": return

        if kcmd[0] == "ghost" and isself:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            if group.invitee == None: return
            invJS = [contact.mid for contact in group.invitee]
            iAd = []
            for tijs in antijs:
                if antijs[tijs].profile.mid not in invJS:
                    iAd.append(antijs[tijs].profile.mid)
            if iAd != []:
                client.inviteIntoGroup(to, iAd)
                client.sendMessage(to, toChar("ghost enable"))
            else:
                client.sendMessage(to, toChar("ghost is already on"))

        if kcmd[0] == "help" and allowed:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            if group.id not in settings["admin"]:
                settings["admin"][group.id] = {}
            if isinstance(settings["admin"][group.id], bool):
                del settings["admin"][group.id]
                return execute(op)
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn: return
            random.choice(bOn).sendMessage(to, kickerHelpMessage.format(k=toChar(settings["prefix"]["kicker"])))

        if kcmd[0] == "prefix" and isself:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn: return
            if len(kcmd) <= 1:
                message = f"ᴋɪᴄᴋᴇʀ ᴘʀᴇꜰɪx ɪꜱ {toChar(settings['prefix']['kicker'])}"
                return random.choice(bOn).sendMessage(group.id, message)
            settings['prefix']['kicker'] = kcmd[1]
            message = f"ᴋɪᴄᴋᴇʀ ᴘʀᴇꜰɪx ɪꜱ ꜱᴇᴛ ᴛᴏ {toChar(settings['prefix']['kicker'])}"
            return random.choice(bOn).sendMessage(group.id, message)

        if kcmd[0] == "war" and isself:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn: return
            if len(kcmd) <= 1:
                message = toChar("war mode is enable" if group.id in settings["warmode"] else "war mode is disable")
                return random.choice(bOn).sendMessage(group.id, message)
            if kcmd[1] == "on":
                if group.id in settings["warmode"]: return  random.choice(bOn).sendMessage(group.id, toChar("war mode is already enable"))
                settings["warmode"][group.id] = True 
                return random.choice(bOn).sendMessage(group.id, toChar("war mode enable"))
            if kcmd[1] == "off":
                if group.id not in settings["warmode"]: return  random.choice(bOn).sendMessage(group.id, toChar("war mode is already disable"))
                del settings["warmode"][group.id]
                return random.choice(bOn).sendMessage(group.id, toChar("war mode disable"))

        if kcmd[0] == "protect":
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            if group.id not in settings["protect"]:
                settings["protect"][group.id] = {"invite": False, "qr": False, "kick": False, "name": False}
            if isinstance(settings["protect"][group.id], bool):
                del settings["protect"][group.id]
                return execute(op)
            FixJSON(settings["protect"][group.id], {"invite": False, "qr": False, "kick": False, "name": False})
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn: return
            if len(kcmd) <= 2:
                message = "ɪɴᴠɪᴛᴇ ᴘʀᴏᴛᴇᴄᴛ: ᴏɴ" if settings["protect"][group.id]["invite"] == True else "ɪɴᴠɪᴛᴇ ᴘʀᴏᴛᴇᴄᴛ: ᴏꜰꜰ"
                message += "\nᴋɪᴄᴋ ᴘʀᴏᴛᴇᴄᴛ: ᴏɴ" if settings["protect"][group.id]["kick"] == True else "\nᴋɪᴄᴋ ᴘʀᴏᴛᴇᴄᴛ: ᴏꜰꜰ"
                message += "\nQʀ ᴘʀᴏᴛᴇᴄᴛ: ᴏɴ" if settings["protect"][group.id]["qr"] == True else "\nQʀ ᴘʀᴏᴛᴇᴄᴛ: ᴏꜰꜰ"
                message += "\nɴᴀᴍᴇ ᴘʀᴏᴛᴇᴄᴛ: ᴏɴ" if not settings["protect"][group.id]["name"] == False else "\nɴᴀᴍᴇ ᴘʀᴏᴛᴇᴄᴛ: ᴏꜰꜰ"
                return random.choice(bOn).sendMessage(group.id, message)
            if kcmd[1] in settings["protect"][group.id] and allowed:
                if kcmd[2] == "on":
                    settings["protect"][group.id][kcmd[1]] = True if kcmd[1] != "name" else group.name
                if kcmd[2] == "off":
                    settings["protect"][group.id][kcmd[1]] = False
                return random.choice(bOn).sendMessage(group.id, toChar(f"{kcmd[1]} ᴘʀᴏᴛᴇᴄᴛ ɪꜱ ꜱᴇᴛ ᴛᴏ ᴏɴ") if settings["protect"][group.id][kcmd[1]] != False else toChar(f"{kcmd[1]} ᴘʀᴏᴛᴇᴄᴛ ɪꜱ ꜱᴇᴛ ᴛᴏ ᴏꜰꜰ"))
            elif kcmd[1] == "all" and allowed:
                if kcmd[2] == "on":
                    for typeOfProtect in list(settings["protect"][group.id]):
                        settings["protect"][group.id][typeOfProtect] = True if typeOfProtect != "name" else group.name
                if kcmd[2] == "off":
                    for typeOfProtect in list(settings["protect"][group.id]):
                        settings["protect"][group.id][typeOfProtect] = False
                return random.choice(bOn).sendMessage(group.id, toChar(f"all ᴘʀᴏᴛᴇᴄᴛ ɪꜱ ꜱᴇᴛ ᴛᴏ ᴏɴ") if settings["protect"][group.id]["qr"] == True else toChar(f"all ᴘʀᴏᴛᴇᴄᴛ ɪꜱ ꜱᴇᴛ ᴛᴏ ᴏꜰꜰ"))

        if kcmd[0] == "admin":
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            if group.id not in settings["admin"]:
                settings["admin"][group.id] = {}
            if isinstance(settings["admin"][group.id], bool):
                del settings["admin"][group.id]
                return execute(op)
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn: return
            if len(kcmd) <= 2:
                if len(kcmd) <= 1:
                    message = o = toChar("admin(s) on this group:")
                    for id in settings["admin"][group.id]:
                        message += f"\n- {settings['admin'][group.id][id]}"
                    return random.choice(bOn).sendMessage(group.id, message if len(message) != len(o) else toChar("no admin on this group"))
                if kcmd[1] == "clear" and isself:
                    if group.id in settings["admin"]:
                        del settings["admin"][group.id]
                        return random.choice(bOn).sendMessage(to, toChar("clear all admin on this group"))
            if kcmd[1] == "add" and isself:
                message = o = toChar("add admin(ꜱ):")
                kcmd.pop(0)
                kcmd.pop(0)
                addName = ' '.join(kcmd)
                addName = addName if not addName.endswith(' ') else addName[:len(addName)-1]
                for member in group.members:
                    if (addName.lower() in member.displayName.lower() if len(member.displayName) > len(addName) else  member.displayName.lower() in addName.lower()) == True:
                        if member.mid not in botsMid and member.mid not in settings["admin"][group.id]:
                            settings["admin"][group.id][member.mid] = member.displayName
                            if member.mid in settings["banlist"]:
                                random.choice(bOn).sendMessage(to, f"ᴅᴇʟ {member.displayName} ɪɴ ʙᴀɴʟɪꜱᴛ")
                            message += f"\n- {member.displayName}"
                return random.choice(bOn).sendMessage(to, message if len(message) != len(o) else toChar("no new admin added."))
            if kcmd[1] == "del" and isself:
                message = o = toChar("del admin(ꜱ):")
                kcmd.pop(0)
                kcmd.pop(0)
                addName = ' '.join(kcmd)
                addName = addName if not addName.endswith(' ') else addName[:len(addName)-1]
                for member in group.members:
                    if (addName.lower() in member.displayName.lower() if len(member.displayName) > len(addName) else  member.displayName.lower() in addName.lower()) == True:
                        if member.mid not in botsMid and member.mid in settings["admin"][group.id]:
                            del settings["admin"][group.id][member.mid]
                            message += f"\n- {member.displayName}"
                return random.choice(bOn).sendMessage(to, message if len(message) != len(o) else toChar("no admin deleted."))

        if kcmd[0] == "kill" and allowed:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            bOn = []
            kicked = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn: return
            midslist = []
            for member in group.members:
                if member.mid in settings["banlist"]:
                    midslist.append(member.mid)
            for ki in bOn:
                for mid in midslist:
                    try:
                        if mid not in kicked:
                            ki.kickoutFromGroup(group.id, [mid])
                            kicked.append(mid)
                    except: continue

        if kcmd[0] == "del" and allowed:
            if len(kcmd) == 1: return
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn: return
            message = "ᴅᴇʟ ᴜꜱᴇʀ(ꜱ):"
            kcmd.pop(0)
            banName = ' '.join(kcmd)
            banName = banName if not banName.endswith(' ') else banName[:len(banName)-1]
            for member in group.members:
                if (banName.lower() in member.displayName.lower() if len(member.displayName) > len(banName) else  member.displayName.lower() in banName.lower()) == True:
                    if member.mid not in botsMid and member.mid in settings["banlist"]:
                        del settings["banlist"][member.mid]
                        message += f"\n- {member.displayName}"
            if message == "ᴅᴇʟ ᴜꜱᴇʀ(ꜱ):": return random.choice(bOn).sendMessage(to, toChar("no blacklist deleted."))
            random.choice(bOn).sendMessage(to, message)

        if kcmd[0] == "ban" and allowed:
            if len(kcmd) == 1: return
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            if group.id not in settings["admin"]:
                settings["admin"][group.id] = {}
            if isinstance(settings["admin"][group.id], bool):
                del settings["admin"][group.id]
                return execute(op)
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn:
                return
            message = old = "ᴀᴅᴅᴇᴅ ᴜꜱᴇʀ(ꜱ):"
            kcmd.pop(0)
            banName = ' '.join(kcmd)
            banName = banName if not banName.endswith(' ') else banName[:len(banName)-1]
            for member in group.members:
                if (banName.lower() in member.displayName.lower() if len(member.displayName) > len(banName) else  member.displayName.lower() in banName.lower()) == True:
                    if member.mid not in botsMid and member.mid not in settings["banlist"] and member.mid not in settings["admin"][group.id]:
                        settings["banlist"][member.mid] = group.id
                        message += f"\n- {member.displayName}"
            random.choice(bOn).sendMessage(to, message if len(message) != len(old) else toChar("no new blacklist added."))

        if kcmd[0] == "log" and isself:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            if group.id not in settings["admin"]:
                settings["admin"][group.id] = {}
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn:
                return
            message = old = "ᴇʀʀᴏʀ ʟᴏɢ(ꜱ):"
            for log in logs:
                message += f"\n{log}"
            logs = []
            random.choice(bOn).sendMessage(to, message if len(message) != len(old) else "ɴᴏ ʟᴏɢꜱ")

        if kcmd[0] == "kick" and allowed:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group:
                return
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn:
                return
            midslist = []
            if "MENTION" in msg.contentMetadata:
                midslist = [mention["M"] for mention in eval(msg.contentMetadata["MENTION"])["MENTIONEES"]]
            for ki in bOn:
                for mid in midslist:
                    try:
                        if mid != ki.profile.mid and mid not in botsMid and mid not in settings["admin"][group.id]:
                            ki.kickoutFromGroup(group.id, [mid])
                    except:
                        continue

        if kcmd[0] == "status" and isself:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn: return
            for ki in bOn:
                try:
                    ki.inviteIntoGroup(group.id, [ki.profile.mid])
                    message = "ʀᴇᴀᴅʏ"
                    if ki.profile.mid in settings["status"]:
                        del settings["settings"][ki.profile.mid]
                except:
                    message = "ɴᴏᴛ ʀᴇᴀᴅʏ"
                    settings["status"][ki.profile.mid] = True
                ki.sendMessage(group.id, message)

        if kcmd[0] == "leave" and isself:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group:
                return
            inG = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    inG.append(kicker[ki])
            for ki in inG:
                ki.leaveGroup(group.id)

        if kcmd[0] == "clear" and allowed:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn: return
            nd = 0
            if len(kcmd) >= 2:
                if not kcmd[1] == "all" and not isself: return
                if settings['banlist'] == {}:
                    return random.choice(bOn).sendMessage(to, toChar(f"no user on blacklist."))
                random.choice(bOn).sendMessage(to, toChar(f"clear {len(settings['banlist'])} user(s) on blacklist."))
                settings['banlist'] = {}
                return
            dp = 0
            for mid in settings['banlist']:
                if settings['banlist'][mid] == to:
                    del settings['banlist'][mid]
                    dp += 1
            random.choice(bOn).sendMessage(to, toChar(f"clear {dp} blacklist user(s) on this group.") if dp != 0 else toChar(f"no blacklist user on this group."))

        if kcmd[0] == "list" and allowed:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group: return
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn: return
            if len(kcmd) >= 2:
                if kcmd[1] == "all" and isself:
                    message = old = toChar("all blacklist user(s):")
                    for mid in settings['banlist']:
                        message += f"\n- {client.getContact(mid).displayName}"
                    return random.choice(bOn).sendMessage(to, message if len(message) != len(old) else toChar("no blacklist user."))
                else:
                    return
            else:
                message = old = toChar("blacklist user(s) on this group:")
                for mid in settings['banlist']:
                    if settings['banlist'][mid] == to:
                        message += f"\n- {client.getContact(mid).displayName}"
            return random.choice(bOn).sendMessage(to, message if len(message) != len(old) else toChar("no blacklist on this group."))

        if kcmd[0] == "response" and allowed:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group:
                return
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki].profile.mid)
            if not bOn:
                return
            for n, ki in enumerate(kicker):
                if kicker[ki].profile.mid in bOn:
                    kicker[ki].sendMentionV2(to, "@!", [msg._from])

        if kcmd[0] == "rank" and isself:
            igenet = 1000
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group:
                return
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn:
                return
            if len(kcmd) == 2: igenet = 1000 if not kcmd[1].isdigit() else int(kcmd[1])
            else: random.choice(bOn).sendMessage(group.id, toChar(f"start testing with rank {igenet}"))
            powerLaist = {}
            for i in range(11):
                powerLaist[i] = 10-i
            for ki in bOn:
                startTime = time.time()
                profile = ki.getProfile()
                endTime = int((time.time() - startTime)*igenet)
                ki.sendMessage(group.id, toChar("0/10 stars" if endTime not in list(powerLaist) and endTime < list(powerLaist)[0] else f'10/10 stars' if endTime < list(powerLaist)[0] and endTime not in list(powerLaist) else f"{powerLaist[int(str(endTime)[1]) if len(str(endTime)) >= 2 else endTime]}/10 stars"))

        if kcmd[0] == "speed" and isself:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group:
                return
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn:
                return
            for ki in bOn:
                startTime = time.time()
                profile = ki.getProfile()
                endTime = time.time() - startTime
                ki.sendMessage(to, toChar(f'{endTime} second | {int(endTime*1000)} MS'))

        if kcmd[0] == "profile" and isself:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group:
                return
            bOn = []
            for ki in kicker:
                if kicker[ki].profile.mid in [member.mid for member in group.members]:
                    bOn.append(kicker[ki])
            if not bOn:
                return
            if len(kcmd) >= 2:
                if kcmd[1] == "picture":
                    if len(kcmd) == 3:
                        if kcmd[2] == "self":
                            for ki in bOn:
                                ki.updateProfilePicture(ki.downloadFileURL("http://dl.profile.line-cdn.net/{}".format(client.getProfile().pictureStatus)))
                        if kcmd[2] == "k1":
                            for ki in bOn:
                                ki.updateProfilePicture(ki.downloadFileURL("http://dl.profile.line-cdn.net/{}".format(kicker[1].getProfile().pictureStatus)))
                elif kcmd[1] == "name":
                    kcmd.pop(0)
                    kcmd.pop(0)
                    if kcmd == []:
                        for ki in bOn:
                            ki.sendMessage(to, ki.getProfile().displayName)
                        return
                    toChange = ' '.join(kcmd)
                    toChange = toChange if not toChange.endswith(' ') else toChange[:len(toChange)-1]
                    for ki in bOn:
                        if len(toChange) > 20: return client.sendMessage(to, toChar('display name over limits.'))
                        proobj = ki.getProfile()
                        proobj.displayName = toChange
                        ki.updateProfile(proobj)

        if kcmd[0] == "join" and isself:
            group = client.getGroup(to) if msg.toType == 2 else None
            if not group:
                return
            def func(group):
                bOn = []
                nIn = []
                iC = False
                for ki in kicker:
                    if kicker[ki].profile.mid not in [member.mid for member in group.members]:
                        nIn.append(kicker[ki])
                    else:
                        bOn.append(kicker[ki])
                if nIn == []:
                    return random.choice(bOn).sendMessage(group.id, "ᴡᴇ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ɪɴ ɢʀᴏᴜᴘ")
                if group.preventedJoinByTicket:
                    group.preventedJoinByTicket = False
                    if bOn == []:
                        client.updateGroup(group)
                    else:
                        random.choice(bOn).updateGroup(group)
                    iC = True
                ticket = client.reissueGroupTicket(group.id)
                for k in nIn:
                    k.acceptGroupInvitationByTicket(group.id, ticket)
                if iC == True:
                    group.preventedJoinByTicket = True
                    random.choice(nIn).updateGroup(group)
            TH = threading.Thread(target=func, args=(group,))
            TH.deamon = True
            TH.start()
    if op.type == 55:
        if not op.param1 in readerTemp: readerTemp[op.param1] = {}
        readerTemp[op.param1][op.param2] = True

client = LINE()
kicker = {}
antijs = {}
try:
    client.login(settings["token"], appName=f"IOSIPAD\t10.5.1\tiPad OS\t13.3.1")
except:
    client.login(appName=f"IOSIPAD\t10.4.2\tiPad OS\t13.3.1", showQr=True)
if settings["token"] != client.authToken:
    settings["token"] = client.authToken
oepoll = OEPoll(client)

botsMid = [client.profile.mid]
ghostMid = []
AMT = "#" * 7 + " ANTI JS LOGIN " + "#" * 7
print(AMT)
for i in range(ANTIJS):
    antijs[i+1] = LINE()
    try:
        antijs[i+1].login(settings["antijs"][str(i+1)]["token"], appName=f"IOSIPAD\t10.5.1\tiPad OS\t13.3.1")
    except:
        antijs[i+1].login(appName=f"IOSIPAD\t10.5.1\tiPad OS\t13.3.1", showQr=True)
    if settings["antijs"][str(i+1)]["token"] != antijs[i+1].authToken:
        settings["antijs"][str(i+1)]["token"] = antijs[i+1].authToken
    botsMid.append(antijs[i+1].profile.mid)
    ghostMid.append(antijs[i+1].profile.mid)
print("#" * len(AMT))

for i in range(KICKER):
    kicker[i+1] = LINE()
    tokenOrEmail = settings["kicker"][str(i+1)]["token"]
    idOrAuthToken, passwd = tokenOrEmail if ';;' not in tokenOrEmail else tokenOrEmail.split(";;")[0], None if ';;' not in tokenOrEmail else tokenOrEmail.split(";;")[1]
    try:
        kicker[i+1].login(tokenOrEmail, passwd=passwd, appName="IOSIPAD\t10.5.1\tiPad OS\t13.3.1")
    except Exception as e:
        tokenOrEmail = ''
        print(e)
        kicker[i+1].login(appName="IOSIPAD\t10.5.1\tiPad OS\t13.3.1", showQr=True)
    if not ';;' in tokenOrEmail:
        if settings["kicker"][str(i+1)]["token"] != kicker[i+1].authToken:
            settings["kicker"][str(i+1)]["token"] = kicker[i+1].authToken
    botsMid.append(kicker[i+1].profile.mid)

for ati in antijs:
    allcontacts = antijs[ati].getAllContactIds()
    for mid in botsMid:
        if mid not in allcontacts and mid != antijs[ati].profile.mid:
            print(f"[@] try friend request to {mid}")
            antijs[ati].findAndAddContactsByMid(mid)
            time.sleep(1.5)

for ki in kicker:
    allcontacts = kicker[ki].getAllContactIds()
    for mid in botsMid:
        if mid not in allcontacts and mid != kicker[ki].profile.mid:
            print(f"[@] try friend request to {mid}")
            kicker[ki].findAndAddContactsByMid(mid)
            time.sleep(1.5)

print("[@] Ready to use")

while True:
    try:
        ops = oepoll.long_poll(count=100)
        if ops:
            for op in ops:
                try:
                    execute(op)
                except Exception as e:
                    #print(e)
                    logs.append(str(e))
                    traceback.print_exc()
    except Exception as e:
        traceback.print_exc()
        exit()
