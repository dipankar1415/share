# AWS Professional Certification Exam Questions

## Question 1: CI/CD Pipeline Architecture

**Scenario:** Your organization is implementing a continuous integration pipeline using AWS managed services. The pipeline needs to automatically build a Python Flask application, create Docker images, and push them to a container registry whenever code changes are committed to a GitHub repository. The solution must use AWS managed services and follow security best practices.

**Question:** Which combination of AWS services and configurations would BEST meet these requirements?

**A.** AWS CodePipeline with GitHub integration, AWS CodeBuild with Ubuntu environment, AWS Systems Manager Parameter Store for secrets, and Docker Hub for container registry

**B.** AWS CodePipeline with AWS CodeCommit, AWS CodeBuild with Amazon Linux environment, AWS Secrets Manager for secrets, and Amazon ECR for container registry

**C.** AWS CodePipeline with GitHub integration, AWS CodeBuild with Ubuntu environment, AWS Secrets Manager for secrets, and Amazon ECR for container registry

**D.** AWS CodePipeline with GitHub integration, AWS CodeBuild with Windows environment, AWS Systems Manager Parameter Store for secrets, and Docker Hub for container registry

**Answer:** A

**Explanation:**

- AWS CodePipeline with GitHub integration provides the orchestration layer
- AWS CodeBuild with Ubuntu environment supports Python Flask applications and Docker operations
- AWS Systems Manager Parameter Store is appropriate for storing Docker Hub credentials securely
- Docker Hub is a valid container registry choice for this scenario
- The privileged mode in CodeBuild is required for Docker operations

---

## Question 2: Security and Permissions

**Scenario:** You are setting up AWS CodeBuild for a CI/CD pipeline that needs to access secrets stored in AWS Systems Manager Parameter Store and build Docker images. The build process requires elevated privileges.

**Question:** What IAM permissions and configurations are REQUIRED for the CodeBuild service role?

**A.** SSM GetParameter permission, CodeBuild service role with privileged mode enabled, and Docker login credentials stored in Parameter Store

**B.** SSM GetParameter permission, CodeBuild service role with privileged mode disabled, and Docker login credentials stored in Secrets Manager

**C.** SSM GetParameter permission, CodeBuild service role with privileged mode enabled, and Docker login credentials stored in Secrets Manager

**D.** SSM GetParameter permission, CodeBuild service role with privileged mode disabled, and Docker login credentials stored in Parameter Store

**Answer:** A

**Explanation:**

- SSM GetParameter permission is required to access secrets from Parameter Store
- Privileged mode must be enabled for Docker operations in CodeBuild
- Parameter Store is a valid choice for storing Docker Hub credentials
- The service role needs appropriate permissions to access these resources

---

## Question 3: Build Specification Configuration

**Scenario:** You need to create a buildspec.yml file for AWS CodeBuild that will build a Python Flask application located in a subdirectory structure. The application has dependencies defined in requirements.txt and needs to be containerized.

**Question:** Which buildspec.yml configuration would correctly build the application?

**A.**

```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.11
  pre_build:
    commands:
      - pip install -r requirements.txt
  build:
    commands:
      - echo Building Docker image
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker push $IMAGE_REPO_NAME:$IMAGE_TAG
```

**B.**

```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.11
  pre_build:
    commands:
      - cd testfolder/sample-python-app
      - pip install -r requirements.txt
  build:
    commands:
      - echo Building Docker image
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker push $IMAGE_REPO_NAME:$IMAGE_TAG
```

**C.**

```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.11
  pre_build:
    commands:
      - pip install -r testfolder/sample-python-app/requirements.txt
  build:
    commands:
      - echo Building Docker image
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker push $IMAGE_REPO_NAME:$IMAGE_TAG
```

**D.**

```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.11
  pre_build:
    commands:
      - cd testfolder/sample-python-app
      - pip install -r requirements.txt
  build:
    commands:
      - echo Building Docker image
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG testfolder/sample-python-app
      - docker push $IMAGE_REPO_NAME:$IMAGE_TAG
```

**Answer:** D

**Explanation:**

- The application is in a subdirectory (testfolder/sample-python-app)
- Need to change directory to the correct location
- Docker build command must specify the correct path to the Dockerfile
- Requirements.txt is relative to the application directory

---

## Question 4: Pipeline Integration

**Scenario:** You have successfully configured AWS CodeBuild to build your application. Now you need to integrate it with AWS CodePipeline to automatically trigger builds when code changes are pushed to your GitHub repository.

**Question:** What is the correct sequence of steps to integrate CodeBuild with CodePipeline?

**A.** Create CodePipeline → Configure GitHub connection → Add Source stage → Add Build stage with CodeBuild → Configure service role

**B.** Create CodePipeline → Configure GitHub connection → Add Source stage → Add Build stage with CodeBuild → Configure service role → Add Deploy stage

**C.** Create CodePipeline → Configure GitHub connection → Add Source stage → Add Build stage with CodeBuild → Configure service role → Test pipeline

**D.** Create CodePipeline → Configure GitHub connection → Add Source stage → Add Build stage with CodeBuild → Configure service role → Add Deploy stage → Test pipeline

**Answer:** A

**Explanation:**

- The basic CI pipeline requires Source and Build stages
- Deploy stage is optional for CI-only pipelines
- Service role configuration is essential for pipeline execution
- Testing the pipeline validates the configuration

---

## Question 5: Error Troubleshooting

**Scenario:** Your AWS CodeBuild project is failing with the error "Cannot connect to the Docker daemon" when trying to build Docker images.

**Question:** What is the MOST LIKELY cause and solution for this error?

**A.** **Cause:** Missing Docker credentials in Parameter Store
**Solution:** Add Docker Hub credentials to Parameter Store and configure environment variables

**B.** **Cause:** CodeBuild environment doesn't have privileged mode enabled
**Solution:** Enable privileged mode in the CodeBuild project environment settings

**C.** **Cause:** Incorrect Dockerfile path in buildspec.yml
**Solution:** Update the Docker build command to use the correct path

**D.** **Cause:** Missing IAM permissions for CodeBuild service role
**Solution:** Add SSM GetParameter permission to the CodeBuild service role

**Answer:** B

**Explanation:**

- "Cannot connect to the Docker daemon" specifically indicates that Docker operations are not allowed
- Privileged mode must be enabled for Docker operations in CodeBuild
- This is a common configuration issue when setting up CI/CD pipelines with Docker

---

## Question 6: Best Practices

**Scenario:** Your organization is implementing CI/CD pipelines for multiple microservices. You need to ensure that sensitive information like API keys, database passwords, and container registry credentials are stored securely and accessed appropriately.

**Question:** Which approach BEST follows AWS security best practices for managing secrets in CI/CD pipelines?

**A.** Store all secrets in AWS Systems Manager Parameter Store with SecureString type, use IAM roles for service access, and implement least privilege access

**B.** Store all secrets in AWS Secrets Manager, use IAM users for service access, and implement least privilege access

**C.** Store all secrets in AWS Systems Manager Parameter Store with String type, use IAM roles for service access, and implement least privilege access

**D.** Store all secrets in AWS Secrets Manager, use IAM roles for service access, and implement least privilege access

**Answer:** D

**Explanation:**

- AWS Secrets Manager is designed for managing secrets and provides automatic rotation capabilities
- IAM roles are preferred over IAM users for service-to-service access
- Least privilege access ensures minimal required permissions
- Secrets Manager provides better integration with other AWS services

---

## Question 7: Infrastructure as Code

**Scenario:** You need to provision the entire CI/CD pipeline infrastructure using Terraform. The infrastructure includes CodePipeline, CodeBuild, IAM roles, and Parameter Store parameters.

**Question:** Which Terraform resources are REQUIRED to provision this infrastructure?

**A.** aws_codepipeline, aws_codebuild_project, aws_iam_role, aws_iam_role_policy_attachment, aws_ssm_parameter

**B.** aws_codepipeline, aws_codebuild_project, aws_iam_role, aws_iam_role_policy_attachment, aws_secretsmanager_secret

**C.** aws_codepipeline, aws_codebuild_project, aws_iam_user, aws_iam_user_policy_attachment, aws_ssm_parameter

**D.** aws_codepipeline, aws_codebuild_project, aws_iam_role, aws_iam_role_policy_attachment, aws_ssm_parameter, aws_ecr_repository

**Answer:** A

**Explanation:**

- aws_codepipeline for the CI/CD pipeline orchestration
- aws_codebuild_project for the build service
- aws_iam_role for service roles (not users)
- aws_iam_role_policy_attachment for attaching policies
- aws_ssm_parameter for storing secrets in Parameter Store
- ECR repository is optional depending on the container registry choice

---

## Question 8: Monitoring and Logging

**Scenario:** You need to implement monitoring and logging for your CI/CD pipeline to track build success rates, identify failures, and maintain audit logs.

**Question:** Which AWS services should you use to implement comprehensive monitoring and logging?

**A.** Amazon CloudWatch Logs, Amazon CloudWatch Metrics, AWS CloudTrail, and Amazon SNS for notifications

**B.** Amazon CloudWatch Logs, Amazon CloudWatch Metrics, AWS CloudTrail, and Amazon SQS for notifications

**C.** Amazon CloudWatch Logs, Amazon CloudWatch Metrics, AWS Config, and Amazon SNS for notifications

**D.** Amazon CloudWatch Logs, Amazon CloudWatch Metrics, AWS CloudTrail, and Amazon EventBridge for notifications

**Answer:** A

**Explanation:**

- CloudWatch Logs for build logs and application logs
- CloudWatch Metrics for performance and success rate monitoring
- CloudTrail for API call auditing and compliance
- SNS for notifications on build failures or successes
- This combination provides comprehensive observability

---

## Question 9: Cost Optimization

**Scenario:** Your organization has multiple CI/CD pipelines running throughout the day. You need to optimize costs while maintaining performance and reliability.

**Question:** Which strategies would BEST optimize costs for your CI/CD pipelines?

**A.** Use smaller compute instances for CodeBuild, implement build caching, set up scheduled builds during off-peak hours, and use spot instances where possible

**B.** Use larger compute instances for CodeBuild, implement build caching, set up scheduled builds during peak hours, and use on-demand instances

**C.** Use smaller compute instances for CodeBuild, disable build caching, set up scheduled builds during off-peak hours, and use spot instances where possible

**D.** Use larger compute instances for CodeBuild, implement build caching, set up scheduled builds during peak hours, and use spot instances where possible

**Answer:** A

**Explanation:**

- Smaller compute instances reduce costs for simple builds
- Build caching reduces build times and resource usage
- Off-peak hour scheduling reduces costs
- Spot instances provide significant cost savings for non-critical workloads

---

## Question 10: Disaster Recovery

**Scenario:** Your CI/CD pipeline is critical for your organization's operations. You need to implement disaster recovery to ensure business continuity in case of regional failures.

**Question:** Which disaster recovery strategy would BEST ensure continuity of your CI/CD operations?

**A.** Implement cross-region replication of CodePipeline artifacts, use multi-region Parameter Store, and implement automated failover to secondary region

**B.** Implement cross-region replication of CodePipeline artifacts, use single-region Parameter Store, and implement manual failover to secondary region

**C.** Implement cross-region replication of CodePipeline artifacts, use multi-region Parameter Store, and implement manual failover to secondary region

**D.** Implement single-region CodePipeline artifacts, use multi-region Parameter Store, and implement automated failover to secondary region

**Answer:** A

**Explanation:**

- Cross-region replication ensures artifacts are available in multiple regions
- Multi-region Parameter Store provides redundancy for secrets
- Automated failover minimizes downtime and manual intervention
- This approach provides the highest level of availability and disaster recovery

---

## Question 11: AWS Organizations and CloudFormation StackSets

**Scenario:** A multi-national company with hundreds of AWS accounts has slowly adopted AWS Organizations with all features enabled. The company has also configured a few Organization Units (OUs) to serve its business objectives. The company has some AWS Identity and Access Management (IAM) roles that need to be configured for every new AWS account created for the company. Also, the security policy mandates enabling AWS CloudTrail for all AWS accounts. The company is looking for an automated solution that can add the mandatory IAM Roles and CloudTrail configurations to all newly created accounts and also delete the resources/configurations when an account leaves the organization without manual intervention.

**Question:** What should a DevOps engineer do to meet these requirements with the minimal overhead?

**A.** From the management account of AWS Organizations, create an AWS CloudFormation stack set to enable AWS Config and deploy your centralized AWS Identity and Access Management (IAM) roles. Configure the stack set to deploy automatically when an account is created through AWS Organizations

**B.** Run automation across multiple accounts using AWS System Manager Automation. Create an AWS resource group from the management account (or any centralized account) and name it exactly the same for all accounts and OUs and add the account ID or OU as a prefix as per standard naming convention. Include the CloudTrail configuration and the IAM role to be created

**C.** From the management account of AWS Organizations, create an Amazon EventBridge rule that is triggered by an AWS account creation API call. Configure an AWS Lambda function to enable CloudTrail logging and to attach the necessary IAM roles to the account

**D.** From the management account of AWS Organizations, enable AWS CloudTrail logs for all member accounts. Similarly, create an IAM role and share it across accounts and OUs of the AWS Organization

**Answer:** A

**Explanation:**

- CloudFormation StackSets allow you to centrally orchestrate AWS CloudFormation enabled services across multiple AWS accounts and regions
- You can deploy centralized IAM roles, provision EC2 instances or Lambda functions across AWS Regions and accounts in your organization
- StackSets simplify the configuration of cross-account permissions and allow for automatic creation and deletion of resources when accounts are joined or removed from your Organization
- Service-managed permission model allows StackSets to automatically configure necessary IAM permissions
- StackSets offer automatic creation or removal of CloudFormation stacks when new AWS accounts join or quit the Organization

---

## Question 12: CodeDeploy Blue/Green Deployment Failure

**Scenario:** A web application is hosted on Amazon EC2 instances behind an Application Load Balancer (ALB). While using CodeDeploy Blue/Green deployment to deploy a new version, the deployment failed during the AllowTraffic lifecycle event. The DevOps team has found no errors in the deployment logs.

**Question:** Which of the following would you identify as the root cause behind the failure of the deployment?

**A.** A scale-in event or any other termination event, during an in-progress deployment, causes the instance to detach from the Amazon EC2 Auto Scaling group and the instance fails the AllowTraffic lifecycle event

**B.** Incorrectly configured health checks on Application Load Balancer (ALB) are responsible for this issue

**C.** The cause of the failure could be a script from the last successful deployment that never runs successfully. Create a new deployment and specify that the ApplicationStop, BeforeBlockTraffic, and AfterBlockTraffic failures should be ignored

**D.** If an instance is terminated between lifecycle events or before the first lifecycle event step starts, then AllowTraffic lifecycle event fails without generating logs

**Answer:** B

**Explanation:**

- In some cases, a Blue/Green deployment fails during the AllowTraffic lifecycle event, but the deployment logs do not indicate the cause for the failure
- This failure is typically due to incorrectly configured health checks in Elastic Load Balancing for the Classic Load Balancer, Application Load Balancer, or Network Load Balancer used to manage traffic for the deployment group
- To resolve the issue, review and correct any errors in the health check configuration for the load balancer
- Other options involve different failure scenarios that would generate logs or are not related to ALB health checks

---

## Question 13: API Gateway SDK Automation

**Scenario:** A company uses an AWS CodePipeline pipeline to deploy updates to the API several times a month. As part of this process, the DevOps team exports the JavaScript SDK for the API from the API Gateway console and uploads it to an Amazon S3 bucket, which is being used as an origin for an Amazon CloudFront distribution. Web clients access the SDK through the CloudFront distribution's endpoint. The goal is to have an automated solution that ensures the latest SDK is always available to clients whenever there's a new API deployment.

**Question:** As an AWS Certified DevOps Engineer - Professional, what solution will you suggest?

**A.** Set up a CodePipeline action that runs immediately after the API deployment stage. Configure this action to invoke an AWS Lambda function. The Lambda function will then download the SDK from API Gateway, upload it to the S3 bucket, and create a CloudFront invalidation for the SDK path

**B.** Set up a CodePipeline action that runs immediately after the API deployment stage. Configure this action to leverage the CodePipeline integration with API Gateway to export the SDK to Amazon S3. Trigger another action that calls the S3 API to invalidate the cache for the SDK path

**C.** Set up an Amazon EventBridge rule on a schedule that is invoked every 5 minutes. Configure this rule to invoke an AWS Lambda function. The Lambda function will then download the SDK from API Gateway, upload it to the S3 bucket, and create a CloudFront invalidation for the SDK path

**D.** Set up an Amazon EventBridge rule that reacts to CreateDeployment events from aws.apigateway. Configure this rule to leverage the CodePipeline integration with API Gateway to export the SDK to Amazon S3. Trigger another action that calls the S3 API to invalidate the cache for the SDK path

**Answer:** A

**Explanation:**

- AWS CodePipeline is a fully managed continuous delivery service that helps automate release pipelines for fast and reliable application and infrastructure updates
- By creating a CodePipeline action with an AWS Lambda function immediately after the API deployment stage, the DevOps team can automate the process of downloading the SDK from API Gateway and uploading it to the S3 bucket
- The Lambda function can create a CloudFront invalidation for the SDK path, ensuring that web clients get the latest SDK without any caching issues
- Other options either use incorrect APIs (S3 API cannot invalidate CloudFront cache) or are inefficient (scheduled checks every 5 minutes)

---

## Question 14: Blue/Green Deployment Strategy

**Scenario:** The flagship application at a company is deployed on Amazon EC2 instances running behind an Application Load Balancer (ALB) within an Auto Scaling group. A DevOps Engineer wants to configure a Blue/Green deployment for this application and has already created launch templates and Auto Scaling groups for both blue and green environments, each deploying to their respective target groups. The ALB can direct traffic to either environment's target group, and an Amazon Route 53 record points to the ALB. The goal is to enable an all-at-once transition of traffic from the software running on the blue environment's EC2 instances to the newly deployed software on the green environment's EC2 instances.

**Question:** What steps should the DevOps Engineer take to fulfill these requirements?

**A.** Set up an all-at-once deployment to the blue environment's EC2 instances. Perform a Route 53 DNS update to point to the green environment's endpoint on the ALB

**B.** Leverage an AWS CLI command to update the ALB and direct traffic to the green environment's target group. Then initiate a rolling restart of the Auto Scaling group for the green environment to deploy the new software on the green environment's EC2 instances

**C.** Initiate a rolling restart of the Auto Scaling group for the green environment to deploy the new software on the green environment's EC2 instances. Once the rolling restart is complete, leverage an AWS CLI command to update the ALB and direct traffic to the green environment's target group

**D.** Initiate a rolling restart of the Auto Scaling group for the green environment to deploy the new software on the green environment's EC2 instances. Perform a Route 53 DNS update to point to the green environment's endpoint on the ALB

**Answer:** C

**Explanation:**

- A Blue/Green deployment is a deployment strategy in which you create two separate, but identical environments
- One environment (blue) is running the current application version and one environment (green) is running the new application version
- Using a Blue/Green deployment strategy increases application availability and reduces deployment risk by simplifying the rollback process if a deployment fails
- The correct sequence is: deploy new software to green environment → test the green environment → redirect traffic to green environment
- Since there is only a single ALB per the given use case, Route 53 DNS updates are not applicable

---

## Question 15: Logging and Monitoring Solution

**Scenario:** An e-commerce company is deploying its flagship application on Amazon EC2 instances. The DevOps team at the company needs a solution to query both the application logs as well as the AWS account API activity.

**Question:** As an AWS Certified DevOps Engineer - Professional, what solution will you recommend to meet these requirements?

**A.** Set up AWS CloudTrail to deliver the API logs to CloudWatch Logs. Leverage the Amazon CloudWatch Agent to deliver logs from the EC2 instances to Amazon CloudWatch Logs. Utilize the CloudWatch Logs Insights to query both sets of logs

**B.** Set up AWS CloudTrail to deliver the API logs to Kinesis Data Streams. Leverage the Amazon CloudWatch Agent to deliver logs from the EC2 instances to Kinesis Data Streams. Direct both the Kinesis Data Streams to direct the stream output to Kinesis Data Analytics for running near-real-time queries on both sets of logs

**C.** Set up AWS CloudTrail to deliver the API logs to Amazon S3. Leverage the Amazon CloudWatch Agent to deliver logs from the EC2 instances to Amazon CloudWatch Logs. Utilize Amazon Athena to query both sets of logs

**D.** Set up AWS CloudTrail to deliver the API logs to Amazon S3. Leverage the Amazon CloudWatch Agent to deliver logs from the EC2 instances to Amazon S3. Utilize Amazon Athena to query both sets of logs

**Answer:** A

**Explanation:**

- CloudTrail is enabled by default for your AWS account and provides a record of events in your AWS account
- You can configure CloudTrail with CloudWatch Logs to monitor your trail API logs and be notified when specific activity occurs
- The CloudWatch agent can collect metrics and logs from Amazon EC2 instances and on-premises servers
- The logs collected by the unified CloudWatch agent are processed and stored in Amazon CloudWatch Logs
- CloudWatch Logs Insights can query both sets of logs (CloudTrail API logs and application logs) from a single interface

---

## Question 16: CodeDeploy Blue/Green with Testing Window

**Scenario:** A production support team manages a web application running on a fleet of Amazon EC2 instances configured with an Application Load balancer (ALB). The instances run in an EC2 Auto Scaling group across multiple Availability Zones. A critical bug fix has to be deployed to the production application. The team needs a deployment strategy that can:
a) Create another fleet of instances with the same capacity and configuration as the original one. b) Continue access to the original application without a downtime c) Transition the traffic to the new fleet when the deployment is fully done. The production test team has requested a two-hour window to complete thorough testing on the new fleet of instances. d) Terminate the original fleet automatically once the test window expires.

**Question:** As a DevOps engineer, which deployment solution will you choose to cater to all the given requirements?

**A.** Use AWS CodeDeploy with a deployment type configured to Blue/Green deployment configuration. To terminate the original fleet after two hours, change the deployment settings of the Blue/Green deployment. Set Original instances value to Terminate the original instances in the deployment group and choose a waiting period of two hours

**B.** Configure AWS Elastic Beanstalk to perform a Blue/Green deployment. This will create a new environment different from the original environment to continue serving the production traffic. Terminate the original environment after two hours and confirm the DNS changes of the new environment have propagated correctly

**C.** Configure AWS Elastic Beanstalk to use rolling deployment policy. Elastic Beanstalk splits the environment's Amazon EC2 instances into batches and deploys the new version of the application to one batch at a time. Production traffic is served unaffected. Use rolling restarts to restart the proxy and application servers running on your environment's instances without downtime

**D.** Use AWS CodeDeploy with a deployment type configured to Blue/Green deployment configuration. To terminate the original fleet after two hours, change the deployment settings of the Blue/Green deployment. Set Original instances value to 'Terminate the original instances in the deployment group' and choose a waiting period of two hours. Choose OneAtATime Deployment configuration setting to deregister the original fleet of instances one at a time to provide increased test time for the production team

**Answer:** A

**Explanation:**

- Traditional deployments with in-place upgrades make it difficult to validate your new application version in a production deployment while also continuing to run the earlier version of the application
- Blue/Green deployments provide a level of isolation between your blue and green application environments
- This helps ensure spinning up a parallel green environment does not affect the resources underpinning your blue environment
- In AWS CodeDeploy Blue/Green deployment type, you can choose "Terminate the original instances in the deployment group" and specify a waiting period
- After traffic is rerouted to the replacement environment, the instances that were deregistered from the load balancer are terminated following the wait period you specify

---

## Question 17: S3 Checksum Behavior

**Scenario:** A developer has uploaded an object of size 100 MB to an Amazon S3 bucket as a single-part direct upload using the REST API that has checksum enabled. The checksum of the object uploaded via the REST API was the checksum of the entire object. Later that day, the developer used the AWS Management Console to rename the object, copy it and edit its metadata. Later, when the developer checked for the checksum of the object updated via the AWS Management Console, the checksum was not the checksum of the entire object. Confused by the behavior, the developer has reached out to you for a possible solution.

**Question:** As an AWS Certified DevOps Engineer - Professional, which of the following options would you identify as the reason for this behavior?

**A.** If an object is greater than 50 MB in size, checksum will be a calculation based on the checksum values of each individual parts. The developer's initial calculation for the REST API based checksum was incorrect. This resulted in the mismatch of the two checksum values

**B.** When you change metadata of an object in S3, the checksum algorithm of the objects changes by default. This is an expected behavior

**C.** A new checksum value for the object, that is calculated based on the checksum values of the individual parts, has been created. This behavior is expected

**D.** If an object is greater than 16 MB in size, checksum will be a calculation based on the checksum values of each individual parts. The developer's initial calculation for the REST API based checksum was incorrect. This resulted in the mismatch of the two checksum values

**Answer:** C

**Explanation:**

- When you perform some operations using the AWS Management Console, Amazon S3 uses a multipart upload if the object is greater than 16 MB in size
- In this case, the checksum is not a direct checksum of the full object, but rather a calculation based on the checksum values of each individual part
- For example, consider an object 100 MB in size that you uploaded as a single-part direct upload using the REST API. The checksum in this case is a checksum of the entire object
- If you later use the console to rename that object, copy it, change the storage class, or edit the metadata, Amazon S3 uses the multipart upload functionality to update the object
- As a result, Amazon S3 creates a new checksum value for the object that is calculated based on the checksum values of the individual parts

---

## Question 18: CloudWatch Cross-Account Observability

**Scenario:** A company has hundreds of AWS accounts and has also created an organization in AWS Organizations to manage the accounts. The company wants a dashboard to seamlessly search, visualize, and analyze CloudWatch metrics data, logs data, and traces (from AWS X-Ray) from all the linked accounts into a single security and operations account. The solution should automatically onboard any new AWS accounts created later in the organization.

**Question:** As a DevOps Engineer, what solution do you suggest to address the given requirements?

**A.** Use the Amazon CloudWatch cross-account observability feature from the CloudWatch console to create the monitoring account and connect the individual AWS accounts to the monitoring account

**B.** Use Amazon CloudWatch cross-account observability to set up security and operations account as the monitoring account and link it with rest of the member accounts of the organization using AWS Organizations

**C.** Create a CloudWatch alarm for the CloudWatch metrics and trigger an event on Amazon EventBridge. Write the metrics data to the Amazon S3 bucket. Use Amazon Athena to create visualizations and dashboards from CloudWatch metrics data, logs data, and traces

**D.** Configure CloudWatch Metric Streams to stream real-time metrics data to Kinesis Data Firehose. Firehose will push the metrics data to Amazon Simple Storage Service (Amazon S3) bucket. configure Amazon Athena to create a dashboard with the metrics data

**Answer:** B

**Explanation:**

- With Amazon CloudWatch cross-account observability, you can monitor and troubleshoot applications that span multiple accounts within a Region
- Seamlessly search, visualize, and analyze your metrics, logs, and traces in any of the linked accounts without account boundaries
- Set up one or more AWS accounts as monitoring accounts and link them with multiple source accounts
- A monitoring account is a central AWS account that can view and interact with observability data generated from source accounts
- AWS recommends that you use Organizations so that new AWS accounts created later in the organization are automatically onboarded to cross-account observability as source accounts
