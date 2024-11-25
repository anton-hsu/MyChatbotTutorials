# \[MyChatbot\]\[API\] 檔案上傳流程

MyChatbot使用時的第一個步驟是要上傳檔案，檔案上傳了才能選擇已經上傳的檔案來建立知識庫。
上傳檔案可用HTTP REQUEST或是S3。
使用HTTP上傳會有續傳的問題所以建議使用 S3，請參考[Sample Code](https://github.com/anton-hsu/MyChatbotTutorials/blob/main/Knowledge_SampleCode.py)。

* [/api/vl/datasets/{datasetId}/documents/create_by_upload](https://afs-mychatbot-api.twcc.ai/api/v1/docs/ffm-knowledge-management#/documents/DocumentHttpController_createDocumentByUpload)
這個API實作了file upload + create by file，是利用 HTTP 上傳檔案時使用的 API，如果使用 S3 並不需要使用這隻API來建立知識庫。
* [/api/vl/datasets/{datasetId}/documents/create_by_file](https://afs-mychatbot-api.twcc.ai/api/v1/docs/ffm-knowledge-management#/documents/DocumentHttpController_createDocuemntByFile)
已經使用 S3 上傳後會需要利用 file import 後拿到的 file_id 打 create_by_file 這隻 API來建立知識庫。

## MyChatbot 使用S3-Compatible API上傳檔案

1. MyChatbot使用時的第一個步驟是要上傳檔案。底層設計建議使用S3 API上傳。
2. 要使用S3上傳需要先拿到 access / secret key。這個access / secret key 必需經特定的API取得。
   請參考[Sample Code](https://github.com/anton-hsu/MyChatbotTutorials/blob/main/Knowledge_SampleCode.py)實作。

3. 透過S3上傳以後會需要客戶把檔案放到 system 的 bucket 底下 

      a. S3是aws標準的protocol, api用法可以參考[AWS網站](https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_Amazon_Simple_Storage_Service.html), 前端通常會用AWS SDK來實作。
      b. S3 操作通常使用的API參考如下
         - [s3 List Buckets](https://github.com/aws/aws-sdk-js-v3/tree/main/clients/client-s3#v2-compatible-style) ( API : s3.listBuckets)
         - [s3 List Objects](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/S3.html#listObjectsV2-property) (API : s3.listObjectsV2)
         - [s3 Upload Objects](https://github.com/aws/aws-sdk-js-v3/tree/main/lib/lib-storage)

4. 接著是用[MyChatbot Knowledge API](https://afs-mychatbot-api.twcc.ai/api/v1/docs/ffm-knowledge-management#/)，用 file import 的 API([/api/v1/files/import](https://afs-mychatbot-api.twcc.ai/api/v1/docs/ffm-knowledge-management#/files/FileHttpController_importFiles)) 把檔案轉移到 MyChatbot/Knowledge 模組下管理

    a. 這邊 /api/v1/files/import 填的 subpath 就會是檔案放在 system 底下的路徑，如果檔案放在根目錄那麼 subpath 就給空的值
    b. 我們會建議集中放在一個 folder 底下比較方便管理
例如檔案放在 upload 的 folder 底下那 subpath 就給 "upload" (開頭不帶斜線)
如果放在 upload/knowledge 底下那 subpath 就給 "upload/knowledge"

5. 檔案import至MyChatbot Knowledge中，即可使用 [create_by_file](https://afs-mychatbot-api.twcc.ai/api/v1/docs/ffm-knowledge-management#/documents/DocumentHttpController_createDocuemntByFile) 這隻 API來建立知識庫

6. 如果想透過HTTP REQUEST的方式上傳，可以直接使用 [create_by_upload](https://afs-mychatbot-api.twcc.ai/api/v1/docs/ffm-knowledge-management#/documents/DocumentHttpController_createDocumentByUpload)，指定要上傳的datasetid即可。

7. 透過以上步驟將檔案import至MyChatbot 知識庫後，會需要再打[reindex API](https://afs-mychatbot-api.twcc.ai/api/v1/docs/ffm-knowledge-management#/documents/DocumentHttpController_reindexDocument)讓系統將該檔案向量化並存至向量資料庫中。


