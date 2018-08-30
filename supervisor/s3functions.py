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
    def uploadDirectory(path,bucketname):
        for root,dirs,files in os.walk(path):
            for file in files:
                self.client.upload_file(os.path.join(root,file),bucketname,file)


if __name__ == "__main__":
    s3 = S3()
    if(os.environ['MODE']=="INIT"):
        with open(os.path.join(os.environ['SCAR_INPUT_DIR'],"script.sh"), "w") as file1:
            file1.write(os.environ['SCRIPT'])
            file1.close()
        os.system('chmod +x '+os.environ['SCAR_INPUT_DIR']+"/script.sh")
    elif(os.environ['MODE']=="FINISH"):
        s3.uploadDirectory("/tmp",os.environ['BUCKET'])






