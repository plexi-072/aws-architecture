import boto3
import time
from botocore.client import ClientError
from datetime import datetime, timedelta, tzinfo

ec2 = boto3.client('ec2')

instances = ["InstansIds"]
image_prefix = "backup_"


def lambda_handler(event, context):
    for instance in instances:
        create_image(image_prefix + tag_name(instance), instance)


def create_image(prefix, instanceid):
    imagename = "_".join([prefix, datetime.now().strftime("%Y-%m-%d")])

    try:
        # create image noreboot
        response = ec2.create_image(
            InstanceId=instanceid,
            Name=imagename,
            Description='created automatically by Lambda',
            NoReboot=True,
        )
        return
    except ClientError as e:
        print(str(e))


def tag_name(instance_id):
    tags = ec2.describe_instances(InstanceIds=[instance_id])
    for tag in tags['Reservations'][0]['Instances'][0]['Tags']:
        if tag['Key'] == 'Name':
            return tag['Value']
        else:
            return instance_id