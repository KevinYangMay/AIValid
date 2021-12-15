import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
from flask import Flask,url_for,redirect,render_template,request,send_from_directory,jsonify
# 解决腾讯自签名证书问题 message:[SSL: CERTIFICATE_VERIFY_FAILED]
import ssl
ssl._create_default_https_context=ssl._create_unverified_context

app=Flask(__name__,template_folder='./web/dist',static_folder='./web/dist',static_url_path="")
# app=Flask(__name__)


def IDCardOCR(SecretId,SecretKey,img,op_code):
    try:
        cred = credential.Credential(SecretId,SecretKey)
        # (SecretId,SecretKey) 里面填写的值
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)
        req=''
        params = {
            "ImageBase64": img,
            }
        if op_code=='idCard':
            req = models.IDCardOCRRequest()
            params['CardSide']='FRONT'
            req.from_json_string(json.dumps(params))
            resp = client.IDCardOCR(req)
        if op_code=='bankCard':
            req = models.BankCardOCRRequest()
            req.from_json_string(json.dumps(params))
            resp = client.BankCardOCR(req)
        print(resp.to_json_string())
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        print(err)


@app.route('/')
def home():
  print('111111')  
  return render_template('index.html')


@app.route('/AIcheck', methods=['GET', 'POST'])
def AIcheck():
    print('进入')
    query=request.get_json(silent=True)
    img=query['imgBase64']
    op_code=query['op_code']
    SecretId='AKIDZx5xbz6vVnpa5JGxOZT6SYNvCCvNZVBa'
    SecretKey='91cx1pOghRv96mBLEqBG4QVLuBCwQIzQ'
    result=IDCardOCR(SecretId,SecretKey,img,op_code)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5431)