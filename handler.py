import os
import boto3
from io import BytesIO
from gzip import GzipFile
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

s3_resource = boto3.resource('s3')
s3 = boto3.client('s3')


def adtr_process(event, context):
    log.debug('Starting adtr_process')
    bucket_name = os.environ['bucket_name']
    log.debug('bucket name loaded.'+bucket_name)
    for item in event['Records']:
        Key = item['s3']['object']['key']
    log.debug('Key loaded')
    object = s3_resource.Object(bucket_name, Key)
    log.debug('object defined')
    try:
        upload_status = 'success'
        object_bytes = object.get()
        log.debug('object get executed')
        #bytestream = BytesIO(object_bytes['Body'].read())
        #log.debug('bytestream created')
        #got_text = GzipFile(None, 'rb', fileobj=bytestream).read().decode('utf-8')
        #log.debug('text gotten / decoded from bytes')
        #with GzipFile(None, 'rb', fileobj=bytestream).read().decode('utf-8') as f:
        log.debug('putting object...')
        s3.put_object(Body=GzipFile(None, 'rb', fileobj=BytesIO(object_bytes['Body'].read())).read().decode('utf-8'),
                      Bucket=bucket_name,
                      Key='unzipped/'+Key[0:-7])
        #response = s3.put_object(
        #        Body=got_text,
        #        Bucket=bucket_name,
        #        Key='unzipped/' + Key[0:-7]
        #    )
        # Create temporary file
        #temp_file = tempfile.mktemp()
        # Fetch and load target file
        #s3.download_file(bucket_name, Key, temp_file)
        #zipdata = zipfile.ZipFile(temp_file)
        log.debug('put_object executed')
    except Exception:
        upload_status = 'fail'
    finally:
        return log.debug(upload_status)
