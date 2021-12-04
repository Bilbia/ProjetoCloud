from log import logging
import boto3
import time

def create_instance(ec2, ec2Region, image, userData, securityGroupId, securityGroupName, instanceName):
    try:
        ec2Resource = boto3.resource("ec2", region_name=ec2Region)
        if(userData == None):
            instance = ec2Resource.create_instances(
                ImageId = image,
                MinCount = 1,
                MaxCount = 1,
                InstanceType = 't2.micro',
                SecurityGroupIds = [securityGroupId],
                SecurityGroups = [securityGroupName],
                TagSpecifications = [{
                    "ResourceType": "instance",
                    "Tags": [
                        {
                            "Key": "InstanceName",
                            "Value": instanceName
                        },
                        {
                            "Key": "Owner",
                            "Value": "bilbia"
                        }
                    ]
                }]
            )
        else:
            instance = ec2Resource.create_instances(
                ImageId = image,
                MinCount = 1,
                MaxCount = 1,
                InstanceType = 't2.micro',
                UserData = userData,
                SecurityGroupIds = [securityGroupId],
                SecurityGroups = [securityGroupName],
                TagSpecifications = [{
                    "ResourceType": "instance",
                    "Tags": [
                        {
                            "Key": "InstanceName",
                            "Value": instanceName
                        },
                        {
                            "Key": "Owner",
                            "Value": "bilbia"
                        }
                    ]
                }]
            )

        logging.info("="*10)
        logging.info(f"Creating {instanceName} instance")
        instance[0].wait_until_running()
        instance[0].reload()
        time.sleep(120)
        logging.info(f"{instanceName} instance created")

        instanceID = ec2.describe_instances(Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            },
            {
                "Name": "tag:InstanceName",
                "Values": [instanceName]
            },
        ])["Reservations"][0]["Instances"][0]["InstanceId"]

        instanceIP = instance[0].public_ip_address

        logging.info(f"Instance ID: {instanceID}")
        logging.info(f"Instance IP: {instanceIP}")

        return instanceID, instanceIP
    
    except Exception as e:
        logging.info("="*10)
        logging.info("Error creating instance")
        logging.error(e)
        return False

def delete_instances(ec2):
    try:
        waiter = ec2.get_waiter('instance_terminated')
        instances_IDs = []
        for instance in ec2.describe_instances(Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["pending", "running", "stopping", "stopped"]
            },
            {
                "Name": "tag:Owner",
                "Values": ["bilbia"]
            }
        ])["Reservations"]:
            instances_IDs.append(instance["Instances"][0]["InstanceId"])

        if(len(instances_IDs) > 0):
            logging.info("="*10)
            logging.info("Deleting instances")
            ec2.terminate_instances(InstanceIds=instances_IDs)
            print(instances_IDs)
            waiter.wait(InstanceIds=instances_IDs)
            logging.info("Instances deleted")
        
        else:
            logging.info("="*10)
            logging.info("There are no instances running, nothing to delete")
    
    except Exception as e:
        logging.info("="*10)
        logging.info("Error deleting instances")
        logging.error(e)
        
