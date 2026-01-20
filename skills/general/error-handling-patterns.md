# Error Handling Patterns

## Category
General

## Description
Implementing robust error handling strategies across different programming languages. This skill covers exception handling, error propagation, graceful degradation, and creating meaningful error messages.

## Use Cases
- Building reliable applications
- Debugging and troubleshooting
- User-friendly error reporting
- System resilience and fault tolerance
- API error responses

## Prerequisites
- Understanding of try-catch or equivalent constructs
- Knowledge of error types in your language
- Awareness of call stack and error propagation
- Understanding of application flow control

## Implementation

### Basic Example (JavaScript)

```javascript
// Basic error handling
function divideNumbers(a, b) {
  try {
    if (typeof a !== 'number' || typeof b !== 'number') {
      throw new TypeError('Arguments must be numbers');
    }
    if (b === 0) {
      throw new Error('Division by zero is not allowed');
    }
    return a / b;
  } catch (error) {
    console.error('Error in divideNumbers:', error.message);
    throw error; // Re-throw for caller to handle
  }
}

// Using error handling in async code
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch user data:', error);
    // Return default or null, depending on requirements
    return null;
  }
}

// Error handling with finally
function processFile(filename) {
  let file;
  try {
    file = openFile(filename);
    const data = file.read();
    return processData(data);
  } catch (error) {
    console.error(`Error processing file ${filename}:`, error);
    throw error;
  } finally {
    // Always executed, even if error thrown
    if (file) {
      file.close();
    }
  }
}
```

### Advanced Example (Multiple Languages)

**Python - Custom Exceptions**

```python
# Custom exception classes
class ValidationError(Exception):
    """Raised when data validation fails"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class DatabaseError(Exception):
    """Raised when database operations fail"""
    pass

class User:
    def __init__(self, email, age):
        self.email = email
        self.age = age

    @staticmethod
    def validate(email, age):
        errors = []
        
        if not email or '@' not in email:
            errors.append(ValidationError('email', 'Invalid email format'))
        
        if not isinstance(age, int) or age < 0 or age > 150:
            errors.append(ValidationError('age', 'Age must be between 0 and 150'))
        
        if errors:
            raise ValidationError('user', 
                                f'Validation failed: {[str(e) for e in errors]}')

def create_user(email, age):
    """Create user with comprehensive error handling"""
    try:
        # Validate input
        User.validate(email, age)
        
        # Create user
        user = User(email, age)
        
        # Save to database (simulated)
        try:
            save_to_database(user)
        except Exception as e:
            raise DatabaseError(f"Failed to save user: {str(e)}") from e
        
        return user
        
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise
    except DatabaseError as e:
        print(f"Database error: {e}")
        # Could implement retry logic here
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

# Context manager for resource handling
from contextlib import contextmanager

@contextmanager
def database_connection(connection_string):
    """Context manager for database connections"""
    conn = None
    try:
        conn = connect_to_database(connection_string)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise DatabaseError(f"Database operation failed: {e}") from e
    finally:
        if conn:
            conn.close()

# Usage
try:
    with database_connection("postgresql://...") as conn:
        result = conn.execute("SELECT * FROM users")
except DatabaseError as e:
    print(f"Database error: {e}")
```

**Go - Explicit Error Handling**

```go
package main

import (
    "errors"
    "fmt"
    "io"
    "os"
)

// Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s with ID %s not found", e.Resource, e.ID)
}

// Error wrapping and unwrapping
func getUserByID(id string) (*User, error) {
    user, err := fetchUserFromDB(id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, &NotFoundError{Resource: "User", ID: id}
        }
        return nil, fmt.Errorf("failed to fetch user %s: %w", id, err)
    }
    return user, nil
}

// Multiple return values for error handling
func divideNumbers(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Error handling with defer
func processFile(filename string) error {
    file, err := os.Open(filename)
    if err != nil {
        return fmt.Errorf("failed to open file %s: %w", filename, err)
    }
    defer file.Close() // Ensure file is closed

    data, err := io.ReadAll(file)
    if err != nil {
        return fmt.Errorf("failed to read file %s: %w", filename, err)
    }

    if err := processData(data); err != nil {
        return fmt.Errorf("failed to process data from %s: %w", filename, err)
    }

    return nil
}

// Panic and recover for exceptional cases
func safeDivide(a, b int) (result int, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("panic recovered: %v", r)
        }
    }()

    if b == 0 {
        panic("division by zero")
    }
    result = a / b
    return result, nil
}
```

**Rust - Result Type**

```rust
use std::fs::File;
use std::io::{self, Read};
use std::num::ParseIntError;

// Custom error types
#[derive(Debug)]
enum AppError {
    Io(io::Error),
    Parse(ParseIntError),
    Validation(String),
}

impl From<io::Error> for AppError {
    fn from(error: io::Error) -> Self {
        AppError::Io(error)
    }
}

impl From<ParseIntError> for AppError {
    fn from(error: ParseIntError) -> Self {
        AppError::Parse(error)
    }
}

// Function returning Result
fn read_number_from_file(filename: &str) -> Result<i32, AppError> {
    let mut file = File::open(filename)?; // ? operator propagates errors
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    
    let number: i32 = contents.trim().parse()?;
    
    if number < 0 {
        return Err(AppError::Validation(
            "Number must be positive".to_string()
        ));
    }
    
    Ok(number)
}

// Pattern matching on Result
fn process_user_input(input: &str) -> Result<i32, String> {
    match input.parse::<i32>() {
        Ok(num) if num > 0 => Ok(num),
        Ok(_) => Err("Number must be positive".to_string()),
        Err(_) => Err("Invalid number format".to_string()),
    }
}

// Using and_then for chaining
fn calculate_and_double(input: &str) -> Result<i32, String> {
    input.parse::<i32>()
        .map_err(|_| "Invalid number".to_string())
        .and_then(|n| {
            if n > 100 {
                Err("Number too large".to_string())
            } else {
                Ok(n * 2)
            }
        })
}
```

## Best Practices
- **Fail fast**: Validate input early and fail quickly with clear errors
- **Use specific exceptions**: Create custom exception types for different error scenarios
- **Include context**: Error messages should explain what went wrong and where
- **Don't swallow errors**: Always handle or propagate errors; don't silently ignore them
- **Log appropriately**: Log errors with sufficient detail for debugging
- **Clean up resources**: Use finally blocks or RAII patterns to ensure cleanup
- **Avoid bare except/catch**: Catch specific exceptions rather than all exceptions
- **Document error conditions**: Specify what errors functions can raise
- **Use error codes or types**: Make error handling explicit in function signatures
- **Graceful degradation**: Provide fallback behavior when possible

## Common Pitfalls
- **Catching too broadly**: Catching all exceptions can hide bugs
- **Ignoring errors**: Not checking return values or catching without handling
- **Poor error messages**: Generic messages like "Error occurred" aren't helpful
- **Not cleaning up**: Forgetting to release resources in error paths
- **Re-throwing incorrectly**: Losing stack trace information
- **Over-engineering**: Creating complex error hierarchies when simple errors suffice
- **Exposing internals**: Error messages revealing sensitive implementation details
- **Not validating input**: Assuming input is valid and catching errors later

## Related Skills
- [Logging Best Practices](./logging-patterns.md)
- [Input Validation](./input-validation.md)
- [Defensive Programming](./defensive-programming.md)

## Resources
- [Error Handling in JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling)
- [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
- [Go Error Handling](https://go.dev/blog/error-handling-and-go)
- [Rust Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- [Exception Handling Best Practices](https://www.toptal.com/qa/how-to-write-testable-code-and-why-it-matters)
