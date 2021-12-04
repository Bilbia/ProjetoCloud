from log import logging

def create_auto_scalling(ec2, ec2_autoscalling, autoscallingName, targetGroupArn, launchConfigName):
    try:
        zones = []
        for zone in ec2.describe_availability_zones()["AvailabilityZones"]:
            zones.append(zone["ZoneName"])

        logging.info("="*10)
        logging.info("Creating auto scalling group")

        ec2_autoscalling.create_auto_scaling_group(
            AutoScalingGroupName = autoscallingName,
            LaunchConfigurationName = launchConfigName,
            MinSize = 1,
            MaxSize = 3,
            TargetGroupARNs = [targetGroupArn],
            AvailabilityZones = zones
        )

        logging.info("Auto Scalling group created")

    except Exception as e: 
        logging.info("="*10)
        logging.info("Error creating auto scalling group")
        logging.error(e)

def delete_auto_scalling(ec2_autoscalling, autoscallingName):
    try:
        logging.info("="*10)
        logging.info("Deleting auto scalling group")
        ec2_autoscalling.delete_auto_scaling_group(
            AutoScalingGroupName = autoscallingName,
            ForceDelete = True
        )

        logging.info("Auto scalling group deleted")

    except Exception as e:
        logging.info("="*10)
        logging.info("Error deleting auto scalling group")
        logging.error(e)

def attach_loadbalancer(ec2_autoscalling, autoscallingName, targetGroupArn):
    try:
        logging.info("="*10)
        logging.info("Attaching load balancer to target group")
        ec2_autoscalling.attach_load_balancer_target_groups(
            AutoScalingGroupName = autoscallingName,
            TargetGroupARNs = [targetGroupArn]
        )
        logging.info("Load balancer attached to target group")

    except Exception as e:
        logging.info("="*10)
        logging.info("Error deleting auto scalling group")
        logging.error(e)

def create_auto_scalling_policy(ec2_autoscalling, autoscallingPolicyName, autoscallingName):
    try:
        logging.info("="*10)
        logging.info("Creating auto scalling policy")
        ec2_autoscalling.put_scaling_policy(
            AutoScalingGroupName = autoscallingName,
            PolicyName = autoscallingPolicyName,
            PolicyType = "TargetTrackingScaling",
            TargetTrackingConfiguration = {
                "PredefinedMetricSpecification": {
                    "PredefinedMetricType": "ASGAverageCPUUtilization"
                },
                "TargetValue": 50
            }
        )

        logging.info("Auto scalling policy created")

    except Exception as e:
        logging.info("="*10)
        logging.info("Error creating auto scalling policy")
        logging.error(e)