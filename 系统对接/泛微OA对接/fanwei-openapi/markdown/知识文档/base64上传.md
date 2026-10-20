# base64上传

- **文档 ID**: `220355033999343616`
- **业务模块**: 知识文档
- **是否 API 接口**: 是
- **请求 URL**: `{OpenApiOrigin}/api/file/v2/common/upload/base64`
- **请求方式**: `POST`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| access_token | 是 | String | 调用接口凭证 获取accessToken信息 |

## 返回参数

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| userid | long | 用户Id |
| base64 | string | 附件BASE64编码内容 |
| name | string | 指定上传的附件在OA中的名称 |
| module | string | 所属模块(常见module列表） |
| createDocument | boolean | true:生成文档，false:不生成文档（值传入true时会结合folderId参数值在文档模块对应目录下生成文档，module=document时folderId必传，module是其他模块时如果没有folderId会生成在系统知识库模块目录下） |
| createDocContent | boolean | true:生成正文类型文档，false:不生成正文类型文档（生效前置条件需要createDocument为true，且仅支持pdf,ofd,wps,office格式文件） |
| folderId | long | 文档文件夹目录（前置生效条件需要createDocument值为true否则该参数没有意义，如果folderId不传且createDocument值为true会根据module传入的值在文档模块系统知识库对应module的目录下生成文档） |
| refId | long | 模块关联的业务ID（如当前附件属于流程模块上传，此处值就是流程的ID值） |
