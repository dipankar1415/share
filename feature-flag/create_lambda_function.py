#!/usr/bin/env python3
"""
Create Lambda Function for Simple SSM Feature Flags

This script creates a Lambda function that reads feature flags directly from SSM Parameter Store.
No AppConfig needed - just simple SSM parameter.

Prerequisites:
    - AWS CLI configured
    - boto3 installed
    - SSM parameter already created (run setup_simple_ssm.py first)
"""

import boto3
import json
import os
import zipfile
import io
import time
from botocore.exceptions import ClientError

# Configuration
FUNCTION_NAME = "AppConfigFeatureFlagFunction"
RUNTIME = "python3.12"
REGION = "us-west-2"
ARCHITECTURE = "x86_64"

# SSM Parameter name
SSM_PARAMETER_NAME = os.getenv('SSM_PARAMETER_NAME', '/kognitos/dev/config')

# Read Lambda function code from file
def get_lambda_code():
    """Read Lambda function code from lambda_function_simple_ssm.py"""
    try:
        with open('lambda_function_simple_ssm.py', 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"[ERROR] lambda_function_simple_ssm.py not found. Make sure you're in the appconfig-feature-flags directory.")
        return None

def print_info(message):
    print(f"[INFO] {message}")

def print_success(message):
    print(f"[OK] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_warning(message):
    print(f"[WARNING] {message}")

# Initialize AWS clients
lambda_client = boto3.client('lambda', region_name=REGION)
iam_client = boto3.client('iam')

def create_lambda_role():
    """Create IAM role for Lambda function"""
    role_name = f"{FUNCTION_NAME}-role"
    
    print_info(f"Creating IAM role: {role_name}")
    
    # Trust policy for Lambda
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        role_arn = None
        
        # Check if role exists
        try:
            response = iam_client.get_role(RoleName=role_name)
            role_arn = response['Role']['Arn']
            print_warning(f"Role {role_name} already exists: {role_arn}")
            
            # Verify trust policy is correct
            current_trust = response['Role']['AssumeRolePolicyDocument']
            if isinstance(current_trust, str):
                current_trust = json.loads(current_trust)
            
            # Update trust policy if needed
            if current_trust != trust_policy:
                print_info("Updating trust policy...")
                iam_client.update_assume_role_policy(
                    RoleName=role_name,
                    PolicyDocument=json.dumps(trust_policy)
                )
                print_success("Trust policy updated")
        except iam_client.exceptions.NoSuchEntityException:
            # Create role
            response = iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description=f"IAM role for {FUNCTION_NAME} Lambda function"
            )
            role_arn = response['Role']['Arn']
            print_success(f"Role {role_name} created: {role_arn}")
            
            # Wait a moment for role to propagate
            print_info("Waiting for IAM role to propagate (5 seconds)...")
            time.sleep(5)
        
        # Attach basic Lambda execution policy
        try:
            iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
            )
            print_success("Basic Lambda execution policy attached")
        except ClientError as e:
            if "already attached" not in str(e).lower():
                print_warning(f"Could not attach basic policy: {e}")
        
        # Create inline policy for SSM access
        policy_name = f"{FUNCTION_NAME}-SSMPolicy"
        ssm_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "ssm:GetParameter",
                        "ssm:GetParameters"
                    ],
                    "Resource": f"arn:aws:ssm:{REGION}:*:parameter/kognitos/*"
                }
            ]
        }
        
        try:
            iam_client.put_role_policy(
                RoleName=role_name,
                PolicyName=policy_name,
                PolicyDocument=json.dumps(ssm_policy)
            )
            print_success(f"SSM policy attached to role")
        except ClientError as e:
            print_warning(f"Could not attach SSM policy: {e}")
        
        return role_arn
        
    except ClientError as e:
        print_error(f"Failed to create role: {e}")
        return None

def create_lambda_function(role_arn):
    """Create Lambda function with retry logic"""
    print_info(f"Creating Lambda function: {FUNCTION_NAME}")
    
    # Helper function to create zip file from Lambda code
    def create_lambda_zip(lambda_code):
        """Create a zip file in memory containing the Lambda function code"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Lambda expects the file to be named lambda_function.py
            zip_file.writestr('lambda_function.py', lambda_code)
        zip_buffer.seek(0)
        return zip_buffer.read()
    
    try:
        # Check if function exists
        try:
            lambda_client.get_function(FunctionName=FUNCTION_NAME)
            print_warning(f"Function {FUNCTION_NAME} already exists. Updating code...")
            
            # Read Lambda code from file
            lambda_code = get_lambda_code()
            if not lambda_code:
                return False
            
            # Create zip file with Lambda code (AWS Lambda requires code as ZIP)
            zip_content = create_lambda_zip(lambda_code)
            
            # Update function code
            lambda_client.update_function_code(
                FunctionName=FUNCTION_NAME,
                ZipFile=zip_content
            )
            
            # Update configuration
            lambda_client.update_function_configuration(
                FunctionName=FUNCTION_NAME,
                Environment={
                    'Variables': {
                        'SSM_PARAMETER_NAME': SSM_PARAMETER_NAME
                    }
                }
            )
            
            print_success(f"Function {FUNCTION_NAME} updated")
            return True
            
        except lambda_client.exceptions.ResourceNotFoundException:
            # Create new function - retry if role propagation issue
            pass
    
        # Retry logic for role propagation
        max_retries = 3
        retry_delay = 10  # seconds
        
        for attempt in range(1, max_retries + 1):
            try:
                print_info(f"Attempt {attempt}/{max_retries} to create function...")
                
                # Read Lambda code from file
                lambda_code = get_lambda_code()
                if not lambda_code:
                    return False
                
                # Create zip file with Lambda code (AWS Lambda requires code as ZIP)
                zip_content = create_lambda_zip(lambda_code)
                
                # Create function
                response = lambda_client.create_function(
                    FunctionName=FUNCTION_NAME,
                    Runtime=RUNTIME,
                    Role=role_arn,
                    Handler='lambda_function.lambda_handler',
                    Code={'ZipFile': zip_content},
                    Description='Lambda function for simple SSM feature flags',
                    Timeout=30,
                    MemorySize=128,
                    Environment={
                        'Variables': {
                            'SSM_PARAMETER_NAME': SSM_PARAMETER_NAME
                        }
                    },
                    Architectures=[ARCHITECTURE]
                )
                
                print_success(f"Function {FUNCTION_NAME} created with ARN: {response['FunctionArn']}")
                
                return True
                
            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', '')
                error_message = str(e)
                
                if "cannot be assumed" in error_message.lower() and attempt < max_retries:
                    print_warning(f"Role not ready yet (attempt {attempt}/{max_retries})")
                    print_info(f"Waiting {retry_delay} seconds for IAM role to propagate...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print_error(f"Failed to create function: {e}")
                    if "cannot be assumed" in error_message.lower():
                        print_error("\nTroubleshooting:")
                        print_error("1. Check IAM role exists: aws iam get-role --role-name AppConfigFeatureFlagFunction-role")
                        print_error("2. Verify trust policy allows lambda.amazonaws.com")
                        print_error("3. Wait a few minutes and try again (IAM propagation can take time)")
                    return False
        
        print_error("Failed to create function after all retries")
        return False
        
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def main():
    print("=" * 80)
    print("Creating Lambda Function for Simple SSM Feature Flags")
    print("=" * 80)
    print()
    
    # Create IAM role
    role_arn = create_lambda_role()
    if not role_arn:
        print_error("Failed to create IAM role. Exiting.")
        return
    
    print()
    
    # Create Lambda function
    if create_lambda_function(role_arn):
        print()
        print("=" * 80)
        print_success("Lambda function created successfully!")
        print("=" * 80)
        print()
        print("Next steps:")
        print("1. Go to AWS Lambda Console")
        print(f"2. Find function: {FUNCTION_NAME}")
        print("3. Click 'Test' to test the function")
        print("4. Update feature flag: .\\update-ssm-parameter.ps1")
        print()
    else:
        print_error("Failed to create Lambda function")

if __name__ == "__main__":
    main()
