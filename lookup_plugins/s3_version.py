"""
Get S3 object current version
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase

import boto3
import sys

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        ret = []

        bucket = variables['lambda_bucket_name']
        object_key = terms[0]
        access_key = variables['assumed_role']['sts_creds']['access_key']
        secret_key = variables['assumed_role']['sts_creds']['secret_key']
        security_token = variables['assumed_role']['sts_creds']['session_token']

        s3 = boto3.resource(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=security_token
        )

        # grab the object directly
        s3_object = s3.Object(bucket,object_key)

        # load the object metadata
        s3_object.load()

        # populate the return array
        ret.append( s3_object.version_id )

        return ret

