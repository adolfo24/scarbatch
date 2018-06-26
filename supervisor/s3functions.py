#!/usr/bin/python
import boto3
import botocore
from botocore.exceptions import ClientError
import os
class S3(object):

    def __init__(self):
        self.client = boto3.client(
                's3',   
                aws_access_key_id=os.environ['KEY_ID'],
                aws_secret_access_key=os.environ['SECRET_KEY']
            )
    def download_file(self,bucket,namefile):
        try:
            self.client.download_file(bucket, namefile,"/data/"+namefile)
            return namefile
        except ClientError as ce:
            error_msg = "Error register job definition."
            print error_msg, error_msg + ": %s" % ce
            raise ce 


if __name__ == "__main__":    
    S3().download_file(os.environ['BUCKET'],os.environ['FILE_NAME'])
    if (os.environ['TYPE']=="script"):
        os.system('chmod +x /data/'+os.environ['FILE_NAME'])


