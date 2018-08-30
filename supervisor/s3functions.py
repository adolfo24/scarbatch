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
    def upload_directory():
    for root, dirs, files in os.walk(os.environ['SCAR_OUTPUT_DIR']):
        nested_dir = root.replace(os.environ['SCAR_OUTPUT_DIR'], '')
        if nested_dir:
            nested_dir = nested_dir.replace('/','',1) + '/'

        for file in files:
            complete_file_path = os.path.join(root, file)
            file = nested_dir + file if nested_dir else file
            print "[S3_UPLOAD] Going to upload {complete_file_path} to s3 bucket {s3_bucket} as {file}"\
                .format(complete_file_path=complete_file_path, s3_bucket="pruebascar", file=file)
            s3_client.upload_file(complete_file_path, "pruebascar", file)


if __name__ == "__main__":
    s3 = S3()
    if(os.environ['MODE']=="INIT"):
        with open(os.path.join(os.environ['SCAR_INPUT_DIR'],"script.sh"), "w") as file1:
            file1.write(os.environ['SCRIPT'])
            file1.close()
        os.system('chmod +x '+os.environ['SCAR_INPUT_DIR']+"/script.sh")
    elif(os.environ['MODE']=="FINISH"):
        s3.upload_directory()






