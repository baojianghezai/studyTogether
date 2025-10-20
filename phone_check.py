import configparser
import os
import sys

from typing import List

from alibabacloud_dypnsapi20170525.client import Client as Dypnsapi20170525Client
from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dypnsapi20170525 import models as dypnsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient


class Sample_check:
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
        config_reader.read('./config.ini',encoding='utf-8')
        # 获取所有section
        sections = config_reader.sections()
        if 'AK' in sections:
            AK_ID = config_reader.get('AK','ALIYUN_ACCESS_KEY_ID_M')
            AK_SK = config_reader.get('AK','ALIYUN_ACCESS_KEY_SECRET_M')
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
        vriCode: str,
    ) -> str | None:
        client = Sample_check.create_client()
        check_sms_verify_code_request = dypnsapi_20170525_models.CheckSmsVerifyCodeRequest(
            phone_number=phoneNum,
            verify_code=vriCode
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = client.check_sms_verify_code_with_options(check_sms_verify_code_request, runtime)
            ConsoleClient.log(UtilClient.to_jsonstring(resp))
            return UtilClient.to_jsonstring(resp)

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
        client = Sample_check.create_client()
        check_sms_verify_code_request = dypnsapi_20170525_models.CheckSmsVerifyCodeRequest()
        runtime = util_models.RuntimeOptions()
        try:
            resp = await client.check_sms_verify_code_with_options_async(check_sms_verify_code_request, runtime)
            ConsoleClient.log(UtilClient.to_jsonstring(resp))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)