---
name: sqlmodel-database-design
description: Creates SQLModel table definitions with proper relationships, constraints, and validation for database schemas. Use when defining database models, table relationships, or request/response models.
---

# SQLModel Database Design

Create SQLModel models with proper structure, relationships, and constraints.

## Core Principles

- Always use `table=True` for database models
- Include `primary_key=True` for id fields
- Use `Field()` for constraints and defaults
- Add `created_at`/`updated_at` timestamps
- Separate request/response models from database models

## Base Model Pattern

```python
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class TimestampMixin(SQLModel):
    """Mixin for timestamp fields."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
```

## Database Model Example

```python
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

# Database table model (table=True)
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, max_length=255)
    username: str = Field(max_length=100)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    items: List["Item"] = Relationship(back_populates="owner")

class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    owner: Optional[User] = Relationship(back_populates="items")
```

## Request/Response Models

```python
# CREATE model - required fields for creation
class UserCreate(SQLModel):
    email: str
    username: str
    password: str

# READ model - fields returned to client (no passwords!)
class UserRead(SQLModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

# UPDATE model - all fields optional for partial updates
class UserUpdate(SQLModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

# With relationships
class ItemRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    owner_id: Optional[int] = None

class UserReadWithItems(UserRead):
    items: List[ItemRead] = []
```

## Field Constraints

```python
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # String constraints
    name: str = Field(max_length=100)
    sku: str = Field(unique=True, index=True)

    # Numeric constraints
    price: float = Field(gt=0)  # greater than 0
    quantity: int = Field(ge=0, default=0)  # greater or equal to 0

    # Optional fields
    description: Optional[str] = Field(default=None, max_length=1000)

    # Default values
    is_available: bool = Field(default=True)
```

## Relationship Types

```python
# One-to-Many
class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    employees: List["Employee"] = Relationship(back_populates="department")

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    department: Optional[Department] = Relationship(back_populates="employees")

# Many-to-Many (requires link table)
class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    courses: List["Course"] = Relationship(back_populates="students", link_model="StudentCourseLink")

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    students: List["Student"] = Relationship(back_populates="courses", link_model="StudentCourseLink")

class StudentCourseLink(SQLModel, table=True):
    student_id: Optional[int] = Field(default=None, foreign_key="student.id", primary_key=True)
    course_id: Optional[int] = Field(default=None, foreign_key="course.id", primary_key=True)
```
