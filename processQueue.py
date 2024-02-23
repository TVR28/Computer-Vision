# processQueue.py
import time
import ast
import os
import json

import boto3

# Initialize AWS clients
sqs = boto3.client('sqs', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')

# Queue URL and S3 bucket name (fill these with your actual SQS queue URL and S3 bucket name)
queue_url = 'YOUR_SQS_QUEUE_URL'
S3_BUCKET = 'YOUR_S3_BUCKET_NAME'

while True:
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1
    )
    
    # Check if any messages are received
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        
        # Convert the message body from string to dictionary
        message_body = ast.literal_eval(message['Body'])
        print(f"Message received: {message_body}")
        
        # Process the video summarization
        input_video = message_body['input_video']
        model_type = message_body['model']['type']
        model_name = message_body['model']['name']
        video_id = message_body['id']
        
        # Download the input video from S3
        s3.download_file(S3_BUCKET, input_video, "in.mp4")
        
        # Run the video summarization algorithm (adjust the command according to your setup)
        os.system(f"python infer.py {model_type} --ckpt-path ../models/{model_type}/{model_name} --source in.mp4 --save-path output.mp4")
        
        # Upload the summarized video to S3
        s3.upload_file('output.mp4', S3_BUCKET, f"output/{video_id}.mp4")
        
        # Publish a notification to SNS about the completion of video summarization
        sns_response = sns.publish(
            TargetArn='YOUR_SNS_TOPIC_ARN',  # Replace with your SNS topic ARN
            Message=json.dumps({'id': video_id, 'output_video': f"output/{video_id}.mp4"})
        )
        
        # Delete the processed message from the queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        
        print(f"Video summarization completed for {video_id}, output uploaded to S3, and notification sent via SNS.")
    else:
        print("No messages in the queue. Sleeping...")
        time.sleep(60)  # Sleep for 60 seconds before checking the queue again
