# AWS Certified DevOps Engineer Professional - Study Guide Summary

## Course Overview

This study guide covers the AWS Certified DevOps Engineer Professional (DOP-C02) certification exam. This is an advanced, professional-level course that requires:

- Prior experience with AWS Certified Developer certification (prerequisite)
- AWS Certified SysOps certification (recommended)
- Minimum 2 years of real-world experience
- Strong understanding of AWS services and DevOps practices

## Exam Domains

### Domain 1 - SDLC Automation

#### CI/CD Services

- **AWS CodeCommit**: Private Git repositories (Note: Deprecated July 2024 - use GitHub instead)
- **AWS CodePipeline**: Visual workflow orchestration for CI/CD
- **AWS CodeBuild**: Managed build service with Docker containers
- **AWS CodeDeploy**: Automated application deployment to EC2, Lambda, ECS
- **AWS CodeArtifact**: Artifact management for dependencies
- **Amazon CodeGuru**: ML-powered code reviews and performance recommendations

#### Key Concepts

- **Continuous Integration (CI)**: Automated testing and building on code commits
- **Continuous Delivery (CD)**: Automated deployment with quick releases
- **Deployment Strategies**:
  - All at once
  - Rolling
  - Blue/Green
  - Canary
  - Immutable

#### CodePipeline Features

- Multi-stage workflows (Source → Build → Test → Deploy)
- Artifacts stored in S3
- Manual approval stages
- CloudFormation integration
- Multi-region deployments
- EventBridge integration for monitoring

#### CodeBuild

- Fully managed, serverless build service
- Uses buildspec.yml for build instructions
- Supports Docker, VPC, and environment variables
- Test reports and build badges
- Integration with SSM Parameter Store and Secrets Manager

#### CodeDeploy

- **Deployment Platforms**: EC2/On-premises, Lambda, ECS
- **Deployment Types**: In-place, Blue/Green
- **Hooks**: Lifecycle events for custom scripts
- **Rollback**: Automatic rollback on failure
- **Traffic Shifting**: Linear, Canary, All-at-once

### Domain 2 - Configuration Management and IaC

#### AWS CloudFormation

Declarative infrastructure as code

**Key Components**:

- Resources (mandatory)
- Parameters
- Mappings
- Outputs
- Conditions
- Intrinsic Functions

#### CloudFormation Features

- **Helper Scripts**: cfn-init, cfn-signal, cfn-hup
- **Nested Stacks**: Reusable templates
- **StackSets**: Deploy across multiple accounts/regions
- **Change Sets**: Preview changes before deployment
- **Drift Detection**: Identify manual changes
- **Custom Resources**: Lambda-backed resources for custom logic
- **Dynamic References**: Retrieve secrets from SSM/Secrets Manager

#### AWS Service Catalog

- Self-service portal for approved products
- Products defined as CloudFormation templates
- Portfolio management with IAM permissions
- Launch constraints for minimal user permissions

#### Elastic Beanstalk

Platform as a Service (PaaS) for application deployment

**Deployment Options**:

- All at once
- Rolling
- Rolling with additional batches
- Immutable
- Blue/Green
- Traffic splitting (Canary)

- **Components**: Application, Version, Environment
- **Tiers**: Web Server, Worker

#### AWS SAM (Serverless Application Model)

- Framework for serverless applications
- Simplified CloudFormation syntax
- sam build, sam deploy, sam sync commands
- SAM Accelerate for faster deployments
- Integration with CodeDeploy for Lambda

#### AWS CDK (Cloud Development Kit)

- Define infrastructure using programming languages
- Compiles to CloudFormation templates
- Supports JavaScript, TypeScript, Python, Java, .NET

#### AWS Systems Manager

**Key Features**:

- **Parameter Store**: Secure configuration storage
- **Session Manager**: Secure shell access without SSH
- **Run Command**: Execute commands across instances
- **Patch Manager**: Automated patching
- **State Manager**: Maintain configuration
- **Automation**: Runbooks for common tasks
- **Maintenance Windows**: Scheduled operations

### Domain 3 - Resilient Cloud Solutions

#### Lambda

- **Versions and Aliases**: Immutable versions, mutable aliases
- **Concurrency**: Reserved and provisioned concurrency
- **Cold Starts**: Provisioned concurrency eliminates cold starts
- **Storage**: EFS mounting, ephemeral storage (/tmp)

#### API Gateway

- **Endpoint Types**: Edge-optimized, Regional, Private
- **Features**: Caching, throttling, request validation
- **Deployment**: Stages, canary deployments
- **Security**: IAM, Cognito, Custom Authorizers

#### ECS/EKS

- **Launch Types**: EC2, Fargate
- **Auto Scaling**: Service and capacity provider scaling
- **Task Definitions**: Container configurations
- **Load Balancing**: ALB, NLB integration
- **Logging**: CloudWatch Logs with awslogs driver

#### Kinesis Data Streams

- Real-time data streaming
- **Capacity Modes**: Provisioned, On-demand
- **Retention**: Up to 365 days
- **Consumers**: Lambda, KCL, Kinesis Data Firehose

#### Database Services

- **RDS**: Read replicas, Multi-AZ, automated backups
- **Aurora**: Global databases, auto-scaling replicas
- **DynamoDB**: DAX caching, Global Tables, Streams
- **ElastiCache**: Redis (clustering, replication), Memcached

#### Route 53

- **Routing Policies**: Weighted, Latency, Failover, Geolocation
- **Health Checks**: Endpoint monitoring, failover
- **Multi-region**: Global traffic management

#### Storage Gateway

- Hybrid cloud storage solution
- Bridge between on-premises and S3
- RefreshCache API for file gateway

#### Auto Scaling

- **Scaling Policies**: Target tracking, Step, Scheduled, Predictive
- **Lifecycle Hooks**: Custom actions during scaling
- **Warm Pools**: Pre-initialized instances for faster scaling
- **Termination Policies**: Control which instances terminate first

#### Multi-AZ & Multi-Region

- **Multi-AZ**: High availability within a region
- **Multi-Region**: Disaster recovery, low latency
- **Global Services**: Route 53, CloudFront, S3 CRR, DynamoDB Global Tables

#### Disaster Recovery

**Strategies (fastest to slowest RTO)**:

1. Multi-Site/Hot Site
2. Warm Standby
3. Pilot Light
4. Backup and Restore

- **RPO**: Recovery Point Objective (data loss)
- **RTO**: Recovery Time Objective (downtime)

### Domain 4 - Monitoring and Logging

#### CloudWatch

- **Metrics**: Standard and custom metrics
- **Logs**: Log groups, streams, insights
- **Alarms**: Trigger actions based on thresholds
- **Dashboards**: Visualize metrics
- **Synthetics**: Canary monitoring for endpoints
- **Anomaly Detection**: ML-based anomaly detection

#### CloudWatch Features

- **Metric Streams**: Near real-time streaming to destinations
- **Log Subscriptions**: Real-time processing with Lambda, KDS, KDF
- **Metric Filters**: Create metrics from log events
- **Unified Agent**: Collect system-level metrics and logs

#### Amazon Athena

- Serverless SQL queries on S3 data
- Supports CSV, JSON, Parquet, ORC
- Integration with QuickSight for visualization
- Federated queries across multiple data sources

#### AWS Glue

- Managed ETL service
- Data Catalog for metadata
- Crawlers for automatic schema discovery
- Integration with Athena, Redshift, EMR

### Domain 5 - Incident and Event Response

#### Amazon EventBridge

- Event-driven architecture
- **Event Sources**: AWS services, SaaS, custom applications
- **Event Buses**: Default, Partner, Custom
- **Rules**: Filter and route events to targets
- **Targets**: Lambda, SNS, SQS, Step Functions, etc.
- **Archive & Replay**: Store and replay events

#### S3 Event Notifications

- Trigger actions on S3 events (create, delete, restore)
- **Destinations**: Lambda, SQS, SNS, EventBridge
- EventBridge provides advanced filtering and more destinations

#### AWS Health Dashboard

- **Service History**: Global AWS service health
- **Your Account**: Personalized health events
- EventBridge integration for automated responses

#### EC2 Status Checks

- **System Status**: AWS infrastructure issues
- **Instance Status**: OS/network configuration issues
- **CloudWatch Alarms**: Automated recovery actions

#### CloudTrail

- API call auditing and logging
- **Event Types**: Management, Data, Insights
- **Retention**: 90 days default, longer with S3
- **Integration**: CloudWatch Logs, EventBridge

#### SQS/SNS Dead Letter Queues

- Handle failed message processing
- Redrive to source for reprocessing
- Debugging and troubleshooting

#### AWS X-Ray

- Distributed tracing for microservices
- Performance analysis and bottleneck identification
- Integration with Lambda, API Gateway, ECS, Beanstalk

### Domain 6 - Security and Compliance

#### AWS Organizations

- **Features**: Consolidated billing, SCPs, OU structure
- **Service Control Policies (SCPs)**: Restrict permissions across accounts
- **OrganizationAccountAccessRole**: Cross-account admin access
- **Reserved Instances**: Shared across organization

#### AWS Control Tower

- Automated multi-account environment setup
- **Landing Zone**: Best practice configuration
- **Account Factory**: Automated account provisioning
- **Guardrails**: Preventive (SCPs) and Detective (Config)
- **Customizations**: CfCT, AFC for automated deployments

#### IAM Identity Center (AWS SSO)

- Single sign-on for AWS accounts and applications
- **Permission Sets**: Reusable IAM policies
- **Identity Sources**: Built-in, Active Directory, SAML 2.0
- **ABAC**: Attribute-based access control
- **MFA**: Always-on or context-aware

#### AWS Config

- Resource configuration tracking and compliance
- **Config Rules**: Managed and custom rules
- **Remediation**: Automated fixes with SSM Automation
- **Aggregators**: Multi-account and multi-region compliance
- **Conformance Packs**: Reusable compliance packages

#### AWS WAF (Web Application Firewall)

- Protect web applications from exploits
- **Deployments**: ALB, API Gateway, CloudFront, AppSync
- **Rules**: IP, header, SQL injection, XSS, rate-based
- **Managed Rules**: Pre-configured rule sets

#### AWS Firewall Manager

- Centralized firewall management across organization
- **Policy Types**: WAF, Shield, Security Groups, Network Firewall
- Auto-remediation for non-compliant resources

#### Amazon GuardDuty

- Intelligent threat detection using ML
- **Data Sources**: CloudTrail, VPC Flow, DNS logs, EKS, RDS, S3
- **Findings**: Security issues with severity levels
- **Response**: EventBridge integration for automation
- **Multi-Account**: Administrator/member account structure

#### Amazon Detective

- Root cause analysis for security findings
- Visualizations using ML and graphs
- Integrates with GuardDuty, Macie, Security Hub

#### Amazon Inspector

- Automated security assessments
- **Targets**: EC2 instances, Container images (ECR), Lambda
- **Checks**: Vulnerabilities, network reachability
- SSM Agent required for EC2 instances

#### AWS Secrets Manager

- Secure secret storage with rotation
- **Integration**: RDS automatic password rotation
- **Multi-Region**: Secret replication across regions
- KMS encryption

## Additional Services

#### AWS Application Auto Scaling

- Unified scaling for multiple services
- DynamoDB, ECS, Lambda, Aurora, etc.
- Scaling plans with target tracking, step, and scheduled policies

#### Amazon QuickSight

- Serverless BI and visualization service
- Integration with RDS, Athena, Redshift, S3

#### AWS Tag Editor

- Bulk tag management across resources
- Search tagged/untagged resources

#### Trusted Advisor

- Best practice recommendations
- **Categories**: Cost, Performance, Security, Fault Tolerance, Service Limits
- EventBridge integration for automation

## Exam Preparation Tips

- **Prerequisites**: Complete AWS Developer and SysOps certifications first
- **Experience**: Minimum 2 years hands-on AWS experience
- **Practice**: Use AWS services extensively in real projects
- **Resources**:
  - AWS Exam Readiness course
  - AWS DevOps Blog
  - Practice exams
  - Hands-on labs

### Key Focus Areas

- CI/CD pipelines with CodePipeline
- Infrastructure as Code (CloudFormation, CDK, SAM)
- Container orchestration (ECS, EKS)
- Monitoring and logging (CloudWatch, X-Ray)
- Security and compliance (Organizations, Config, GuardDuty)
- Incident response automation (EventBridge, Lambda)

### Exam Format

- Professional-level certification
- Tests real-world scenarios
- Deep understanding required
- Focus on automation and best practices

## Important Notes

- **CodeCommit Deprecation**: Use GitHub instead (as of July 2024)
- **Serverless Focus**: Lambda, API Gateway, DynamoDB, Fargate
- **Automation**: Everything should be automated (IaC, CI/CD, remediation)
- **Multi-Account**: Organizations and Control Tower are critical
- **Security**: Defense in depth with multiple layers
- **Monitoring**: Comprehensive observability with CloudWatch and X-Ray
