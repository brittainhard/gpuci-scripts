import boto3
from botocore.exceptions import ClientError
import datetime
import dateutil
from secrets import *

AMI = "ami-a9d09ed1"
SECURITY_GROUP = "sg-0bfaf68638765cb9f"
EIP = "eipalloc-05cac4bd27006b123"
INSTANCE_SIZE = "t2.micro"

session = boto3.Session(
    aws_access_key_id=key_id,
    aws_secret_access_key=key,
    region_name=region
)


def running(instance):
    return instance.state["Code"] == 16


def created_on(instance):
    return instance.launch_time


def time_difference(instance):
    td = created_on(instance)
    tm = datetime.datetime.now(tz=dateutil.tz.tz.tzutc()) - td
    hours, remainder = divmod(tm.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return datetime.time(minute=minutes, second=seconds)


def close_to_next_hour(time):
    return 60 - time.minute <= 2


def get_gpu_instance(instances):
    for x in instances:
        print(x.image.id)
        if x.image.id == AMI:
            return x
    return None


def attach_elastic_ip(instance):
	try:
		response = cl.associate_address(AllocationId=EIP,
										 InstanceId=instance.id)
		print(response)
	except ClientError as e:
		print(e)


def get_running_instances(instances):
    running_instances = []
    for x in instances:
        if running(x):
            running_instances.append(x)
    return running_instances


def terminate_instance(instance):
    instance.terminate()


def create_instance():
    instances = ec2.create_instances(
        ImageId=AMI,
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[SECURITY_GROUP],
        InstanceType=INSTANCE_SIZE,
    )
    return instances
     

ec2 = session.resource("ec2")
cl = session.client("ec2")
instances = list(ec2.instances.iterator())
a = get_gpu_instance(instances)
