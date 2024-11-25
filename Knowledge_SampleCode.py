#!/usr/bin/env python
# coding: utf-8

# In[1]:

# ver 1.0 created by ASUS OCIS team
# Author: Scott
# Revised: Anton

import requests
import json
import boto3

# apiKey 輸入在MyChatbot平台右上角取得的"APP金鑰"
# projectId 輸入在MyChatbot平台左上角選擇專案處，copy欲使用專案的project id  
apiKey = 'YOUR_API_KEY'
projectId = 'YOUR_PROJECT_ID'
url = 'https://afs-mychatbot-api.twcc.ai' # 台智雲上的MyChatbot服務url，若是獨立另外部署的MyChatbot以及使用企業自己的domain請務必修改
storageUrl = 'https://afs-mychatbot-storage.twcc.ai' # 台智雲上的MyChatbot服務url，若是獨立另外部署的MyChatbot以及使用企業自己的domain請務必修改

headers = {'authorization': 'Bearer ' + apiKey,
          'x-iam-project-id': projectId,
          'Content-Type': 'application/json'}

# get S3 access key and secret key
r = requests.get(url + '/iam/api/v1/credential/project/' + projectId, headers=headers)
s3Key = r.json()
print(s3Key)





# upload file to S3

bucketName='system'
fileName='YOUR FILE' # 欲上傳的檔案，預設放在執行程式同樣的目錄下
s3Client = boto3.client('s3', 
    endpoint_url=storageUrl,
    aws_access_key_id=s3Key['accessKey'],
    aws_secret_access_key=s3Key['secretKey'],
    aws_session_token=None,
    config=boto3.session.Config(signature_version='s3v4'),
    verify=True
)

s3Client.upload_file('./' + fileName, bucketName, '/upload/' + fileName)
objects= s3Client.list_objects(Bucket=bucketName, Prefix='/upload')['Contents']
for obj in objects:
  print(obj['Key'])


# create knowledge datasets


datasetName = 'test_python' 
payload = json.dumps({
  "name": "test_python", # dataset name you want to create, same as above datasetName variable
  "description": "description test_python",
  "type": "knowledge",
  "embeddingSetting": {
    "separators": [
      "\n"
    ],
    "chunkSize": 800, # chunk size, depends on your document type, find your best chunk size by test
    "chunkOverlap": 50,
    "model": "ffm"
  },
  "retrievalSetting": {
    "topK": 15,
    "enableScoreThreshold": True,
    "enableRerank": True,
    "scoreThreshold": 0.2,
    "rerankTopK": 8
  },
  "files": [], 
  "texts": [],
  "urls": []
})
datasets = requests.get(url + '/api/v1/datasets', headers=headers).json()
datasetId=''
for dataset in datasets:
    if dataset['name'] == datasetName:
        datasetId=dataset['id']
        break
if datasetId == '':
    r = requests.request("POST", url + '/api/v1/datasets', headers=headers, data=payload)
    datasetId=r.json()['id']
print(datasetId)


# import file from S3 to knowledge


payload = json.dumps({
  "files": [
    {
      "fileName": fileName,
      "subpath": "upload"
    }
  ]
})

r = requests.request("POST", url + '/api/v1/files/import', headers=headers, data=payload)
data = r.json()
fileId = data[0]['id']
print(fileId)


# add file to knowledge dataset


payload = json.dumps({
  "fileId": fileId,
  "embeddingSetting": {
    "separators": [
      "\n"
    ],
    "chunkSize": 800,
    "chunkOverlap": 50
  }
})

r = requests.request("POST", url + '/api/v1/datasets/' + datasetId + '/documents/create_by_file', headers=headers, data=payload)
data = r.json()

print(data)




# %%
