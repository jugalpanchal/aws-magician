# read the metadata about the files from the bucket({src_bucket_name}/{src_prefix}) and create a metadata file in the bucket({metadata_bucket_name}/{metadata_prefix}).

import boto3

# soruce bucket
src_bucket_name = ''
src_prefix = ''

# create client and pages
client = boto3.client('s3')
paginator = client.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=src_bucket_name, Prefix=prefix)

# create metadata details
str = 'file_name,date,size' # schema
for page in pages:
    for obj in page['Contents']:
        str = str + f"""\n{obj['Key']},{obj['LastModified'].strftime('%Y-%m-%d')},{obj['Size']}"""

        
# write metadata in a bucket
metadata_bucket_name = ''
metadata_prefix = ''
client.put_object(Body=str, Bucket=metadata_bucket_name, Key=metadata_prefix)
