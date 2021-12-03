import boto3
from instances import create_instance, delete_instances
from securitygroups import create_security_group, delete_security_group
from images import create_image, delete_image
from loadbalancer import create_loadbalancer, delete_loadbalancer
from instancescripts import *
from permissions import *

POSTGRES_SECURITY__GROUP = "Postgres_Security_Group"
DJANGO_SECURITY_GROUP = "Django_Security_Group"
POSTGRES_INSTANCE_NAME = "bilbia_postgres_ohio"
DJANGO_INSTANCE_NAME = "bilbia_django_north_virginia"
DJANGO_IMAGE_NAME = "django_image"
LOADBALANCER_NAME = "bilbia-loadbalancer"
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
# delete_auto_scalling(auto_scalling_resource)

# deleting image
delete_image(north_virginia_resource, DJANGO_IMAGE_NAME)

# deleting launched image config
# delete_launch_config(auto_scalling_resource, bago)

# deleting instances
delete_instances(ohio_resource)
delete_instances(north_virginia_resource)

# deleting target groups
# delete_target_groups(loadbalancer_resource)

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

#creating target group

#creating load balancer
loadbalancer_arn = create_loadbalancer(north_virginia_resource, loadbalancer_resource, LOADBALANCER_NAME, django_security_group_id)



