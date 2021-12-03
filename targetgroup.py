from log import logging

def create_target_group(ec2, ec2_loadbalancer, targetGroupName):
    try:
        logging.info("="*10)
        logging.info(f"Creating {targetGroupName} target group")

        vpcId = ec2.describe_vcps()["Vpcs"][0]["VpcId"]
        targetGroup = ec2_loadbalancer.create_target_group(
            Name = targetGroupName,
            Protocol = "HTTP",
            Port = 8080,
            VpcId = vpcId,
            TargetType = "instance",
        )

        targetGroupArn = targetGroup["TargetGroups"][0]["TargetGroupArn"]
        logging.info(f"{targetGroupName} target group created")

        return targetGroupArn

    except Exception as e:
        logging.info("="*10)
        logging.info("Error creating target group")
        logging.error(e)

def delete_target_group(ec2_loadbalancer, targetGroupName):
    try:
        targetGroups = ec2_loadbalancer.describe_target_groups(Names=[targetGroupName])
        if (len(targetGroups["TargetGroups"]) > 0):
            logging.info("="*10)
            logging.info("Deleting target group")
            ec2_loadbalancer.delete_target_group(TargetGroupArn = targetGroups["TargetGroups"][0]["TargetGroupArn"])
            logging.info(f"Target group {targetGroupName} deleted")
        else:
            logging.info("="*10)
            logging.info(f"There are no target groups named {targetGroupName}, nothing to delete")

    except Exception as e:
        logging.info("="*10)
        logging.info("Error deleting target group")
        logging.error(e)