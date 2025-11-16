# AWS Strands Agents vs Amazon Bedrock Agents: A Comparative Analysis

*Based on Real-World Customer Interactions*

---

## Introduction

In the rapidly evolving world of AI agents, AWS has introduced **AWS Strands Agents**, a new approach to building intelligent agent systems. This article compares AWS Strands Agents with the existing **Amazon Bedrock Agents**, highlighting their similarities, differences, pros, and cons based on real-world customer interactions.

## The End Goal of Agents

Before diving into the comparison, let's understand what agents need to achieve:

- Handle multiple questions in one go
- Process different types of questions:
  - "What's the time in New York?"
  - "What's the weather?"
  - "List S3 buckets in my AWS account"
- **Key Requirement**: Figure out the order of operations and execute autonomously
- No manual intervention needed between steps

## How Agents Work: The Tool-Based Approach

LLMs don't have real-time data or AWS account access by default. Agents need to invoke tools to accomplish tasks:

1. Tool 1: Get latitude/longitude of New York City
2. Tool 2: Get time using location
3. Tool 3: Get weather information
4. Tool 4: List S3 buckets using AWS credentials

Both solutions use this tool-based approach, but they differ significantly in implementation.

---

## Amazon Bedrock Agents

### Overview

**Implementation with Bedrock Agents:**

- Uses LLMs hosted in Bedrock
- Implements agents using **Action Groups**
- Each tool = Action Group Function = Lambda Function
- **Best Practice**: Separate Lambda for each tool
- Requires 4 different Lambda functions for our example

### How Bedrock Agents Decide

The agent uses descriptions provided for each Action Group to automatically invoke tools:

- Example descriptions:
  - "Gets latitude/longitude given city name"
  - "Outputs time given latitude/longitude"
- Input parameters must be defined (numeric, decimal, etc.)
- Agent invokes tools based on these descriptions

### Developer Work

**Who writes the code? You, the developer!**

**Example: Time tool Lambda**
- Invoke external API
- Pass location, return time

**Example: S3 buckets Lambda**
- Use AWS boto3 SDK
- `S3.boto3.client.list_buckets()`
- Uses IAM role/AWS credentials

Lambda requires event handlers and infrastructure code.

### Summary: Key Characteristics

- ✅ Works with Bedrock-hosted LLMs only
- ❌ Cannot use external LLMs (e.g., Anthropic Claude directly)
- ❌ Requires coding and managing multiple Lambdas
- ❌ More tools = longer processing time
- ✅ Fully managed infrastructure by AWS
- ✅ Auto-scaling and patching
- ✅ Easy integration with Bedrock Guardrails
- ⚠️ **Tedious and time-consuming to implement**

---

## AWS Strands Agents

### Introduction: The Evolution

AWS Strands takes a different approach:

- Packages all tools, agents, and LLM interaction in **one single codebase**
- Can use Bedrock-hosted LLMs **OR** external LLMs
- **Mind-blowing feature**: Comes with common tools pre-built
- **No coding required** for standard tools
- **No descriptions needed** - Strands figures it out automatically
- **No input/output parameters** required

### Architecture

The architecture flow is straightforward:

- User → Queries → LLM → Agent(s) → Tools
- Demonstrates automatic tool invocation without descriptions

**Key message**: "No Coding Required for Common Tools"

### Demo Setup: Simple Implementation

```python
# Install: pip install strands-agent
# Install: pip install strands-agent-anthropic

from strands_agent import Agent
from strands_agent.models import AnthropicModel

model = AnthropicModel(
    api_key="your-key",
    model_id="claude-3-7-sonnet"
)

agent = Agent(model=model)
# Or use default Bedrock Claude 3.7
```

### Using Tools: Out-of-the-Box

```python
from strands_tools import current_time, http_request, use_aws

agent = Agent(
    model=model,
    tools=[current_time, http_request, use_aws]
)
# No coding, no descriptions needed!
```

### Notable Strands Tools

1. **HTTP Request**
   - Call any API endpoint automatically
   - No coding required

2. **Python Tool**
   - Creates Python code dynamically
   - Trained on AWS codebase

3. **Use AWS**
   - Makes AWS API calls via boto3
   - Natural language commands
   - No coding or descriptions needed

### Demo Results

In a real-world demonstration:

- ✅ **Current time**: Worked instantly with `current_time` tool
- ✅ **S3 buckets**: Listed using `use_aws` tool automatically
- ✅ **Weather**: Used HTTP request to:
  1. Get coordinates from city name
  2. Call National Weather Service API
  3. Return formatted weather data

**All without writing a single line of tool code!**

### Custom Tools in Strands

**Writing Your Own Tools:**

- Use `@tool` decorator
- Write custom functions within the same codebase
- Easy to extend functionality

**Deployment Options:**

- Run locally (as in demo)
- Package as ZIP → AWS Lambda
- Package as container → ECS/EKS
- You manage the infrastructure

### Summary: Key Characteristics

- ✅ Use Bedrock-hosted LLMs **OR** external LLMs
- ✅ 20+ powerful tools included
- ✅ Use tools without coding
- ✅ Automatic tool invocation (no descriptions)
- ✅ Write custom tools easily
- ✅ Single concise codebase
- ✅ Much faster to implement
- ⚠️ You manage infrastructure (Lambda/ECS/EKS)

---

## Side-by-Side Comparison

| Feature              | Bedrock Agents   | AWS Strands        |
| -------------------- | ---------------- | ------------------ |
| LLM Support          | Bedrock only     | Bedrock + External |
| Tool Coding          | Required         | Pre-built tools    |
| Descriptions         | Required         | Automatic          |
| Infrastructure       | Managed by AWS   | You manage         |
| Implementation Speed | Slower           | Faster             |
| Codebase             | Multiple Lambdas | Single codebase    |
| Guardrails           | Easy integration | Manual setup       |

---

## When to Use What?

### Choose the Right Tool for the Job

**Use Bedrock Agents when:**

- You need fully managed infrastructure
- You want AWS to handle scaling/patching
- You need Guardrails integration
- You're okay with slower development

**Use AWS Strands when:**

- You need rapid development
- You want to use external LLMs
- You prefer a single codebase
- You can manage your own infrastructure
- You want maximum flexibility

---

## Conclusion: Key Takeaways

- Both solutions enable autonomous agent workflows
- **Bedrock Agents**: Managed, but requires more coding
- **AWS Strands**: Faster development, but you manage infrastructure
- **Use the right tool for the right job**
- Strands significantly reduces development time
- Bedrock Agents provide more managed services

---

*Code available on GitHub (upon request)*

*Based on real-world customer interactions*

