import boto3
from instances import create_instance, delete_instances
from securitygroups import create_security_group, delete_security_group
from instancescripts import *
from permissions import *

POSTGRES_SECURITY__GROUP = "Postgres_Security_Group"
DJANGO_SECURITY_GROUP = "Django_Security_Group"
POSTGRES_INSTANCE_NAME = "bilbia_postgres_ohio"
DJANGO_INSTANCE_NAME = "bilbia_django_north_virginia"
AMI_OHIO = "ami-020db2c14939a8efb"
AMI_NORTH_VIRGINIA = "ami-0279c3b3186e54acd"






# ec2 clients
ohio_resource = boto3.client('ec2', region_name='us-east-2')
north_virginia_resource = boto3.client('ec2', region_name='us-east-1')
loadbalancer_resource = boto3.client('elbv2', region_name='us-east-1')
auto_scalling_resource = boto3.client('autoscaling', region_name='us-east-1')

# ==================================
# DELETING EVERYTHING BEFORE RUNNING

# deleting loadbalancers
# delete_loadbalancer(loadbalancer_resource)

# deleting auto scalling
# delete_auto_scalling(auto_scalling_resource)

# deleting image
# delete_image(north_virginia_resource, bagulho aqui)

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
postgres_id, postgres_ip = create_instance(ohio_resource, AMI_OHIO, postgres_script, postgres_security_group_id, POSTGRES_SECURITY__GROUP, POSTGRES_INSTANCE_NAME)

django_script = django_script.replace("POSTGRES_IP", str(postgres_ip))
django_id, django_ip = create_instance(north_virginia_resource, AMI_NORTH_VIRGINIA, django_script, django_security_group_id, DJANGO_SECURITY_GROUP, DJANGO_INSTANCE_NAME)




