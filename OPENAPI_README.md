# OpenAPI Interview Questions & Development Guide

## Table of Contents
1. [Interview Questions](#interview-questions)
2. [Developing OpenAPI Specs with UI Tools](#developing-with-ui-tools)
3. [Developing OpenAPI Specs with Python](#developing-with-python)

---

## Interview Questions

### Basic Level

**Q1: What is OpenAPI Specification?**
- OpenAPI Specification (OAS) is a standard, **language-agnostic interface description for HTTP APIs**
- Allows both humans and computers to understand API capabilities without accessing source code
- Previously known as Swagger Specification (versions 1.0-2.0)
- Current version is OpenAPI 3.1.x

**Q2: What are the main components of an OpenAPI document?**
- `openapi`: Version of OpenAPI Specification
- `info`: Metadata about the API (title, version, description)
- `servers`: API server URLs
- `paths`: Available endpoints and operations
- `components`: Reusable schemas, parameters, responses
- `security`: Security mechanisms
- `tags`: Grouping of operations

**Q3: What's the difference between OpenAPI 2.0 and 3.0?**
- Server definitions (host/basePath vs servers array)
- Request body handling (parameters vs requestBody)
- Multiple response examples support
- Callback support in 3.0
- Links between operations in 3.0
- Better security scheme definitions

**Q4: What are the HTTP methods supported in OpenAPI?**
- GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, TRACE

**Q5: How do you define path parameters in OpenAPI?**
```yaml
paths:
  /users/{userId}:
    get:
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
```

### Intermediate Level

**Q6: What is the $ref keyword used for?**
- References reusable components within the spec
- Reduces duplication and improves maintainability
- Can reference local components or external files
```yaml
$ref: '#/components/schemas/User'
$ref: './common.yaml#/components/schemas/Error'
```

**Q7: How do you handle API versioning in OpenAPI?**
- URL path versioning: `/v1/users`, `/v2/users`
- Header versioning: `Accept: application/vnd.api.v1+json`
- Query parameter: `/users?version=1`
- Server-level versioning in servers array

**Q8: Explain the difference between schema and example in OpenAPI**
- `schema`: Defines the structure and data types
- `example`: Provides sample data for documentation
- `examples`: Multiple named examples (OpenAPI 3.0+)

**Q9: How do you document authentication in OpenAPI?**
```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
security:
  - bearerAuth: []
```

**Q10: What are callbacks in OpenAPI 3.0?**
- Define webhook/callback requests that the API will make
- Useful for async operations where server calls client
- Documented under the operation that triggers the callback

### Advanced Level

**Q11: How do you handle polymorphism in OpenAPI?**
```yaml
oneOf:  # Exactly one schema must match
  - $ref: '#/components/schemas/Cat'
  - $ref: '#/components/schemas/Dog'
anyOf:  # One or more schemas must match
  - $ref: '#/components/schemas/Cat'
  - $ref: '#/components/schemas/Dog'
allOf:  # All schemas must match (composition)
  - $ref: '#/components/schemas/Animal'
  - type: object
    properties:
      breed: string
```

**Q12: What is discriminator and when would you use it?**
- Helps identify which schema to use in polymorphic scenarios
- Improves performance by avoiding schema validation attempts
```yaml
discriminator:
  propertyName: petType
  mapping:
    cat: '#/components/schemas/Cat'
    dog: '#/components/schemas/Dog'
```

**Q13: How do you document file uploads in OpenAPI 3.0?**
```yaml
requestBody:
  content:
    multipart/form-data:
      schema:
        type: object
        properties:
          file:
            type: string
            format: binary
          metadata:
            type: object
```

**Q14: What are links in OpenAPI and how are they used?**
- Define relationships between operations
- Allow navigation from one operation's response to another operation
- Useful for HATEOAS-style APIs

**Q15: How do you handle API deprecation in OpenAPI?**
```yaml
paths:
  /old-endpoint:
    get:
      deprecated: true
      description: "Use /new-endpoint instead"
```

**Q16: What tools can validate OpenAPI specifications?**
- Swagger Editor
- Spectral (linting)
- OpenAPI Generator validators
- Redocly CLI
- Postman

**Q17: How do you document rate limiting in OpenAPI?**
- Use custom headers in responses
- Document in description fields
- Use extensions like `x-rate-limit`
```yaml
responses:
  '200':
    headers:
      X-RateLimit-Limit:
        schema:
          type: integer
      X-RateLimit-Remaining:
        schema:
          type: integer
```

**Q18: What are OpenAPI extensions and when would you use them?**
- Custom properties starting with `x-`
- Vendor-specific functionality
- Tool-specific metadata
- Example: `x-amazon-apigateway-integration`

---

## Developing with UI Tools

### 1. Swagger Editor (Online/Desktop)

**Online Version:**
- Visit: https://editor.swagger.io
- Write YAML/JSON in left pane
- See live preview on right
- Validate in real-time
- Generate server/client code

**Features:**
- Syntax highlighting
- Auto-completion
- Real-time validation
- Interactive documentation
- Code generation

**Workflow:**
1. Start with basic structure
2. Define paths and operations
3. Add schemas to components
4. Reference schemas using $ref
5. Add examples and descriptions
6. Validate and test
7. Export specification

### 2. Stoplight Studio

**Features:**
- Visual form-based editor
- Code editor mode
- Mock servers
- Design-first approach
- Git integration
- Collaboration features

**Getting Started:**
1. Download from stoplight.io
2. Create new API project
3. Use visual forms to add endpoints
4. Switch to code view for advanced editing
5. Test with built-in mock server
6. Publish documentation

### 3. Postman

**Features:**
- Import/Export OpenAPI specs
- Generate from collections
- Visual schema builder
- API testing integration
- Team collaboration

**Workflow:**
1. Create API in Postman
2. Define schema for each endpoint
3. Add examples and tests
4. Export as OpenAPI 3.0
5. Share with team

### 4. SwaggerHub

**Features:**
- Cloud-based collaboration
- Version control
- Auto-mocking
- API standardization
- Integration with CI/CD

**Usage:**
1. Sign up at swaggerhub.com
2. Create new API
3. Edit in browser
4. Collaborate with team
5. Publish documentation
6. Integrate with tools

### 5. Redocly

**Features:**
- Beautiful documentation
- Multi-file specs
- Linting and validation
- Custom branding
- Developer portal

---

## Developing with Python

### Method 1: Manual YAML/JSON Creation

```python
import yaml
import json

# Define OpenAPI spec as Python dict
openapi_spec = {
    "openapi": "3.0.3",
    "info": {
        "title": "User Management API",
        "version": "1.0.0",
        "description": "API for managing users"
    },
    "servers": [
        {
            "url": "https://api.example.com/v1",
            "description": "Production server"
        }
    ],
    "paths": {
        "/users": {
            "get": {
                "summary": "List all users",
                "operationId": "listUsers",
                "tags": ["users"],
                "parameters": [
                    {
                        "name": "limit",
                        "in": "query",
                        "schema": {"type": "integer", "default": 10}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/User"}
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Create a user",
                "operationId": "createUser",
                "tags": ["users"],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserInput"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "User created",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        }
                    }
                }
            }
        },
        "/users/{userId}": {
            "get": {
                "summary": "Get user by ID",
                "operationId": "getUserById",
                "tags": ["users"],
                "parameters": [
                    {
                        "name": "userId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "User found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        }
                    },
                    "404": {
                        "description": "User not found"
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "required": ["id", "username", "email"],
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "username": {"type": "string", "example": "johndoe"},
                    "email": {"type": "string", "format": "email", "example": "john@example.com"},
                    "createdAt": {"type": "string", "format": "date-time"}
                }
            },
            "UserInput": {
                "type": "object",
                "required": ["username", "email"],
                "properties": {
                    "username": {"type": "string", "minLength": 3},
                    "email": {"type": "string", "format": "email"},
                    "password": {"type": "string", "minLength": 8}
                }
            }
        },
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    },
    "security": [
        {"bearerAuth": []}
    ]
}

# Save as YAML
with open('openapi.yaml', 'w') as f:
    yaml.dump(openapi_spec, f, default_flow_style=False, sort_keys=False)

# Save as JSON
with open('openapi.json', 'w') as f:
    json.dump(openapi_spec, f, indent=2)

print("OpenAPI specification created successfully!")
```

### Method 2: Using Flask with flask-smorest

```python
from flask import Flask
from flask_smorest import Api, Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['API_TITLE'] = 'User Management API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = Api(app)

# Define schemas
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)

class UserInputSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class QueryArgsSchema(Schema):
    limit = fields.Int(missing=10)
    offset = fields.Int(missing=0)

# Create blueprint
blp = Blueprint('users', __name__, url_prefix='/users', description='User operations')

@blp.route('/')
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    @blp.arguments(QueryArgsSchema, location='query')
    def get(self, args):
        """List all users"""
        # Implementation
        users = []  # Fetch from database
        return users
    
    @blp.arguments(UserInputSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """Create a new user"""
        # Implementation
        new_user = {}  # Create in database
        return new_user

@blp.route('/<int:user_id>')
class UserById(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get user by ID"""
        # Implementation
        user = {}  # Fetch from database
        return user
    
    @blp.arguments(UserInputSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        """Update user"""
        # Implementation
        return user_data
    
    @blp.response(204)
    def delete(self, user_id):
        """Delete user"""
        # Implementation
        return ''

api.register_blueprint(blp)

if __name__ == '__main__':
    app.run(debug=True)
```

### Method 3: Using FastAPI (Auto-generates OpenAPI)

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="User Management API",
    description="API for managing users",
    version="1.0.0",
    docs_url="/swagger-ui",
    redoc_url="/redoc"
)

# Define models
class UserInput(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "secretpass123"
            }
        }

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "created_at": "2024-01-10T10:00:00Z"
            }
        }

# Endpoints
@app.get("/users", response_model=List[User], tags=["users"])
async def list_users(
    limit: int = Query(10, description="Number of users to return"),
    offset: int = Query(0, description="Number of users to skip")
):
    """
    Retrieve a list of users.
    
    - **limit**: Maximum number of users to return
    - **offset**: Number of users to skip
    """
    # Implementation
    users = []
    return users

@app.post("/users", response_model=User, status_code=201, tags=["users"])
async def create_user(user: UserInput):
    """
    Create a new user.
    
    - **username**: Unique username
    - **email**: Valid email address
    - **password**: User password (min 8 characters)
    """
    # Implementation
    new_user = User(
        id=1,
        username=user.username,
        email=user.email,
        created_at=datetime.now()
    )
    return new_user

@app.get("/users/{user_id}", response_model=User, tags=["users"])
async def get_user(user_id: int):
    """
    Get a specific user by ID.
    """
    # Implementation
    user = None  # Fetch from database
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User, tags=["users"])
async def update_user(user_id: int, user: UserInput):
    """Update an existing user."""
    # Implementation
    updated_user = User(
        id=user_id,
        username=user.username,
        email=user.email,
        created_at=datetime.now()
    )
    return updated_user

@app.delete("/users/{user_id}", status_code=204, tags=["users"])
async def delete_user(user_id: int):
    """Delete a user."""
    # Implementation
    return None

# Access OpenAPI spec at: http://localhost:8000/openapi.json
# Access Swagger UI at: http://localhost:8000/swagger-ui
# Access ReDoc at: http://localhost:8000/redoc

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Method 4: Using apispec Library

```python
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import Schema, fields

# Create spec
spec = APISpec(
    title="User Management API",
    version="1.0.0",
    openapi_version="3.0.3",
    plugins=[MarshmallowPlugin()],
    info={
        "description": "API for managing users",
        "contact": {
            "email": "api@example.com"
        }
    },
    servers=[
        {"url": "https://api.example.com/v1", "description": "Production"}
    ]
)

# Define schemas
class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime()

class UserInputSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

# Add schemas to spec
spec.components.schema("User", schema=UserSchema)
spec.components.schema("UserInput", schema=UserInputSchema)

# Add paths
spec.path(
    path="/users",
    operations={
        "get": {
            "summary": "List all users",
            "tags": ["users"],
            "parameters": [
                {
                    "name": "limit",
                    "in": "query",
                    "schema": {"type": "integer", "default": 10}
                }
            ],
            "responses": {
                "200": {
                    "description": "Successful response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/User"}
                            }
                        }
                    }
                }
            }
        },
        "post": {
            "summary": "Create a user",
            "tags": ["users"],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/UserInput"}
                    }
                }
            },
            "responses": {
                "201": {
                    "description": "User created",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"}
                        }
                    }
                }
            }
        }
    }
)

# Generate OpenAPI spec
import yaml
with open('openapi_generated.yaml', 'w') as f:
    yaml.dump(spec.to_dict(), f, default_flow_style=False)

print("OpenAPI spec generated!")
print(yaml.dump(spec.to_dict(), default_flow_style=False))
```

### Method 5: Generate from Existing Flask App

```python
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

app = Flask(__name__)

# Create APISpec
spec = APISpec(
    title="User Management API",
    version="1.0.0",
    openapi_version="3.0.3",
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

@app.route('/users', methods=['GET'])
def get_users():
    """Get all users
    ---
    get:
      summary: List all users
      tags:
        - users
      responses:
        200:
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    """
    return jsonify({"users": []})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID
    ---
    get:
      summary: Get user by ID
      tags:
        - users
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        404:
          description: User not found
    """
    return jsonify({"id": user_id, "username": "johndoe"})

# Register routes with spec
with app.test_request_context():
    spec.path(view=get_users)
    spec.path(view=get_user)

# Serve OpenAPI spec
@app.route('/openapi.json')
def get_openapi_spec():
    return jsonify(spec.to_dict())

# Swagger UI
SWAGGER_URL = '/swagger-ui'
API_URL = '/openapi.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "User Management API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Best Practices

1. **Use $ref for reusability** - Define schemas once in components
2. **Add examples** - Help developers understand expected data
3. **Document errors** - Include all possible error responses
4. **Version your API** - Use semantic versioning
5. **Validate your spec** - Use tools like Spectral or Swagger Editor
6. **Keep it DRY** - Don't repeat yourself, use references
7. **Add descriptions** - Make your API self-documenting
8. **Use tags** - Organize endpoints logically
9. **Security first** - Document authentication requirements
10. **Test your spec** - Generate mock servers and test

---

## Tools & Resources

**Validation:**
- Swagger Editor: https://editor.swagger.io
- Spectral: https://stoplight.io/open-source/spectral
- OpenAPI Generator: https://openapi-generator.tech

**Documentation:**
- Swagger UI: https://swagger.io/tools/swagger-ui/
- ReDoc: https://redocly.com/redoc
- RapiDoc: https://rapidocweb.com

**Python Libraries:**
- FastAPI: https://fastapi.tiangolo.com
- flask-smorest: https://flask-smorest.readthedocs.io
- apispec: https://apispec.readthedocs.io
- connexion: https://connexion.readthedocs.io

**Learning:**
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- Swagger Documentation: https://swagger.io/docs/
- OpenAPI Guide: https://oai.github.io/Documentation/
