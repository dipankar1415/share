import json
import boto3
import os
from botocore.exceptions import ClientError

# Initialize SSM client
ssm_client = boto3.client('ssm', region_name='us-west-2')

# SSM Parameter name
PARAMETER_NAME = os.getenv('SSM_PARAMETER_NAME', '/kognitos/dev/config')

def get_configuration():
    """Retrieve configuration directly from SSM Parameter Store"""
    try:
        response = ssm_client.get_parameter(Name=PARAMETER_NAME)
        config_value = response['Parameter']['Value']
        
        # Parse JSON
        config = json.loads(config_value)
        print(f"Retrieved config from SSM: {json.dumps(config)}")
        
        return config
    except ClientError as e:
        print(f"Error retrieving SSM parameter: {e}")
        return {"use-textract-ocr": "off"}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"use-textract-ocr": "off"}

def lambda_handler(event, context):
    """Lambda handler"""
    try:
        # Get configuration directly from SSM
        config = get_configuration()
        
        # Evaluate the feature flag
        use_textract = config.get('use-textract-ocr', 'off')
        
        if use_textract == 'on':
            message = "Textract OCR is ENABLED."
        else:
            message = "Textract OCR is DISABLED."
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'feature_status': message,
                'config_data': config,
                'feature_flag': use_textract == 'on',
                'use_textract_ocr': use_textract
            })
        }
    
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

