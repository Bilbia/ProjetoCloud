import boto3
from instances import create_instance, delete_instances
from securitygroups import create_security_group, delete_security_group
from images import create_image, delete_image, launch_image, delete_launch_image
from loadbalancer import create_loadbalancer, delete_loadbalancer
from targetgroup import create_target_group, delete_target_group
from autoscalling import create_auto_scalling, delete_auto_scalling, attach_loadbalancer, create_auto_scalling_policy
from listener import create_listener
from instancescripts import *
from permissions import *

POSTGRES_SECURITY__GROUP = "Postgres_Security_Group"
DJANGO_SECURITY_GROUP = "Django_Security_Group"
POSTGRES_INSTANCE_NAME = "bilbia_postgres_ohio"
DJANGO_INSTANCE_NAME = "bilbia_django_north_virginia"
DJANGO_IMAGE_NAME = "django_image"
DJANGO_TARGET_GROUP_NAME = "django-target-group"
LOADBALANCER_NAME = "bilbia-loadbalancer"
LAUNCH_CONFIG_NAME = "django_launch_config"
AUTO_SCALLING_NAME = "django-auto-scalling"
AUTO_SCALLING_POLICY_NAME = "django-auto-scalling-policy"
AMI_OHIO = "ami-020db2c14939a8efb"
AMI_NORTH_VIRGINIA = "ami-0279c3b3186e54acd"
OHIO_REGION = "us-east-2"
NORTH_VIRGINIA_REGION = "us-east-1"






# ec2 clients
ohio_resource = boto3.client('ec2', region_name=OHIO_REGION)
north_virginia_resource = boto3.client('ec2', region_name=NORTH_VIRGINIA_REGION)
loadbalancer_resource = boto3.client('elbv2', region_name=NORTH_VIRGINIA_REGION)
auto_scalling_resource = boto3.client('autoscaling', region_name=NORTH_VIRGINIA_REGION)

# ==================================
# DELETING EVERYTHING BEFORE RUNNING

# deleting loadbalancers
delete_loadbalancer(loadbalancer_resource, LOADBALANCER_NAME)

# deleting auto scalling
delete_auto_scalling(auto_scalling_resource, AUTO_SCALLING_NAME)

# deleting image
delete_image(north_virginia_resource, DJANGO_IMAGE_NAME)

# deleting launched image config
delete_launch_image(auto_scalling_resource, LAUNCH_CONFIG_NAME)

# deleting instances
delete_instances(ohio_resource)
delete_instances(north_virginia_resource)

# deleting target groups
delete_target_group(loadbalancer_resource, DJANGO_TARGET_GROUP_NAME)

# deleting security-groups
delete_security_group(ohio_resource, POSTGRES_SECURITY__GROUP)
delete_security_group(north_virginia_resource, DJANGO_SECURITY_GROUP)


# ================================
# CREATING EVERYTHING

# creating security-groups
postgres_security_group_id = create_security_group(ohio_resource, POSTGRES_SECURITY__GROUP, postgres_permissions)
django_security_group_id = create_security_group(north_virginia_resource, DJANGO_SECURITY_GROUP, django_permissions)

# crating instances
postgres_id, postgres_ip = create_instance(ohio_resource, OHIO_REGION, AMI_OHIO, postgres_script, postgres_security_group_id, POSTGRES_SECURITY__GROUP, POSTGRES_INSTANCE_NAME)
django_script = django_script.replace("POSTGRES_IP", str(postgres_ip))
django_id, django_ip = create_instance(north_virginia_resource, NORTH_VIRGINIA_REGION, AMI_NORTH_VIRGINIA, django_script, django_security_group_id, DJANGO_SECURITY_GROUP, DJANGO_INSTANCE_NAME)

# creating django image
django_image_id = create_image(north_virginia_resource, DJANGO_IMAGE_NAME, django_id) 

# deleting django instance
delete_instances(north_virginia_resource)

# creating target group
target_group_arn = create_target_group(north_virginia_resource, loadbalancer_resource, DJANGO_TARGET_GROUP_NAME)

# creating load balancer
loadbalancer_arn = create_loadbalancer(north_virginia_resource, loadbalancer_resource, LOADBALANCER_NAME, django_security_group_id)

# launching image
launch_image(auto_scalling_resource, django_image_id, django_security_group_id, LAUNCH_CONFIG_NAME)

# creating auto scalling group
create_auto_scalling(north_virginia_resource, auto_scalling_resource, AUTO_SCALLING_NAME, target_group_arn, LAUNCH_CONFIG_NAME)

# attaching load balancer to target groups
attach_loadbalancer(auto_scalling_resource, AUTO_SCALLING_NAME, target_group_arn)

# creating auto scalling policy
create_auto_scalling_policy(auto_scalling_resource, AUTO_SCALLING_POLICY_NAME, AUTO_SCALLING_NAME)

# creating listener
create_listener(loadbalancer_resource, loadbalancer_arn, target_group_arn)




