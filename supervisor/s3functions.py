#!/usr/bin/python
import boto3
import botocore
from botocore.exceptions import ClientError
import os
class S3():
    def __init__(self):
        self.client = boto3.client('s3')
    def download_file(self,bucket,namefile):
        try:
            self.client.download_file(bucket, namefile,os.environ['SCAR_INPUT_DIR']+"/"+namefile)
            return namefile
        except ClientError as ce:
            error_msg = "Error register job definition."
            print error_msg, error_msg + ": %s" % ce
            raise ce 


if __name__ == "__main__":
    s3 = S3()
    s3.download_file("pruebascar","myjob.sh")
    if not os.path.exists(os.environ['SCAR_INPUT_DIR']):
        os.makedirs(os.environ['SCAR_INPUT_DIR'])
    with open(os.path.join(os.environ['SCAR_INPUT_DIR'],"script.sh"), "w") as file1:
        file1.write(os.environ['SCRIPT'])
        file1.close()
    os.system('chmod +x '+os.environ['SCAR_INPUT_DIR']+"/script.sh")


