#!/usr/bin/python
import boto3
import botocore
from botocore.exceptions import ClientError
import os
class S3():
    def __init__(self):
        self.client = boto3.client('s3')
    
    def download_bucket(self,bucket):

        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(bucket)
        for object in my_bucket.objects.all():
            print str(os.path.join(os.curdir, object.key))
            my_bucket.download_file(object.key, "/tmp/imput"+os.path.join(os.curdir, object.key))
        print os.listdir('/tmp/imput')

    def download_file(self,bucket,namefile):
        try:
            self.client.download_file(bucket, namefile,os.environ['SCAR_INPUT_DIR']+"/"+namefile)
            return namefile
        except ClientError as ce:
            error_msg = "Error download file to S3."
            print error_msg, error_msg + ": %s" % ce
            raise ce
    def uploadDirectory(self,path,bucketname):
        try:
            for root,dirs,files in os.walk(path):
                for file in files:
                    key= "/tmp/"+os.environ['REQUEST_ID']+"/output/"+file
                    self.client.put_object(Bucket=bucketname,Key=key,Body=file)
        except ClientError as ce:
            error_msg = "Error upload file to S3."
            print error_msg, error_msg + ": %s" % ce
            raise ce
        


if __name__ == "__main__":
    s3 = S3()
    if(os.environ['MODE']=="INIT"):
        with open(os.path.join(os.environ['SCAR_INPUT_DIR'],"script.sh"), "w") as file1:
            file1.write(os.environ['SCRIPT'])
            file1.close()
        os.system('chmod +x '+os.environ['SCAR_INPUT_DIR']+"/script.sh")
        print 'BUCKET_INPUT: '+str(os.environ['BUCKET_INPUT'])
        if (os.environ['BUCKET_INPUT']!=""):
            s3.download_bucket(os.environ['BUCKET_INPUT'])
    elif(os.environ['MODE']=="FINISH"):
        if (os.environ['BUCKET_OUTPUT']!=""):
            s3.uploadDirectory("/tmp/output", os.environ['BUCKET_OUTPUT'])
        
        





