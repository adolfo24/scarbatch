#!/usr/bin/python
import boto3
import botocore
from botocore.exceptions import ClientError
import os
import errno
class S3():
    def __init__(self):
        self.client = boto3.client('s3')
    
    def download_bucket(self,bucket):
        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(bucket)
        for object in my_bucket.objects.all():
            print "Object : "+str(object)
            print "key : "+str(object.key)
            path= os.path.dirname(os.path.join("/tmp/input", object.key))
            print "path : "+path
            if not os.path.exists(path):
                try:
                    self._mkdir_recursive(path)
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            my_bucket.download_file(object.key, os.path.join("/tmp/input", object.key))
        print os.listdir('/tmp/input')

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
        
    def _mkdir_recursive(self, path):
        sub_path = os.path.dirname(path)
        if not os.path.exists(sub_path):
            self._mkdir_recursive(sub_path)
        if not os.path.exists(path):
            os.mkdir(path)


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
    

        
        





