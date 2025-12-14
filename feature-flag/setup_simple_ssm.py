#!/usr/bin/env python3
"""
Simple SSM Parameter Setup - No AppConfig Needed

For a simple true/false feature flag, you don't need AppConfig.
Just use SSM Parameter Store directly.

Prerequisites:
    - AWS CLI configured
    - boto3 installed (pip install boto3)
    - IAM permissions for SSM

Usage:
    python setup_simple_ssm.py
"""

import boto3
import json
import sys
from botocore.exceptions import ClientError

# Configuration
REGION = "us-west-2"
PARAMETER_NAME = "/kognitos/dev/config"

# Simple feature flag - use Textract OCR on/off
CONFIG_VALUE = {
    "use-textract-ocr": "off"
}

def print_info(message):
    print(f"[INFO] {message}")

def print_success(message):
    print(f"[OK] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_warning(message):
    print(f"[WARNING] {message}")

# Initialize SSM client
ssm_client = boto3.client('ssm', region_name=REGION)

def create_ssm_parameter():
    """Create SSM parameter with Textract OCR flag"""
    print(f"\n{'='*60}")
    print("Creating SSM Parameter for Textract OCR Feature Flag")
    print(f"{'='*60}\n")
    
    config_json = json.dumps(CONFIG_VALUE)
    
    try:
        # Check if parameter exists
        try:
            ssm_client.get_parameter(Name=PARAMETER_NAME)
            print_warning(f"Parameter {PARAMETER_NAME} already exists. Updating...")
            
            ssm_client.put_parameter(
                Name=PARAMETER_NAME,
                Value=config_json,
                Type="String",
                Overwrite=True
            )
            print_success(f"Parameter updated: {PARAMETER_NAME}")
        except ssm_client.exceptions.ParameterNotFound:
            # Create new parameter
            ssm_client.put_parameter(
                Name=PARAMETER_NAME,
                Value=config_json,
                Type="String",
                Description="Textract OCR feature flag"
            )
            print_success(f"Parameter created: {PARAMETER_NAME}")
        
        # Verify
        response = ssm_client.get_parameter(Name=PARAMETER_NAME)
        value = json.loads(response['Parameter']['Value'])
        
        print(f"\n{'='*60}")
        print("✅ Setup Complete!")
        print(f"{'='*60}")
        print(f"\nParameter: {PARAMETER_NAME}")
        print(f"Value: {json.dumps(value, indent=2)}")
        print(f"\nTo update the flag, use:")
        print(f"  .\\update-ssm-parameter.ps1")
        print(f"\nOr AWS CLI:")
        print(f'  aws ssm put-parameter --name "{PARAMETER_NAME}" --value \'{{"use-textract-ocr":"on"}}\' --type String --overwrite --region {REGION}')
        print()
        
        return True
        
    except ClientError as e:
        print_error(f"Failed to create parameter: {e}")
        return False

def main():
    print("=" * 60)
    print("Simple SSM Parameter Setup (No AppConfig)")
    print("=" * 60)
    print()
    print("This creates just the SSM parameter.")
    print("No AppConfig Application, Environment, or Profile needed.")
    print()
    
    if create_ssm_parameter():
        print("\n✅ All done! Your Lambda can now read from SSM directly.")
        print("\nNext steps:")
        print("1. Update Lambda code to use lambda_function_simple_ssm.py")
        print("2. Update Lambda IAM role to allow ssm:GetParameter")
        print("3. Test your Lambda function")
    else:
        print("\n❌ Setup failed. Check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

