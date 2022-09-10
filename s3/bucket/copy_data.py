import sys

import botocore
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SQLContext
from awsglue.job import Job
import re

import datetime
import pytz
from datetime import timedelta

import boto3
from boto3.s3.transfer import TransferConfig, S3Transfer
from botocore.config import Config

# create context objects
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
sqlContext = SQLContext(sc)

# configs
boto_config = Config(
    connect_timeout=300,
    read_timeout=300,
    retries=dict(
        max_attempts=10
    )
)
transfer_config = TransferConfig(
    multipart_chunksize=1024 * 1024 * 25,
    multipart_threshold=1024 * 1024 * 25
)
extra_args = {
    # 'ServerSideEncryption': 'aws:kms',
    # 'SSEKMSKeyId': output_kms,
    'ACL': 'bucket-owner-full-control'
}

# s3 pointer
s3 = boto3.resource('s3', region_name='us-east-2', config=boto_config)

# source and target bucket names
src_bucket_name = 'bucket-source'
trg_bucket_name = 'bucket-target'

# source and target bucket pointers
s3_src_bucket = s3.Bucket(src_bucket_name)
print('Source Bucket Name : {0}'.format(s3_src_bucket.name))
s3_trg_bucket = s3.Bucket(trg_bucket_name)
print('Target Bucket Name : {0}'.format(s3_trg_bucket.name))

# source and target directories
src_dir = 'request'
trg_dir = 'response'

# source and target objects with filters
s3_src_bucket_objs = s3_src_bucket.objects.all()
#s3_src_bucket_objs = s3_src_bucket.objects.filter(Prefix=src_dir) non-prod
#s3_trg_bucket_objs = s3_trg_bucket.objects.filter(Prefix=trg_dir)

# Request file name prefix
file_prefix = 'api_request'

# regex to filter files. damn it doesn't work, will check later.
#rx = re.compile(r'request/.+?'+file_prefix+'.*')

# datetime zone
#local_tz = pytz.timezone("America/Detroit")
#naive = datetime.datetime.strptime("2020-6-3 13:32:12", "%Y-%m-%d %H:%M:%S")
#local_dt = local_tz.localize(naive, is_dst=None)
#print('local_dt : {0}'.format(local_dt))

# filter - start and end date
start_date = datetime.datetime.strptime("2022-01-01", "%Y-%m-%d").replace(tzinfo=None)
end_date = datetime.datetime.strptime("2022-12-31", "%Y-%m-%d").replace(tzinfo=None)

# iterates each source directory
for iterator_obj in s3_src_bucket_objs:
    file_path_key = iterator_obj.key
    date_key = iterator_obj.last_modified.replace(tzinfo=None)
    if start_date <= date_key <= end_date and file_prefix in file_path_key:
        #print('Directory Name: {0} and Date : {1}'.format(file_path_key, iterator_obj.last_modified))
        #file_content = iterator_obj.get()['Body'].read()
        #print(file_content)

        # api request file name. It start with value of file_prefix.
        src_file_name = file_path_key.split('/')[-1].uuid.uuid4()

        # construct target directory path
        trg_dir_path = '{0}/datekey={1}'.format(trg_dir, date_key.date())

        # check if directory exist or not
        #s3.Object(trg_bucket_name, dateKeyDir).load()

        # source file
        src_file_ref = {
            'Bucket': src_bucket_name,
            'Key': file_path_key
        }

        # target file path
        trg_file_path = '{0}/{1}'.format(trg_dir_path, src_file_name)

        # copy source file to target
        #s3.meta.client.copy(copy_source, trg_bucket_name, copy_target)
        trg_new_obj = s3_trg_bucket.Object(trg_file_path)
        trg_new_obj.copy(src_file_ref, ExtraArgs=extra_args, Config=transfer_config)



