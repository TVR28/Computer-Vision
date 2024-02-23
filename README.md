# Video Summarization API With DSNet Using PyTorch and AWS

Video Summarization API leverages deep learning and AWS infrastructure to provide an efficient, scalable solution for summarizing video content. This project is inspired by the DSNet paper and aims to make video content more accessible and manageable by extracting and presenting key segments, saving time and resources for users.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Pre-Training and API Usage](#pre-training)
- [System Design](#system-design)
- [Implementation Phases](#implementation-phases)
- [AWS Services Used](#aws-services-used)
- [Output](#output)
- [Contributing](#contributing)

## Introduction

![image](https://github.com/anvithalolla/Video_Summarization_API/assets/55392153/995d4d01-4234-49de-9093-98ac384c8a34)

The Video Summarization API is designed to handle 600 requests per day, processing input videos stored in S3 buckets and utilizing various AWS services for a fully integrated cloud solution.

Access the **DSNet: A Flexible Detect-to-Summarize Network for Video Summarization** [paper](https://ieeexplore.ieee.org/document/9275314)

## Prerequisites

- `AWS` Account with CLI configured
- `Python 3.8+`
- `PyTorch`
- `OpenCV`
- Access to Amazon Web Services `EC2`, `S3`, `Lambda`, `API Gateway`, `SQS`, `SNS`

## Getting Started

This section guides you through the initial setup and configuration needed to start using Video Summarizer. The setup involves creating an AWS EC2 instance, configuring it with the necessary hardware and software, and setting up the base repository.

### Step 1: AWS EC2 Instance Setup

1. **Create an EC2 Instance**:
    - Log into your AWS Management Console and navigate to the EC2 Dashboard.
    - Launch a new instance and select the **p2.xlarge** instance type for optimal performance with video summarization tasks. Note: This instance type is necessary for its GPU capabilities, which are essential for processing video data efficiently.

2. **Increase Capacity**:
    - By default, AWS accounts might have limitations on the usage of certain instance types. If you encounter a limit for the **p2.xlarge** instances, request an increase in capacity through AWS Support.

3. **Key-Pair Configuration**:
    - During the instance setup, create a new key-pair named `video_summarization_key`. This key will be used to securely connect to your instance.
    - Download the key-pair and convert it to `.ppk` format using a tool like PuTTYgen if you're on Windows. This format is required for PuTTY, a SSH client used to connect to the instance.

### Step 2: Connecting to Your Instance

1. **Use PuTTY for SSH Connection**:
    - Open PuTTY and input your instance's public IP address in the `Host Name (or IP address)` field.
    - Navigate to `Connection > SSH > Auth` in the PuTTY configuration menu. Browse and select your `.ppk` key file under `Private key file for authentication`.

2. **Remote Terminal Access**:
    - Once the configuration is set, open the connection to access the remote terminal of your EC2 instance.

### Step 3: Environment Setup

In the remote terminal, execute the following commands to set up your environment:

```bash
# Update your instance's package repository
sudo apt-get update

# Install CUDA (replace 'latest_version' with the actual version number)
sudo apt-get install cuda-latest_version

# Clone the base repository
git clone https://github.com/anvithalolla/Video_Summarization_API.git

# Navigate to the repository directory
cd Video_Summarization_API

# Install required dependencies
pip install -r requirements.txt
```

## Pre-Training

Video Summarizer offers pre-trained models that are readily available for download. These models can be used for immediate video summarization without the need for training from scratch. If you prefer to train your own models, you may skip this section.

### Downloading Pre-trained Models

We provide two types of pre-trained models: anchor-based and anchor-free. You can download and unzip these models using the following commands:

- **Anchor-Based Model**:
    ```
    wget https://www.dropbox.com/s/0jwn4c1ccjjysrz/pretrain_ab_basic.zip
    unzip pretrain_ab_basic.zip
    ```

- **Anchor-Free Model**:
    ```
    wget https://www.dropbox.com/s/2hjngmb0f97nxj0/pretrain_af_basic.zip
    unzip pretrain_af_basic.zip
    ```

It's crucial to extract these pre-trained model archives for the subsequent video summarization tasks.

### Environment Setup

Before utilizing the pre-trained models, ensure your environment is correctly set up. This setup includes installing CUDA 11.0.4, Python 3.7, and other necessary dependencies.

1. **CUDA Installation**:
    Update your package list and remove any existing NVIDIA drivers before installing the new ones:
    ```
    sudo apt update
    sudo apt-get --purge remove 'nvidia*'
    sudo apt install nvidia-driver-450
    sudo reboot
    ```

2. **Python 3.7 Installation**:
    Update your package list, add the deadsnakes PPA for newer Python versions, and install Python 3.7 along with necessary packages:
    ```
    sudo apt update
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.7
    sudo apt install python3.7-distutils
    sudo apt-get install python3.7-dev
    ```

3. **Clone Repository and Set Up Virtual Environment**:
    After cloning the repository to your server, create a virtual environment using Python 3.7 and activate it:
    ```
    virtualenv venv --python=python3.7
    source venv/bin/activate
    ```

4. **Install Dependencies**:
    Navigate to your project directory and install the required Python packages. If you encounter any issues with Torch, install it first before proceeding with other requirements:
    ```
    cd DSNet  # Change to your project directory
    pip install torch==1.1.0
    pip install -r requirements.txt
    ```

### Running Inference

To run the inference process, follow these steps:

1. **Prepare the Model Directory**:
    ```
    mkdir -p models && cd models
    ```

2. **Execute Inference**:
    Change the directory to `src` and run the inference script. If you encounter an import error with PIL, update torchvision to version 0.5.0:
    ```
    cd src  # Change to the src directory of your project
    pip install torchvision==0.5.0  # Update torchvision if necessary
    python infer.py anchor-free --ckpt-path ../models/pretrain_af_basic/checkpoint/summe.yml.0.pt --source ../custom_data/videos/EE-bNr36nyA.mp4 --save-path ./output.mp4
    ```

3. **Testing with Custom Video**:
    To test with a custom video file, transfer it to your EC2 instance and run the inference script:
    ```
    scp -i ~/.ssh/aws-ft-key-pair.pem /path/to/test.mp4 ubuntu@<PUBLIC_DNS>:/path/to/DSNet/src/
    ```
    Replace `<PUBLIC_DNS>` with your instance's public DNS. Then, run the inference command again with your test video as the source.

By following these instructions, you can leverage Video Summarizer's pre-trained models for efficient video summarization.


## API Usage

Send a POST request with the video path and model selection to the API endpoint. The API processes requests asynchronously, with summarized videos stored in the designated output S3 bucket.

## System Design

Video Summarization employs a robust and scalable architecture to handle video summarization requests efficiently. The system is designed to be fully automated, leveraging various AWS services to manage the workflow from request to delivery.

### Overview

The process begins when a user submits a video summarization request through an API built with Amazon API Gateway. This request triggers a Lambda function, which performs two critical actions:

1. **Immediate Acknowledgment**: The Lambda function sends an immediate response back to the user, acknowledging the receipt of the request.
2. **Queue Update**: The function updates an Amazon SQS queue specifically created to manage the video summarization tasks.

### Continuous Polling and Processing

An EC2 instance is dedicated to continuously polling this SQS queue for new requests. Upon receiving a new request, the EC2 instance performs the following steps:

- **Video Download**: Retrieves the input video file from an Amazon S3 bucket.
- **Summarization**: Initiates the video summarization process using pre-determined models and algorithms.
- **Output Upload**: Once the summarization is complete, the output video is uploaded back to a designated S3 bucket for retrieval.

### Notification System

Upon successful completion and upload of the summarized video, an Amazon SNS topic is used to send a notification to the API endpoint. This notification contains details about the output video, such as its location in the S3 bucket, allowing the user to access the summarized content.

### Architectural Diagram

![image](https://github.com/anvithalolla/Video_Summarization_API/assets/55392153/3d765679-b905-40c4-ae3b-b81159125190)

This diagram illustrates the flow of data and interactions between different AWS services, providing a clear view of how Video Summarizer processes each video summarization request from start to finish.

By employing this architecture, Video Summarizer ensures a seamless and scalable solution to video summarization, capable of handling multiple requests concurrently and efficiently.
.

## Implementation Phases

This section outlines the key steps involved in setting up and configuring the Video Summarizer system, including AWS services like Lambda, SQS, and API Gateway.

### Phase 1: Setting Up AWS IAM Role

1. **Create a Role in AWS IAM**:
    - Name the role `SQSBasicLambdaExecutionRole`.
    - Attach the `AmazonSQSFullAccess` and `AWSLambdaBasicExecutionRole` policies.

### Phase 2: Lambda Function Configuration

1. **Create Lambda Function**:
    - Navigate to AWS Lambda and create a new function named `VSApiProcessRequest`.
    - Select Python 3.11 as the runtime.
    - Assign the `SQSBasicLambdaExecutionRole` created earlier.

2. **Lambda Function Configuration**:
    - In the General Configuration, set the timeout to 1 minute.
    - In Asynchronous Invocation, set the retry attempts to 0.

### Phase 3: API Gateway Setup

1. **Create API Gateway**:
    - Choose REST API and name it `VS_API`.
    - Create a new POST method linked to the `VSApiProcessRequest` Lambda function.

2. **Deploy API**:
    - Test the POST method to ensure it returns a "hello from lambda" message, confirming the setup is correct.

### Phase 4: Lambda Function Code

Implement the following code in the Lambda function to process requests, generate unique IDs, and update the SQS queue:

```python
import ast
import json
import random
import string
import boto3

def lambda_handler(event, context):
    # Parse the request body
    body = ast.literal_eval(event['body'])
    input_video = body['input']
    model = body['model']
    
    # Generate a unique ID for the request
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    
    # Initialize SQS client and update the queue
    sqs = boto3.client('sqs')
    sqs.send_message(
        QueueUrl='[Your_SQS_Queue_URL]',
        MessageBody=json.dumps({'id': id, 'input': input_video, 'model': model}),
        MessageGroupId='[Your_Message_Group_ID]'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'id': id})
    }
```
### Phase 5: SQS Queue Setup

- **Create SQS Queue**:
    - Navigate to the Amazon SQS console and create a new FIFO queue named `Video_summarization_queue.fifo`.
    - FIFO queues are designed to ensure that the order in which messages are sent and received is strictly preserved and that each message is processed exactly once.

### Phase 6: S3 Bucket Preparation

- **Create an S3 Bucket**:
    - Go to the Amazon S3 console and create a new bucket for storing your input and output videos.
    - Organize the bucket by creating two folders: `input` for incoming videos and `output` for the summarized videos.
    - Upload your test video into the `input` folder for initial testing.

### Phase 7: Testing and Validation

- **API Gateway Testing**:
    - In the Amazon API Gateway console, configure the request body for your API method to include the path to your test video and the model details: `{"input": "input/test.mp4", "model": {"type": "anchor-based", "name": "summe.yml.0.pt"}}`.
    - Invoke the POST method to test the setup. Ensure that the Lambda function is triggered and that it interacts with the SQS queue as expected.

### Phase 8: EC2 Instance Configuration and SNS Setup

- **Configure EC2 Instance**:
    - Assign an IAM role to your EC2 instance that grants it permissions similar to the Lambda function, including access to S3, SQS, and SNS services.

- **SNS Topic Creation**:
    - Create a new SNS topic named `VS_SNS` using the Amazon SNS console. This topic will be used to notify the API endpoint or other subscribers upon the completion of the video summarization process.

### Phase 9: Processing Queue Data

- **Implement a Processing Script on EC2**:
    - Develop a script to be run on the EC2 instance that continuously polls the SQS queue for new messages.
    - For each message, the script should download the input video from the S3 bucket, process it using the video summarization algorithm, and then upload the summarized video back to the S3 bucket in the `output` folder.
    - After processing, the script should publish a notification to the `VS_SNS` topic with details about the completed job.

```python
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
```
## AWS Services Used

- **EC2**: For running the video summarization models and processing tasks.
- **S3**: To store input and output videos.
- **Lambda**: To handle API requests and manage SQS queue updates.
- **API Gateway**: For API endpoint creation and management.
- **SQS**: To queue video summarization tasks.
- **SNS**: For notifying the API endpoint upon task completion.

## Output

The final output (output.mp4) is a summarized version of the input video, significantly reduced in length while retaining essential content. This output is stored in an S3 bucket and accessible via a notification sent to the API endpoint.


## Contributing

Contributions to Video Summarization API are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository to your own GitHub account.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a clear description of your changes.


