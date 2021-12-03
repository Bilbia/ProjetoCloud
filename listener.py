from log import logging

def create_listener(ec2_loadbalancer, loadbalancerArn, targetGroupArn):
    try:
        logging.info("="*10)
        logging.info("Creating listener")
        ec2_loadbalancer.create_listener(
            LoadBalancerArn = loadbalancerArn,
            Protocol = "HTTP",
            Port = 80,
            DefaultActions = [
                {
                    "Type": "forward",
                    "TargetGroupArn": targetGroupArn
                }
            ]
        )

        logging.info("Listener created")

    except Exception as e:
        logging.info("="*10)
        logging.info("Error creating listener")
        logging.error(e)