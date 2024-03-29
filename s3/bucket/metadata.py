# read the metadata about the files from the bucket({src_bucket_name}/{src_prefix}) and create a metadata file in the bucket({metadata_bucket_name}/{metadata_prefix}).

import boto3

# soruce bucket
src_bucket_name = ''
src_prefix = ''

# create client
client = boto3.client('s3')
# we cannot get more than 1000 objects without pagination.
paginator = client.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=src_bucket_name, Prefix=src_prefix)

# create metadata details
str = 'file_path,date,time,size' # schema
for page in pages:
    for obj in page['Contents']:
        str = str + f"""\n{obj['Key']},{obj['LastModified'].strftime('%Y-%m-%d')},{obj['LastModified'].strftime('%H:%M:%S')},{obj['Size']}"""

        
# write metadata in a bucket
metadata_bucket_name = ''
metadata_prefix = ''
client.put_object(Body=str, Bucket=metadata_bucket_name, Key=metadata_prefix)
