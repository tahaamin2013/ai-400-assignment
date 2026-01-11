---
name: daily-code-review
description: Reviews code changes before commit, checking for bugs, missing error handling, and best practices. Use before committing code to ensure quality and catch common issues.
---

# Daily Code Review

Review code changes systematically to catch bugs, security issues, and violations of best practices.

## Review Checklist

### Error Handling

- [ ] Check for missing `try/except` blocks around I/O operations
- [ ] Verify `HTTPException` is used for FastAPI errors
- [ ] Ensure database operations handle `None` returns
- [ ] Check for uncaught exceptions in async code

### Import Hygiene

- [ ] Verify all imports are actually used
- [ ] Check for unused `from x import *` statements
- [ ] Ensure imports are at the top of the file
- [ ] Group imports: stdlib, third-party, local

### Security & Configuration

- [ ] Look for hardcoded values that should be environment variables
- [ ] Check for exposed secrets (API keys, passwords)
- [ ] Verify user input is validated
- [ ] Check for SQL injection vulnerabilities
- [ ] Ensure sensitive data isn't logged

### Code Quality

- [ ] Functions have proper docstrings
- [ ] Type hints are present for parameters and returns
- [ ] Variable names are descriptive
- [ ] Complex logic has comments explaining "why"
- [ ] No dead code or commented-out code blocks

### FastAPI Specific

- [ ] Status codes are appropriate (201 for create, 404 for not found)
- [ ] Response models are defined and used
- [ ] Dependency injection is used for sessions/clients
- [ ] CORS is configured if needed
- [ ] Routes are grouped in APIRouter

### Database/SQLModel

- [ ] `table=True` is set for database models
- [ ] Foreign keys are properly defined
- [ ] Relationships use `back_populates`
- [ ] Timestamp fields have defaults
- [ ] Query results handle empty lists

## Common Issues to Flag

```python
# MISSING ERROR HANDLING
# Bad:
data = fetch_from_api(url)

# Good:
try:
    data = fetch_from_api(url)
except requests.RequestException as e:
    raise HTTPException(status_code=503, detail="External API unavailable")

# HARDCODED VALUES
# Bad:
DATABASE_URL = "postgresql://user:pass@localhost/db"

# Good:
DATABASE_URL = os.getenv("DATABASE_URL")

# MISSING VALIDATION
# Bad:
@app.post("/users")
def create_user(email: str, password: str):
    ...

# Good:
class UserCreate(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8)

@app.post("/users")
def create_user(user: UserCreate):
    ...

# NO TYPE HINTS
# Bad:
def get_user(id):
    ...

# Good:
def get_user(id: int) -> Optional[User]:
    ...
```

## Review Workflow

1. **Read the diff**: Focus on changed lines
2. **Run through checklist**: Check each category
3. **Note issues**: List line numbers and specific problems
4. **Suggest fixes**: Provide concrete improvements
5. **Verify fixes**: Recheck after changes

## Report Format

```
Code Review Report
==================

Files Reviewed: N
Issues Found: N

Critical Issues:
- [file:line] description

Warnings:
- [file:line] description

Suggestions:
- [file:line] description
```
