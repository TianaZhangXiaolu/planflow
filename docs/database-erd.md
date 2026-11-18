
# Database Entity Relationship Diagram

PlanFlow uses PostgreSQL as its relational database.

## ER Diagram

```mermaid
erDiagram
    USER ||--o{ PROJECT : owns
    PROJECT ||--o{ TASK : contains
    PROJECT ||--o{ CATEGORY : has
    CATEGORY o|--o{ TASK : categorizes

    USER {
        int id PK
        string username
        string password
    }

    PROJECT {
        int id PK
        int user_id FK
        string name
        text description
        datetime created_at
        datetime updated_at
    }

    CATEGORY {
        int id PK
        int project_id FK
        string name
        datetime created_at
    }

    TASK {
        int id PK
        int project_id FK
        int category_id FK "nullable"
        string title
        text description
        boolean is_completed
        datetime created_at
        datetime updated_at
    }
```

## Relationships

- One user can own multiple projects.
- One project can contain multiple tasks.
- One project can have multiple categories.
- A task belongs to one project.
- A task can optionally belong to one category.
- Each category belongs to one project.

## Referential Integrity

- Deleting a project cascades deletion to its associated tasks and categories.
- Deleting a category sets the associated tasks' category reference to `NULL`.
- Tasks must belong to a project.
