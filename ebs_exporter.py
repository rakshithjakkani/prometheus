from prometheus_client import start_http_server, Gauge
import boto3
import time

if __name__ == '__main__':
    # Create a Prometheus Gauge to represent the metric
    ebs_volume_health = Gauge('ebs_volume_health', 'EBS Volume Health Status', ['volume_id'])

    # Start the Prometheus HTTP server
    start_http_server(8001)

    while True:
        # Create an AWS session
        session = boto3.Session()

        # Create an EC2 client
        ec2_client = session.client('ec2')

        # Get a list of EBS volumes
        response = ec2_client.describe_volumes()

        # Iterate through the volumes and collect metrics
        for volume in response['Volumes']:
            volume_id = volume['VolumeId']
            res = ec2_client.describe_volume_status(VolumeIds=[volume_id])["VolumeStatuses"][0]['VolumeStatus']

            print(res)
            health_status = res.get('Status', 'Unknown')
            print(health_status)

            # Set the metric value
            ebs_volume_health.labels(volume_id=volume_id).set(1 if health_status == 'ok' else 0)

        # Sleep for 30 seconds before collecting metrics again
        time.sleep(30)
