# PowerShell script to update SSM parameter for AppConfig feature flags

$PARAM_NAME = "/kognitos/dev/config"
$REGION = "us-west-2"

# Simple JSON configuration - minified (no spaces) to avoid PowerShell parsing issues
# Change "off" to "on" to enable the feature flag
# IMPORTANT: Keys must be in double quotes for valid JSON
$JSON_VALUE = '{\"use-textract-ocr\":\"on\"}'

Write-Host "Updating SSM parameter: $PARAM_NAME" -ForegroundColor Blue
Write-Host "Region: $REGION" -ForegroundColor Blue
Write-Host ""

# Always use --overwrite since parameter likely exists
Write-Host "Updating parameter (using --overwrite)..." -ForegroundColor Yellow

try {
    # Use the minified JSON directly (no spaces to avoid PowerShell splitting)
    # Quote it properly for AWS CLI
    $result = aws ssm put-parameter --name $PARAM_NAME --value $JSON_VALUE --type "String" --overwrite --region $REGION 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Success! Parameter updated: $PARAM_NAME" -ForegroundColor Green
        Write-Host ""
        Write-Host "Verifying parameter value:" -ForegroundColor Blue
        
        $paramValue = aws ssm get-parameter --name $PARAM_NAME --region $REGION --query 'Parameter.Value' --output text
        
        # Display the parameter value
        Write-Host $paramValue -ForegroundColor Cyan
        
        # Try to pretty print JSON if jq is available
        try {
            $paramValue | jq . 2>$null
        } catch {
            # If jq not available, just show raw value
        }
    } else {
        Write-Host ""
        Write-Host "❌ Failed to update parameter" -ForegroundColor Red
        Write-Host "Error output: $result" -ForegroundColor Red
        Write-Host ""
        Write-Host "Trying alternative: Without --overwrite (in case parameter doesn't exist)..." -ForegroundColor Yellow
        
        # Alternative: Try without overwrite first (in case it doesn't exist)
        $result2 = aws ssm put-parameter --name $PARAM_NAME --value $JSON_VALUE --type "String" --region $REGION 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Success! Parameter created." -ForegroundColor Green
        } else {
            Write-Host "❌ Both methods failed." -ForegroundColor Red
            Write-Host ""
            Write-Host "Error: $result2" -ForegroundColor Red
            Write-Host ""
            Write-Host "Manual command to try:" -ForegroundColor Yellow
            Write-Host "  aws ssm put-parameter --name `"$PARAM_NAME`" --value '$JSON_VALUE' --type String --overwrite --region $REGION"
        }
    }
} catch {
    Write-Host "❌ Exception occurred: $_" -ForegroundColor Red
}

