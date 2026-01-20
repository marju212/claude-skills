# Unit Test Writing

## Category
Testing

## Description
Writing effective unit tests to validate individual functions, methods, or components in isolation. This skill covers test structure, assertions, mocking, and test-driven development practices.

## Use Cases
- Validating function behavior with different inputs
- Ensuring code changes don't break existing functionality
- Documenting expected behavior through tests
- Practicing test-driven development (TDD)
- Building confidence in code quality

## Prerequisites
- Understanding of the testing framework for your language
- Knowledge of assertions and test structure
- Familiarity with mocking/stubbing concepts
- Basic understanding of the code being tested

## Implementation

### Basic Example (JavaScript with Jest)

```javascript
// math.js
function add(a, b) {
  return a + b;
}

function divide(a, b) {
  if (b === 0) {
    throw new Error('Cannot divide by zero');
  }
  return a / b;
}

module.exports = { add, divide };

// math.test.js
const { add, divide } = require('./math');

describe('Math operations', () => {
  describe('add', () => {
    test('adds two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    test('adds negative numbers', () => {
      expect(add(-1, -1)).toBe(-2);
    });

    test('adds zero', () => {
      expect(add(5, 0)).toBe(5);
    });
  });

  describe('divide', () => {
    test('divides two numbers', () => {
      expect(divide(10, 2)).toBe(5);
    });

    test('throws error when dividing by zero', () => {
      expect(() => divide(10, 0)).toThrow('Cannot divide by zero');
    });
  });
});
```

### Advanced Example (Python with pytest)

```python
# user_service.py
from typing import Optional
from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    email: str
    active: bool = True

class UserRepository:
    def find_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    def save(self, user: User) -> User:
        raise NotImplementedError

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_active_user(self, user_id: int) -> Optional[User]:
        user = self.repository.find_by_id(user_id)
        if user and user.active:
            return user
        return None

    def create_user(self, username: str, email: str) -> User:
        if not username or not email:
            raise ValueError("Username and email are required")
        
        if '@' not in email:
            raise ValueError("Invalid email format")
        
        user = User(id=0, username=username, email=email)
        return self.repository.save(user)

# test_user_service.py
import pytest
from unittest.mock import Mock, MagicMock
from user_service import User, UserService, UserRepository

class TestUserService:
    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository for testing"""
        return Mock(spec=UserRepository)

    @pytest.fixture
    def service(self, mock_repository):
        """Create a UserService instance with mock repository"""
        return UserService(mock_repository)

    def test_get_active_user_returns_user_when_active(self, service, mock_repository):
        # Arrange
        user = User(id=1, username="john", email="john@example.com", active=True)
        mock_repository.find_by_id.return_value = user

        # Act
        result = service.get_active_user(1)

        # Assert
        assert result == user
        mock_repository.find_by_id.assert_called_once_with(1)

    def test_get_active_user_returns_none_when_inactive(self, service, mock_repository):
        # Arrange
        user = User(id=1, username="john", email="john@example.com", active=False)
        mock_repository.find_by_id.return_value = user

        # Act
        result = service.get_active_user(1)

        # Assert
        assert result is None

    def test_get_active_user_returns_none_when_not_found(self, service, mock_repository):
        # Arrange
        mock_repository.find_by_id.return_value = None

        # Act
        result = service.get_active_user(999)

        # Assert
        assert result is None

    @pytest.mark.parametrize("username,email", [
        ("john", "john@example.com"),
        ("jane_doe", "jane.doe@company.org"),
        ("user123", "user@test.co.uk"),
    ])
    def test_create_user_with_valid_data(self, service, mock_repository, username, email):
        # Arrange
        expected_user = User(id=1, username=username, email=email)
        mock_repository.save.return_value = expected_user

        # Act
        result = service.create_user(username, email)

        # Assert
        assert result.username == username
        assert result.email == email
        mock_repository.save.assert_called_once()

    @pytest.mark.parametrize("username,email,error_message", [
        ("", "john@example.com", "Username and email are required"),
        ("john", "", "Username and email are required"),
        ("john", "invalid-email", "Invalid email format"),
    ])
    def test_create_user_with_invalid_data(self, service, username, email, error_message):
        # Act & Assert
        with pytest.raises(ValueError, match=error_message):
            service.create_user(username, email)
```

## Best Practices
- **Follow AAA pattern**: Arrange (setup), Act (execute), Assert (verify)
- **Test one thing at a time**: Each test should verify a single behavior
- **Use descriptive test names**: Names should explain what is being tested and expected outcome
- **Keep tests independent**: Tests should not depend on each other or shared state
- **Use fixtures/setup methods**: Avoid duplication by sharing common setup code
- **Mock external dependencies**: Isolate the unit under test from databases, APIs, etc.
- **Test edge cases**: Include boundary conditions, null values, empty collections, etc.
- **Test error conditions**: Verify that errors are handled correctly
- **Keep tests fast**: Unit tests should run quickly to encourage frequent execution
- **Maintain tests**: Update tests when requirements change

## Common Pitfalls
- **Testing implementation details**: Focus on behavior, not internal implementation
- **Over-mocking**: Don't mock everything; test real integration where appropriate
- **Unclear test failures**: Ensure assertion messages clearly indicate what went wrong
- **Brittle tests**: Tests that break with minor, unrelated code changes
- **Ignoring test coverage**: Use coverage tools but don't chase 100% blindly
- **Not running tests regularly**: Tests are only valuable if they're run frequently
- **Duplicate test logic**: Use parameterized tests to avoid repetition

## Related Skills
- [Integration Testing](./integration-testing.md)
- [Test-Driven Development](./tdd-workflow.md)
- [Mocking and Stubbing](./mocking-dependencies.md)

## Resources
- [Jest Documentation](https://jestjs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Unit Testing Best Practices](https://testdriven.io/blog/testing-best-practices/)
- [Test-Driven Development by Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/)
