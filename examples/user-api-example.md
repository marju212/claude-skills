# Example: Building a User API with Testing

This example demonstrates how to combine multiple skills from this repository to build a complete feature.

## Skills Used

- [API Endpoint Creation](../skills/web-development/api-endpoint-creation.md)
- [Unit Test Writing](../skills/testing/unit-test-writing.md)
- [Error Handling Patterns](../skills/general/error-handling-patterns.md)

## Project Structure

```
user-api/
├── src/
│   ├── models/
│   │   └── user.js
│   ├── routes/
│   │   └── users.js
│   ├── middleware/
│   │   └── errorHandler.js
│   └── server.js
├── tests/
│   ├── models/
│   │   └── user.test.js
│   └── routes/
│       └── users.test.js
├── package.json
└── README.md
```

## Implementation

### 1. User Model (src/models/user.js)

```javascript
class User {
  constructor(id, name, email) {
    this.id = id;
    this.name = name;
    this.email = email;
  }

  static validate(userData) {
    const errors = [];

    if (!userData.name || typeof userData.name !== 'string' || userData.name.trim().length === 0) {
      errors.push('Name is required and must be a non-empty string');
    }

    if (!userData.email || !this.isValidEmail(userData.email)) {
      errors.push('Valid email is required');
    }

    if (errors.length > 0) {
      throw new ValidationError(errors);
    }

    return true;
  }

  static isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}

class ValidationError extends Error {
  constructor(errors) {
    super('Validation failed');
    this.name = 'ValidationError';
    this.errors = errors;
    this.statusCode = 400;
  }
}

module.exports = { User, ValidationError };
```

### 2. API Routes (src/routes/users.js)

```javascript
const express = require('express');
const { User, ValidationError } = require('../models/user');

const router = express.Router();

// In-memory storage (use database in production)
const users = new Map();
let nextId = 1;

// GET all users
router.get('/', (req, res) => {
  const userList = Array.from(users.values());
  res.json({ users: userList, count: userList.length });
});

// GET user by ID
router.get('/:id', (req, res, next) => {
  try {
    const id = parseInt(req.params.id);
    const user = users.get(id);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json(user);
  } catch (error) {
    next(error);
  }
});

// POST create user
router.post('/', (req, res, next) => {
  try {
    User.validate(req.body);

    const user = new User(nextId++, req.body.name, req.body.email);
    users.set(user.id, user);

    res.status(201).json(user);
  } catch (error) {
    next(error);
  }
});

// PUT update user
router.put('/:id', (req, res, next) => {
  try {
    const id = parseInt(req.params.id);
    const existingUser = users.get(id);

    if (!existingUser) {
      return res.status(404).json({ error: 'User not found' });
    }

    User.validate(req.body);

    const updatedUser = new User(id, req.body.name, req.body.email);
    users.set(id, updatedUser);

    res.json(updatedUser);
  } catch (error) {
    next(error);
  }
});

// DELETE user
router.delete('/:id', (req, res, next) => {
  try {
    const id = parseInt(req.params.id);

    if (!users.has(id)) {
      return res.status(404).json({ error: 'User not found' });
    }

    users.delete(id);
    res.status(204).send();
  } catch (error) {
    next(error);
  }
});

module.exports = router;
```

### 3. Error Handler Middleware (src/middleware/errorHandler.js)

```javascript
const { ValidationError } = require('../models/user');

function errorHandler(err, req, res, next) {
  console.error('Error:', err);

  if (err instanceof ValidationError) {
    return res.status(err.statusCode).json({
      error: err.message,
      details: err.errors
    });
  }

  if (err.name === 'SyntaxError' && err.status === 400 && 'body' in err) {
    return res.status(400).json({
      error: 'Invalid JSON in request body'
    });
  }

  res.status(500).json({
    error: 'Internal server error'
  });
}

module.exports = errorHandler;
```

### 4. Server Setup (src/server.js)

```javascript
const express = require('express');
const userRoutes = require('./routes/users');
const errorHandler = require('./middleware/errorHandler');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Routes
app.use('/api/users', userRoutes);

// Error handling
app.use(errorHandler);

// Start server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}

module.exports = app;
```

### 5. Unit Tests (tests/models/user.test.js)

```javascript
const { User, ValidationError } = require('../../src/models/user');

describe('User Model', () => {
  describe('validate', () => {
    test('validates correct user data', () => {
      const validData = { name: 'John Doe', email: 'john@example.com' };
      expect(() => User.validate(validData)).not.toThrow();
    });

    test('throws error for missing name', () => {
      const invalidData = { email: 'john@example.com' };
      expect(() => User.validate(invalidData)).toThrow(ValidationError);
    });

    test('throws error for empty name', () => {
      const invalidData = { name: '   ', email: 'john@example.com' };
      expect(() => User.validate(invalidData)).toThrow(ValidationError);
    });

    test('throws error for missing email', () => {
      const invalidData = { name: 'John Doe' };
      expect(() => User.validate(invalidData)).toThrow(ValidationError);
    });

    test('throws error for invalid email format', () => {
      const invalidData = { name: 'John Doe', email: 'invalid-email' };
      expect(() => User.validate(invalidData)).toThrow(ValidationError);
    });

    test('includes all errors in ValidationError', () => {
      const invalidData = { name: '', email: 'invalid' };
      
      try {
        User.validate(invalidData);
      } catch (error) {
        expect(error).toBeInstanceOf(ValidationError);
        expect(error.errors).toHaveLength(2);
      }
    });
  });

  describe('isValidEmail', () => {
    test('accepts valid email', () => {
      expect(User.isValidEmail('test@example.com')).toBe(true);
    });

    test('rejects email without @', () => {
      expect(User.isValidEmail('testexample.com')).toBe(false);
    });

    test('rejects email without domain', () => {
      expect(User.isValidEmail('test@')).toBe(false);
    });
  });
});
```

### 6. Integration Tests (tests/routes/users.test.js)

```javascript
const request = require('supertest');
const app = require('../../src/server');

describe('User API Endpoints', () => {
  describe('POST /api/users', () => {
    test('creates a new user', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ name: 'Jane Doe', email: 'jane@example.com' })
        .expect(201);

      expect(response.body).toHaveProperty('id');
      expect(response.body.name).toBe('Jane Doe');
      expect(response.body.email).toBe('jane@example.com');
    });

    test('returns 400 for invalid data', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ name: '', email: 'invalid' })
        .expect(400);

      expect(response.body).toHaveProperty('error');
      expect(response.body).toHaveProperty('details');
    });
  });

  describe('GET /api/users/:id', () => {
    test('retrieves existing user', async () => {
      // First create a user
      const createResponse = await request(app)
        .post('/api/users')
        .send({ name: 'Bob Smith', email: 'bob@example.com' });

      const userId = createResponse.body.id;

      // Then retrieve it
      const response = await request(app)
        .get(`/api/users/${userId}`)
        .expect(200);

      expect(response.body.id).toBe(userId);
      expect(response.body.name).toBe('Bob Smith');
    });

    test('returns 404 for non-existent user', async () => {
      await request(app)
        .get('/api/users/99999')
        .expect(404);
    });
  });
});
```

## Running the Example

```bash
# Install dependencies
npm install express jest supertest

# Run the server
node src/server.js

# Run tests
npm test
```

## Key Takeaways

1. **Modular Design**: Separation of concerns with models, routes, and middleware
2. **Error Handling**: Custom error classes and centralized error middleware
3. **Validation**: Input validation before processing
4. **Testing**: Comprehensive unit and integration tests
5. **REST Principles**: Proper HTTP methods and status codes

## Next Steps

To enhance this example, consider adding:
- Database integration ([Data Processing skills](../skills/data-processing/))
- Authentication ([Web Development skills](../skills/web-development/))
- Docker containerization ([DevOps skills](../skills/devops/))
- More comprehensive test coverage
