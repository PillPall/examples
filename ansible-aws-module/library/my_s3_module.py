#!/usr/bin/python
# Copyright (c) 2018 COPYRIGHT
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}
DOCUMENTATION = '''
---
module: my_s3_module
MODULE_DESCRIPTION
requirements:
  - boto3 >= 1.5.0
  - python >= 2.6.0

options:
    s3_bucket:
        description:
          - Name of the S3 Bucket
        required: true
        default: null
    s3_prefix:
      description:
        - Location of the file in the s3 Bucket
      required: true
      default: null
    local_dest:
      description:
        - Local path to store / upload a s3 object
      required: true
      default: /tmp
    mode:
      description:
        - Behaviour of our Ansible module
      required: true
      default: null
      choices: ['download', 'upload']
'''
EXAMPLES = '''
- name: Download a s3 object
  aws_s3_download:
    s3_bucket: mbloch
    s3_prefix: test/hello.txt
    local_dest: ~/hello.txt
    mode: download
  register: dl_output

- name: Upload a s3 object
  aws_s3_download:
    region: ap-southeast-2
    aws_secret_key: MYSecretKey
    aws_access_key: MyAccessKey
    s3_bucket: mbloch
    s3_prefix: test/world.txt
    local_dest: ~/world.txt
    mode: upload
  register: ul_output
'''
RETURN = '''
dest:
    description: Destination path of your downloaded/uploaded file
    returned: (s3://)(/)path/to/download/or/upload
    type: String
    sample: /tmp/hello.txt

source:
    description: Source path of your downloaded/uploaded file
    returned: (s3://)(/)path/to/download/or/upload
    type: String
    sample: /tmp/hello.txt

message:
    descripton: return value of our s3 upload/download
    return: null
    type: null
    sample: null
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ec2 import ansible_dict_to_boto3_tag_list, AnsibleAWSError, boto3_conn, connect_to_aws, ec2_argument_spec, get_aws_connection_info
import traceback

try:
    import boto3
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

def download(s3_connection, module):

    s3_bucket = module.params.get('s3_bucket')
    s3_prefix = module.params.get('s3_prefix')
    local_dest = module.params.get('local_dest')

    try:
        s3_bucket_connection = s3_connection.Bucket(s3_bucket)
        result = s3_bucket_connection.download_file(s3_prefix, local_dest)
        response = dict(changed=True,
                        item=dict(source='s3://' + s3_bucket + '/' + s3_prefix,
                                  dest=local_dest),
                        message=result)
        return response
    except Exception as e:
        module.fail_json(msg="Error: Can't download file from s3 - " + str(e), exception=traceback.format_exc(e))

def upload(s3_connection, module):
    s3_bucket = module.params.get("s3_bucket")
    s3_prefix = module.params.get("s3_prefix")
    local_dest = module.params.get("local_dest")

    try:
        s3_bucket_connection = s3_connection.Bucket(s3_bucket)
        result = s3_bucket_connection.upload_file(local_dest, s3_prefix)
        response = dict(changed=True,
                        item=dict(source=local_dest,
                                   dest='s3://' + s3_bucket + '/' + s3_prefix),
                        message=result)
        return response
    except Exception as e:
        module.fail_json(msg="Error: Can't upload configuration file - " + str(e), exception=traceback.format_exc(e))

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(
        s3_bucket = dict(required=True, type='str'),
        s3_prefix = dict(required=True, type='str'),
        local_dest = dict(default='/tmp/', type='str'),
        mode = dict(required=True, type='str', choices=['download', 'upload']),
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_BOTO:
        module.fail_json(msg='boto3 required for this module')

    region, ec2_url, aws_connect_params = get_aws_connection_info(module, boto3=True)

    if not region:
        module.fail_json(msg='region must be specified')

    conn_type = 'resource'
    resource = 's3'

    try:
        s3_connection = boto3_conn(module, conn_type=conn_type,
                resource=resource, region=region,
                endpoint=ec2_url, **aws_connect_params)
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg='cannot connect to AWS', exception=traceback.format_exc(e))

    mode = module.params.get("mode")

    if mode == 'download':
        result = download(s3_connection, module)
    elif mode == 'upload':
        result = upload(s3_connection, module)
    else:
        module.fail_json(msg='Error: unsupported state. Supported states are download and upload')

    module.exit_json(**result)

if __name__ == '__main__':
    main()
