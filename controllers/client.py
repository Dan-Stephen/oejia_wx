# coding=utf-8
import logging

from werobot.client import Client, ClientException
from werobot.robot import BaseRoBot
from werobot.session.memorystorage import MemoryStorage
from werobot.logger import enable_pretty_logging

from openerp import exceptions

_logger = logging.getLogger(__name__)


class WeRoBot(BaseRoBot):
    pass


WxEnvDict = {}

class WxEntry(object):

    def __init__(self):

        wxclient = Client('appid_xxxxxxxxxxxxxxx', 'appsecret_xxxxxxxxxxxxxx')

        UUID_OPENID = {}

        robot = None

    def send_text(self, openid, text):
        try:
            self.wxclient.send_text_message(openid, text)
        except ClientException, e:
            raise exceptions.UserError(u'发送失败 %s'%e)

    def chat_send(self, db,uuid, msg):
        #_dict = self.UUID_OPENID.get(db,None)
        if UUID_OPENID:
            openid = UUID_OPENID.get(uuid,None)
            if openid:
                self.send_text(openid, msg)
        return -1

    def init(self, env):
        Param = env['ir.config_parameter'].sudo()
        self.wx_token = Param.get_param('wx_token') or ''
        self.wx_appid = Param.get_param('wx_appid') or ''
        self.wx_AppSecret = Param.get_param('wx_AppSecret') or ''

        #robot.config["TOKEN"] = self.wx_token
        wxclient.appid = self.wx_appid
        wxclient.appsecret = self.wx_AppSecret
        # 刷新 AccessToken
        wxclient._token = None
        _ = wxclient.token

        session_storage = MemoryStorage()
        robot = WeRoBot(token=self.wx_token, enable_session=True, logger=_logger, session_storage=session_storage)
        enable_pretty_logging(robot.logger)
        self.robot = robot

def wxenv(env):
    return WxEnvDict[env.cr.dbname]
