
from core.token.RtcTokenBuilder import RtcTokenBuilder, Role_Subscriber, Role_Publisher
from core.token.RtmTokenBuilder import RtmTokenBuilder, Role_Rtm_User
import time
from django.conf import settings
import random

appID = settings.APP_ID
appCertificate = settings.APP_CERTIFICATE
expireTimeInSeconds = 60*3


def rtc(channelName, uid, role):
    privilegeExpiredTs = int(time.time()) + expireTimeInSeconds
    if role == 1:
        token = RtcTokenBuilder.buildTokenWithUid(
            appID, appCertificate, channelName, uid, Role_Publisher, privilegeExpiredTs)
    else:
        token = RtcTokenBuilder.buildTokenWithUid(
            appID, appCertificate, channelName, uid, Role_Subscriber, privilegeExpiredTs)
    return token


def rtm(user):
    privilegeExpiredTs = int(time.time()) + expireTimeInSeconds
    token = RtmTokenBuilder.buildToken(
        appID, appCertificate, user, Role_Rtm_User, privilegeExpiredTs)
    return token


def get_tokens(channelName, role, username):
    uid = random.randint(0, 2294967295)
    suid = random.randint(0, 2294967295)
    if role == 1:
        return {
            'status': 200,
            'usertype': 1,
            'rtm': rtm(username),
            'rtc': rtc(channelName, uid, role),
            'screen_rtc': rtc(channelName, suid, role),
            'uid': uid,
            'suid': suid,
            'channel': channelName
        }
    else:
        return {
            'status': 200,
            'rtm': rtm(username),
            'rtc': rtc(channelName, uid, role),
            'uid': uid,
            'usertype': 0,
            'channel': channelName
        }
