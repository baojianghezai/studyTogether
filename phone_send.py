import os
import sys
import configparser
from typing import List

from alibabacloud_dypnsapi20170525.client import Client as Dypnsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dypnsapi20170525 import models as dypnsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient


class Sample_send:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dypnsapi20170525Client:
        """
        使用凭据初始化账号Client
        @return: Client
        @throws Exception
        """
        config_reader = configparser.ConfigParser()
        config_reader.read('config.ini',encoding='utf-8')
        # 获取所有section
        sections = config_reader.sections()
        print('sections = ', sections)
        AK_ID=''
        AK_SK=''
        if 'AK' in sections:
            AK_ID = config_reader.get('AK','ALIYUN_ACCESS_KEY_ID_M')
            AK_SK = config_reader.get('AK','ALIYUN_ACCESS_KEY_SECRET_M')
            print('AK_ID = ', AK_ID , '\nAK_SK = ',AK_SK)
        config = open_api_models.Config(
            type='access_key',
            access_key_id=AK_ID,
            access_key_secret=AK_SK,
            region_id='cn-qingdao'
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dypnsapi
        config.endpoint = f'dypnsapi.aliyuncs.com'
        return Dypnsapi20170525Client(config)

    @staticmethod
    def main(
        phoneNum: str,
    ) -> None:
        client = Sample_send.create_client()
        send_sms_verify_code_request = dypnsapi_20170525_models.SendSmsVerifyCodeRequest(
            sign_name='速通互联验证码',
            phone_number=phoneNum,
            template_code='100001',
            template_param='{"code":"##code##","min":"5"}'
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = client.send_sms_verify_code_with_options(send_sms_verify_code_request, runtime)
            ConsoleClient.log(UtilClient.to_jsonstring(resp))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample_send.create_client()
        send_sms_verify_code_request = dypnsapi_20170525_models.SendSmsVerifyCodeRequest(
            sign_name='速通互联验证码',
            phone_number='17616591386',
            template_code='100001',
            template_param='{"code":"##code##","min":"5"}'
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = await client.send_sms_verify_code_with_options_async(send_sms_verify_code_request, runtime)
            ConsoleClient.log(UtilClient.to_jsonstring(resp))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
