# API Endpoint Creation

## Category
Web Development

## Description
Creating RESTful API endpoints using popular web frameworks. This skill covers designing, implementing, and testing HTTP endpoints that follow REST principles.

## Use Cases
- Building backend services for web or mobile applications
- Creating microservices with HTTP interfaces
- Developing data access layers
- Implementing CRUD operations via HTTP

## Prerequisites
- Understanding of HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Familiarity with REST principles
- Basic knowledge of a web framework (Express.js, Flask, FastAPI, etc.)
- Understanding of JSON data format

## Implementation

### Basic Example (Express.js)

```javascript
const express = require('express');
const app = express();

app.use(express.json());

// GET endpoint to retrieve a resource
app.get('/api/users/:id', (req, res) => {
  const userId = req.params.id;
  // In practice, fetch from database
  res.json({ id: userId, name: 'John Doe', email: 'john@example.com' });
});

// POST endpoint to create a resource
app.post('/api/users', (req, res) => {
  const { name, email } = req.body;
  // In practice, save to database
  const newUser = { id: Date.now(), name, email };
  res.status(201).json(newUser);
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### Advanced Example (Python FastAPI)

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional

app = FastAPI()

# Data model with validation
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    active: bool = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = None

# In-memory storage (use database in production)
users_db = {}
next_id = 1

@app.get("/api/users", response_model=List[User])
async def list_users(active_only: bool = False):
    """List all users with optional filtering"""
    users = list(users_db.values())
    if active_only:
        users = [u for u in users if u.active]
    return users

@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a specific user by ID"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.post("/api/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    """Create a new user"""
    global next_id
    user.id = next_id
    users_db[next_id] = user
    next_id += 1
    return user

@app.patch("/api/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    """Partially update a user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    stored_user = users_db[user_id]
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(stored_user, field, value)
    
    return stored_user

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete a user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
```

## Best Practices
- **Use appropriate HTTP methods**: GET for retrieval, POST for creation, PUT/PATCH for updates, DELETE for deletion
- **Return proper status codes**: 200 for success, 201 for creation, 204 for no content, 404 for not found, 400 for bad request
- **Validate input data**: Use schema validation libraries (Pydantic, Joi, etc.)
- **Use consistent URL patterns**: Follow REST conventions like `/api/resources/:id`
- **Handle errors gracefully**: Return meaningful error messages
- **Version your API**: Include version in URL (e.g., `/api/v1/users`) for future compatibility
- **Document endpoints**: Use tools like Swagger/OpenAPI for API documentation
- **Implement authentication/authorization**: Protect endpoints that require it

## Common Pitfalls
- **Inconsistent naming**: Stick to plural nouns for collections (e.g., `/users` not `/user`)
- **Using GET for actions that modify data**: Use POST, PUT, PATCH, or DELETE instead
- **Not validating input**: Always validate and sanitize user input to prevent security issues
- **Returning too much data**: Use pagination for large datasets and field selection where appropriate
- **Poor error handling**: Avoid exposing internal errors; return clean, actionable messages
- **Not handling edge cases**: Consider what happens with invalid IDs, missing data, etc.

## Related Skills
- [JSON Data Validation](./json-validation.md)
- [Database Integration](../data-processing/database-queries.md)
- [Authentication & Authorization](./api-authentication.md)

## Resources
- [REST API Tutorial](https://restfulapi.net/)
- [Express.js Documentation](https://expressjs.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [HTTP Status Codes](https://httpstatuses.com/)
