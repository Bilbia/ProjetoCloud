from log import logging

def create_security_group(ec2, securityGroupName, permissions):
    try:
        logging.info("="*10)
        logging.info(f"Creating {securityGroupName} security-group")
        vpcID = ec2.describe_vpcs()['Vpcs'][0]['VpcId']
        securityGroup = ec2.create_security_group(
            GroupName = securityGroupName,
            Description = "security-group",
            VpcId = vpcID,
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key': 'SecurityGroupName',
                            'Value': securityGroupName
                        },
                    ]
                },
            ],
        )

        logging.info(f"{securityGroupName} security-group created")

        securityGroupID = securityGroup['GroupId']
        ec2.authorize_security_group_ingress(
            GroupId = securityGroupID,
            IpPermissions = permissions
        )

        logging.info("Security-group authorized")

        return securityGroupID

    except Exception as e:
        logging.info("="*10)
        logging.info("Error creating security-group")
        logging.error(e)

def delete_security_group(ec2, securityGroupName):
    try:
        securityGroups = ec2.describe_security_groups()
        for securityGroup in securityGroups["SecurityGroups"]:
            if securityGroup["GroupName"] == securityGroupName:
                logging.info("="*10)
                logging.info("Deleting security-group")
                ec2.delete_security_group(GroupName = securityGroup["GroupName"], GroupId=securityGroup["GroupId"])
                logging.info("Security-Group deleted")
                return
        
        logging.info(f"{securityGroupName} not found")

    except Exception as e:
        logging.info("="*10)
        logging.info("Error deleting security-group")
        logging.error(e)