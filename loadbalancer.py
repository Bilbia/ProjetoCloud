from log import logging

def create_loadbalancer(ec2, ec2_loadbalancer, loadbalancerName, securityGroupId):
    try:
        logging.info("="*10)
        logging.info("Getting subnets")
        subnets = ec2.describe_subnets()
        subnets_ids = []
        for subnet in subnets["Subnets"]:
            subnets_ids.append(subnet["SubnetId"])

        logging.info(f"Creating {loadbalancerName} load balancer")
        loadbalancer = ec2_loadbalancer.create_load_balancer(
            Name = loadbalancerName,
            SecurityGroups = [securityGroupId],
            IpAddressType = "ipv4",
            Subnets = subnets_ids,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': loadbalancerName
                }
            ],
        )

        loadbalancerArn = loadbalancer["LoadBalancers"][0]["LoadBalancerArn"]
        waiter = ec2_loadbalancer.get_waiter("load_balancer_available")
        waiter.wait(LoadBalancerArns=[loadbalancerArn])
        logging.info(f"Load balancer {loadbalancerName} created")
        return loadbalancerArn

    except Exception as e:
        logging.info("="*10)
        logging.info("Error creating loadbalancer")
        logging.error(e)

def delete_loadbalancer(ec2_loadbalancer, loadbalancerName):
    try:
        loadbalancer = ec2_loadbalancer.describe_load_balancers(Names=[loadbalancerName])

        if(len(loadbalancer) > 0):
            logging.info("="*10)
            logging.info(f"Deleting load balancer {loadbalancerName}")
            loadbalancerArn = loadbalancer["LoadBalancers"][0]["LoadBalancerArn"]
            ec2_loadbalancer.delete_load_balancer(LoadBalancerArn=loadbalancerArn)
            waiter = ec2_loadbalancer.get_waiter("load_balancers_deleted")
            waiter.wait(LoadBalancerArns=loadbalancerArn)
            logging.info(f"Load Balancer {loadbalancerName} deleted")
            return loadbalancerArn
        
        else:
            logging.info("="*10)
            logging.info(f"There are no load balancers named {loadbalancerName}, nothing to delete")

    except Exception as e:
        logging.info("="*10)
        logging.info("Error deleting loadbalancer")
        logging.error(e)