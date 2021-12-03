from log import logging

def create_image(ec2, imageName, instanceID):
    try:
        logging.info("="*10)
        logging.info(f"Creating {imageName} image")
        image = ec2.create_image(
            Name=imageName,
            InstanceId=instanceID,
            TagSpecifications=[
                {
                    "ResourceType": "image",
                    "Tags": [
                        {
                        "Key": "Name",
                        "Value": imageName
                        }
                    ]
                }
            ]
        )

        imageID = image["ImageId"]
        waiter = ec2.get_waiter("image_available")
        waiter.wait(ImageIds=[imageID])
        logging.info(f"{imageName} image created with {instanceID} instance ID")
        return imageID

    except Exception as e:
        logging.info("="*10)
        logging.info("Error creating image")
        logging.error(e)

def delete_image(ec2, imageName):
    try:
        images = ec2.describe_images(Filters=[
            {
                "Name": "name",
                "Values": [imageName]
            }
        ])

        if(len(images) > 0):
            logging.info("="*10)
            logging.info(f"Deleting image {imageName}")
            ec2.deregister_image(ImageId=images["Images"][0]["ImageId"])
            logging.info(f"Image {imageName} deleted")

        else:
            logging.info("="*10)
            logging.info(f"There are no images named {imageName}, nothing to delete")
    
    except Exception as e:
        logging.info("="*10)
        logging.info("Error deleting image")
        logging.error(e)