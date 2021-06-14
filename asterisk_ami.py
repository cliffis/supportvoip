import os
import time
from ami_settings import login, connection
from pg_db import *


from asterisk.ami import AMIClient
from asterisk.ami import EventListener


def event_notification(source, event):
    # os.system('notify-send "%s" "%s"' % (event.name, str(event)))
    print('notify-send "%s" "%s"' % (event.name, str(event)))
    # event_test(event)


def event_listener(event, **kwargs):
    print('New', event['BridgeUniqueid'])
    # print(type(event))
    

def event_talking(event, **kwargs):
    print('New', event['BridgeUniqueid'])
    # print(type(event))
    

def event_test(event, **kwargs):
    # print('notify-send "%s" ---- "%s"' % (event.name, str(event)))
    # print(event['Exten'], event.name, event['ChannelStateDesc'])
    # print(type(event.name))
    try:
        if event['Exten'] == '36861' and event.name == 'Newstate' and event['ChannelStateDesc'] == 'Up':
            print('New if 1:', event['CallerIDNum'], event['CallerIDName'])
            # insert_log_ami(CallerIDNum, CallerIDName, ConfbridgeTalking, TimeStart="no information", TimeEnd="no information")
            insert_log_ami(event['CallerIDNum'], event['CallerIDName'])

        if event.name == 'Hangup' or event.name == 'HangupRequest':
            print('New if 3:', event['CallerIDNum'], event['CallerIDName'])
            delete_log_ami(event['CallerIDNum'], event['CallerIDName'])

        if event['TalkingStatus'] == 'on' or event['TalkingStatus'] == 'off':
            # elif event['ConfbridgeTalking'] and event.name == 'Newstate':
            print('New if 2:', event['CallerIDNum'], event['CallerIDName'], event['TalkingStatus'])
            update_log_ami_talk(event['CallerIDNum'], event['CallerIDName'], event['TalkingStatus'])

        if event.name == 'ConfbridgeEnd':
            print('New if 4:', event['ConfbridgeEnd'])
            delete_all_log_ami()
        # else:
        #     print("no information-----")
    except:
        return
        # print("no information")


client = AMIClient(**connection)
future = client.login(**login)
if future.response.is_error():
    raise Exception(str(future.response))

client.add_event_listener(event_test)
#
# client.add_event_listener(
#     event_listener,
#     white_list='ConfbridgeTalking',
#     # TalkingStatus='on',
#     # TalkingStatus='off',
#     Conference='36861',
# )

# Uniqueid
# ChannelStateDesc': 'Up','CallerIDNum': '21212', 'CallerIDName': 'Seryakov I.V.''Exten': '36861'"Newstate" "Event : Newstate 
# notify-send "HangupRequest" "Event : HangupRequest -> {'Privilege': 'call,all', 'Channel': 'SIP/CUCM_HU_sip-00000010', 'ChannelState': '6', 'ChannelStateDesc': 'Up', 'CallerIDNum': '21212', 'CallerIDName': 'Seryakov I.V.', 'ConnectedLineNum': '<unknown>', 'ConnectedLineName': '<unknown>', 'Language': 'en', 'AccountCode': '', 'Context': 'from-internal', 'Exten': 'STARTMEETME', 'Priority': '5', 'Uniqueid': '1622718857.68', 'Linkedid': '1622718857.68'}"
# notify-send "Hangup" "Event : Hangup -> {'Privilege': 'call,all', 'Channel': 'SIP/CUCM_HU_sip-00000010', 'ChannelState': '6', 'ChannelStateDesc': 'Up', 'CallerIDNum': '21212', 'CallerIDName': 'Seryakov I.V.', 'ConnectedLineNum': '<unknown>', 'ConnectedLineName': '<unknown>', 'Language': 'en', 'AccountCode': '', 'Context': 'from-internal', 'Exten': 'h', 'Priority': '1', 'Uniqueid': '1622718857.68', 'Linkedid': '1622718857.68', 'Cause': '16', 'Cause-txt': 'Normal Clearing'}"



try:
    while True:
        time.sleep(10)
except (KeyboardInterrupt, SystemExit):
    client.logoff()