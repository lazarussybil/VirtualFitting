# -*- coding=utf-8
#!/usr/bin/env python3
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys,getopt
import logging
from PIL import Image

def upload_cos(path,filename):
    # 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    secret_id = 'AKIDRcs1zfaxa0Ebjb8yJRIyYv2HFyRfLhW4'      # 替换为用户的 secretId
    secret_key = 'e1GG4cy66pKcgXBSWSpxlV1KvRoPluqV'      # 替换为用户的 secretKey
    region = 'ap-shanghai'     # 替换为用户的 Region
    token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
    scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)

    # 2. 获取客户端对象
    client = CosS3Client(config)

    # 3. Uploading Example
    response = client.upload_file(
        Bucket='csc4001-1258905014',
        LocalFilePath=path,
        Key=filename,
        PartSize=1,
        MAXThread=10,
        EnableMD5=False
    )
    print(response['ETag'])

def binary_upload_cos(body,filename):
    # 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    secret_id = 'AKIDRcs1zfaxa0Ebjb8yJRIyYv2HFyRfLhW4'      # 替换为用户的 secretId
    secret_key = 'e1GG4cy66pKcgXBSWSpxlV1KvRoPluqV'      # 替换为用户的 secretKey
    region = 'ap-shanghai'     # 替换为用户的 Region
    token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
    scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)

    # 2. 获取客户端对象
    client = CosS3Client(config)

    # 3. Uploading Example
    response = client.put_object(
        Bucket='csc4001-1258905014',
        Body=body,
        Key=filename,
        StorageClass='STANDARD',
        EnableMD5=False
    )
    print(response['ETag'])

def download_cos(filename):
    # 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    secret_id = 'AKIDRcs1zfaxa0Ebjb8yJRIyYv2HFyRfLhW4'      # 替换为用户的 secretId
    secret_key = 'e1GG4cy66pKcgXBSWSpxlV1KvRoPluqV'      # 替换为用户的 secretKey
    region = 'ap-shanghai'     # 替换为用户的 Region
    token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
    scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)

    # 2. 获取客户端对象
    client = CosS3Client(config)

    # 3. Download Example
    response = client.get_object(
        Bucket='csc4001-1258905014',
        Key=filename,
    )
    fp = response['Body'].get_raw_stream()
    img = Image.open(fp)
    return img

if __name__ == "__main__":
    upload(sys.argv[1],sys.argv[1])
