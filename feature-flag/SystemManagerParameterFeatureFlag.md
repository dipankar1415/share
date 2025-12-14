# Simple SSM Feature Flags - Complete Guide

A simple guide to implement feature flags using AWS SSM Parameter Store with Python Lambda functions. **No AppConfig needed** - just SSM!

---

## Quick Start

### 1. Set Up SSM Parameter

```bash
# Install dependencies
pip install -r requirements.txt

# Create SSM parameter with Textract OCR flag
python setup_simple_ssm.py
```

**What this creates:**

- SSM Parameter: `/kognitos/dev/config` with value `{"use-textract-ocr": "off"}`

### 2. Create Lambda Function

```bash
# Create Lambda function that reads from SSM
python create_lambda_function.py
```

**What this creates:**

- Lambda function: `AppConfigFeatureFlagFunction`
- IAM role with SSM permissions
- Environment variable pointing to SSM parameter

### 3. Update Feature Flag

```powershell
# Edit update-ssm-parameter.ps1 to change true/false
.\update-ssm-parameter.ps1
```

### 4. Test Lambda

Go to AWS Lambda Console → Test → Use any test event → Should return Textract OCR flag status

---

## Architecture

```
┌─────────────────┐
│  SSM Parameter  │  Stores simple JSON
│ /kognitos/dev/  │  {"use-textract-ocr": "on"}
│     config      │
└────────┬────────┘
         │
         │ Read directly
         ▼
┌─────────────────┐
│  Lambda Function│  Reads from SSM
│  (Simple SSM)   │  Returns flag status
└─────────────────┘
```

**No AppConfig needed!** Just SSM Parameter Store.

---

## Lambda Function Code

The Lambda function (`lambda_function_simple_ssm.py`) simply:

1. Reads from SSM Parameter Store
2. Parses JSON: `{"use-textract-ocr": "on"}` or `{"use-textract-ocr": "off"}`
3. Returns status

**No AppConfig, no complexity - just SSM!**

---

## Updating Feature Flags

### Method 1: PowerShell Script (Recommended)

```powershell
# Edit update-ssm-parameter.ps1
# Change line 9: $JSON_VALUE = '{\"use-textract-ocr\":\"on\"}' or \"off\"

.\update-ssm-parameter.ps1
```

### Method 2: AWS CLI

```bash
aws ssm put-parameter \
    --name "/kognitos/dev/config" \
    --value '{"use-textract-ocr":"on"}' \
    --type "String" \
    --overwrite \
    --region us-west-2
```

### Method 3: AWS Console

1. Systems Manager → Parameter Store
2. Find `/kognitos/dev/config`
3. Edit → Update value
4. Save

**No deployment needed!** Lambda reads directly from SSM.

---

## IAM Permissions

Lambda needs this IAM policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["ssm:GetParameter", "ssm:GetParameters"],
      "Resource": "arn:aws:ssm:*:*:parameter/kognitos/*"
    }
  ]
}
```

The `create_lambda_function.py` script sets this up automatically.

---

## Development Workflow

```
1. You edit → lambda_function_simple_ssm.py (local file)
         ↓
2. create_lambda_function.py reads it
         ↓
3. Uploads to AWS Lambda (as lambda_function.py)
         ↓
4. Lambda function runs this code when invoked
         ↓
5. Returns feature flag status
```

**To update Lambda code:**

1. Edit `lambda_function_simple_ssm.py` locally
2. Run: `python create_lambda_function.py`
3. Lambda function is updated automatically

---

## Testing

### Test Lambda Function

1. Go to AWS Lambda Console
2. Select function: `AppConfigFeatureFlagFunction`
3. Click "Test"
4. Use test event: `{}`
5. Check response

**Expected Response:**

```json
{
  "statusCode": 200,
  "body": "{\"feature_status\": \"Textract OCR is ENABLED.\", \"config_data\": {\"use-textract-ocr\": \"on\"}, \"feature_flag\": true, \"use_textract_ocr\": \"on\"}"
}
```

---

## Troubleshooting

### Problem: Lambda can't read SSM parameter

**Solution:**

- Check IAM permissions on Lambda execution role
- Verify SSM parameter exists: `aws ssm get-parameter --name "/kognitos/dev/config" --region us-west-2`
- Check Lambda environment variable: `SSM_PARAMETER_NAME`

### Problem: Invalid JSON error

**Solution:**

- Ensure SSM parameter has valid JSON: `{"use-textract-ocr": "on"}` or `{"use-textract-ocr": "off"}`
- Keys must be in double quotes
- Use `update-ssm-parameter.ps1` script (handles escaping correctly)

### Problem: Feature flag not updating

**Solution:**

- Lambda reads directly from SSM - changes are immediate
- Verify SSM parameter was updated: `aws ssm get-parameter --name "/kognitos/dev/config" --region us-west-2`
- Check CloudWatch logs for errors

---

## Why Simple SSM Instead of AppConfig?

**For a simple true/false flag:**

- **Simpler** - No Application, Environment, or Profile needed
- **Faster** - Direct SSM read, no deployment step
- **Cheaper** - No AppConfig API calls
- **Easier** - Just update SSM parameter, done!

**AppConfig is useful for:**

- Complex configurations
- Multiple environments
- Deployment strategies
- Configuration validation
- Version management

**For a simple Textract OCR flag, SSM is perfect!**

---

## Cleanup

To delete all resources:

```bash
# Delete Lambda function
aws lambda delete-function --function-name AppConfigFeatureFlagFunction --region us-west-2

# Delete SSM Parameter
aws ssm delete-parameter --name "/kognitos/dev/config" --region us-west-2

# Delete IAM role (optional)
aws iam delete-role-policy --role-name AppConfigFeatureFlagFunction-role --policy-name AppConfigFeatureFlagFunction-SSMPolicy
aws iam detach-role-policy --role-name AppConfigFeatureFlagFunction-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam delete-role --role-name AppConfigFeatureFlagFunction-role
```

---

## Summary

**Simple Setup:**

- Just SSM Parameter Store
- No AppConfig complexity
- Direct read from SSM

**Easy Updates:**

- Update SSM parameter
- Lambda picks up changes immediately
- No deployment needed

**Perfect for:**

- Simple on/off feature flags
- Single environment
- Quick changes
