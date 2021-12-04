postgres_permissions = [
    {
        "FromPort": 22,
        "ToPort": 22,
        "IpProtocol": "tcp",
        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
    },
    {
        "FromPort": 5432,
        "ToPort": 5432,
        "IpProtocol": "tcp",
        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
    },
    {
        "FromPort": 80,
        "ToPort": 80,
        "IpProtocol": "tcp",
        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
    },
]

django_permissions = [
    {
        "FromPort": 22,
        "ToPort": 22,
        "IpProtocol": "tcp",
        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
    },
    {
        "FromPort": 8080,
        "ToPort": 8080,
        "IpProtocol": "tcp",
        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
    },
    {
        "FromPort": 80,
        "ToPort": 80,
        "IpProtocol": "tcp",
        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
    },
]