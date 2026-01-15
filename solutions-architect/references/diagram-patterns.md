# Diagram Patterns

Mermaid templates for common architecture diagrams.

## C4 Model Diagrams

### Level 1: System Context

Shows the system as a single box with users and external systems.

```mermaid
graph TB
    subgraph External
        User[👤 User]
        Admin[👤 Admin]
        ExtPayment[💳 Payment Provider]
        ExtEmail[📧 Email Service]
    end
    
    System[🖥️ Our System]
    
    User -->|Uses| System
    Admin -->|Manages| System
    System -->|Processes payments| ExtPayment
    System -->|Sends emails| ExtEmail
```

### Level 2: Container Diagram

Shows applications, databases, and services within the system.

```mermaid
graph TB
    subgraph Users
        WebUser[👤 Web User]
        MobileUser[📱 Mobile User]
        AdminUser[👤 Admin]
    end
    
    subgraph System [Our System]
        WebApp[🌐 Web App<br/>React SPA]
        MobileApp[📱 Mobile App<br/>React Native]
        API[⚙️ API Service<br/>FastAPI]
        Worker[⚡ Background Worker<br/>Celery]
        DB[(🗄️ Database<br/>PostgreSQL)]
        Cache[(⚡ Cache<br/>Redis)]
        Queue[📬 Message Queue<br/>Redis Pub/Sub]
    end
    
    subgraph External
        Payment[💳 Stripe]
        Email[📧 SendGrid]
        Storage[📁 S3]
    end
    
    WebUser --> WebApp
    MobileUser --> MobileApp
    AdminUser --> WebApp
    
    WebApp --> API
    MobileApp --> API
    
    API --> DB
    API --> Cache
    API --> Queue
    
    Queue --> Worker
    Worker --> DB
    Worker --> Email
    
    API --> Payment
    API --> Storage
```

### Level 3: Component Diagram

Shows internal components of a container. Use sparingly.

```mermaid
graph TB
    subgraph API [API Service]
        Router[🔀 Router<br/>FastAPI Router]
        AuthMiddleware[🔐 Auth Middleware<br/>JWT Validation]
        
        subgraph Controllers
            UserCtrl[User Controller]
            ProjectCtrl[Project Controller]
            BillingCtrl[Billing Controller]
        end
        
        subgraph Services
            UserSvc[User Service]
            ProjectSvc[Project Service]
            BillingSvc[Billing Service]
        end
        
        subgraph Repositories
            UserRepo[User Repository]
            ProjectRepo[Project Repository]
        end
    end
    
    Router --> AuthMiddleware
    AuthMiddleware --> Controllers
    
    UserCtrl --> UserSvc
    ProjectCtrl --> ProjectSvc
    BillingCtrl --> BillingSvc
    
    UserSvc --> UserRepo
    ProjectSvc --> ProjectRepo
    BillingSvc --> UserRepo
    
    UserRepo --> DB[(Database)]
    ProjectRepo --> DB
```

---

## Sequence Diagrams

### Basic Request Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant D as Database
    
    C->>A: POST /users
    A->>A: Validate input
    A->>D: INSERT user
    D-->>A: User record
    A-->>C: 201 Created
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant D as Database
    participant R as Redis
    
    C->>A: POST /auth/login
    A->>D: Find user by email
    D-->>A: User record
    A->>A: Verify password
    A->>A: Generate JWT
    A->>D: Store refresh token
    D-->>A: OK
    A-->>C: {access_token, refresh_token}
    
    Note over C,A: Later, access token expires
    
    C->>A: POST /auth/refresh
    A->>D: Validate refresh token
    D-->>A: Token valid
    A->>A: Generate new JWT
    A->>D: Rotate refresh token
    A-->>C: {access_token, refresh_token}
```

### Async Processing Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant Q as Queue
    participant W as Worker
    participant E as Email Service
    participant D as Database
    
    C->>A: POST /orders
    A->>D: Create order (pending)
    A->>Q: Publish order.created
    A-->>C: 202 Accepted
    
    Note over Q,W: Async processing
    
    Q->>W: order.created event
    W->>D: Update order status
    W->>E: Send confirmation email
    E-->>W: Sent
    W->>D: Mark order confirmed
```

### Error Handling Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant D as Database
    participant M as Monitoring
    
    C->>A: POST /resource
    A->>D: Query
    D--xA: Connection timeout
    A->>A: Retry (attempt 2)
    A->>D: Query
    D-->>A: Success
    A-->>C: 201 Created
    
    Note over A,M: If all retries fail
    
    C->>A: POST /resource
    A->>D: Query
    D--xA: Connection timeout
    A->>A: Retry (attempt 2)
    D--xA: Connection timeout
    A->>A: Retry (attempt 3)
    D--xA: Connection timeout
    A->>M: Log error
    A-->>C: 503 Service Unavailable
```

---

## Data Flow Diagrams

### Basic Data Flow

```mermaid
flowchart LR
    subgraph Input
        UI[Web UI]
        API_In[API Request]
    end
    
    subgraph Processing
        Validate[Validation]
        Transform[Transform]
        Business[Business Logic]
    end
    
    subgraph Storage
        DB[(PostgreSQL)]
        Cache[(Redis)]
    end
    
    UI -->|User data| Validate
    API_In -->|JSON| Validate
    Validate -->|Clean data| Transform
    Transform -->|Normalized| Business
    Business -->|Persist| DB
    Business -->|Cache| Cache
```

### ETL Pipeline

```mermaid
flowchart LR
    subgraph Sources
        ProdDB[(Production DB)]
        Logs[Application Logs]
        Events[Event Stream]
    end
    
    subgraph Extract
        DBExtract[DB Extractor]
        LogExtract[Log Parser]
        EventExtract[Event Consumer]
    end
    
    subgraph Transform
        Clean[Data Cleaning]
        Enrich[Enrichment]
        Aggregate[Aggregation]
    end
    
    subgraph Load
        DW[(Data Warehouse)]
        Analytics[Analytics DB]
    end
    
    ProdDB --> DBExtract
    Logs --> LogExtract
    Events --> EventExtract
    
    DBExtract --> Clean
    LogExtract --> Clean
    EventExtract --> Clean
    
    Clean --> Enrich
    Enrich --> Aggregate
    
    Aggregate --> DW
    Aggregate --> Analytics
```

### Real-time Data Flow

```mermaid
flowchart LR
    subgraph Ingestion
        Producer1[Service A]
        Producer2[Service B]
    end
    
    subgraph Streaming
        Kafka[Message Broker]
    end
    
    subgraph Processing
        StreamProc[Stream Processor]
    end
    
    subgraph Consumers
        RealTime[Real-time Dashboard]
        Batch[Batch Analytics]
        Alert[Alerting]
    end
    
    Producer1 -->|Events| Kafka
    Producer2 -->|Events| Kafka
    Kafka --> StreamProc
    StreamProc -->|Processed| RealTime
    Kafka -->|Raw| Batch
    StreamProc -->|Anomalies| Alert
```

---

## Entity Relationship Diagrams

### Basic ERD

```mermaid
erDiagram
    USER ||--o{ PROJECT : owns
    USER ||--o{ TEAM_MEMBER : "is member"
    TEAM ||--o{ TEAM_MEMBER : has
    TEAM ||--o{ PROJECT : owns
    PROJECT ||--o{ TASK : contains
    USER ||--o{ TASK : assigned
    
    USER {
        uuid id PK
        string email UK
        string name
        timestamp created_at
    }
    
    TEAM {
        uuid id PK
        string name
        uuid owner_id FK
    }
    
    PROJECT {
        uuid id PK
        string name
        uuid owner_id FK
        uuid team_id FK
        enum status
    }
    
    TASK {
        uuid id PK
        string title
        uuid project_id FK
        uuid assignee_id FK
        enum status
    }
    
    TEAM_MEMBER {
        uuid id PK
        uuid team_id FK
        uuid user_id FK
        enum role
    }
```

---

## State Diagrams

### Order Status Flow

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Pending: Submit
    Pending --> Processing: Payment received
    Pending --> Cancelled: Cancel
    Processing --> Shipped: Ship
    Processing --> Cancelled: Cancel
    Shipped --> Delivered: Confirm delivery
    Shipped --> Returned: Return requested
    Delivered --> [*]
    Returned --> Refunded: Process refund
    Refunded --> [*]
    Cancelled --> [*]
```

### User Account States

```mermaid
stateDiagram-v2
    [*] --> Pending: Register
    Pending --> Active: Verify email
    Pending --> [*]: Expire (72h)
    Active --> Suspended: Admin action
    Active --> Deactivated: User request
    Suspended --> Active: Admin action
    Deactivated --> Active: Reactivate
    Deactivated --> Deleted: 30 days
    Deleted --> [*]
```

---

## Deployment Diagrams

### Cloud Architecture

```mermaid
graph TB
    subgraph Internet
        Users[Users]
        CDN[CloudFlare CDN]
    end
    
    subgraph Cloud [AWS/Railway]
        subgraph Public
            LB[Load Balancer]
            WebServers[Web Servers x2]
        end
        
        subgraph Private
            APIServers[API Servers x3]
            Workers[Workers x2]
        end
        
        subgraph Data
            PrimaryDB[(Primary DB)]
            ReplicaDB[(Replica DB)]
            Redis[(Redis Cluster)]
        end
    end
    
    Users --> CDN
    CDN --> LB
    LB --> WebServers
    WebServers --> APIServers
    APIServers --> PrimaryDB
    APIServers --> Redis
    PrimaryDB --> ReplicaDB
    Workers --> PrimaryDB
    Workers --> Redis
```

---

## Tips for Good Diagrams

### Do
- Use consistent shapes for same types (databases always cylinders)
- Label connections with what flows through them
- Group related items in subgraphs
- Keep diagrams focused - one concept per diagram
- Use colors sparingly and meaningfully

### Don't
- Cram everything into one diagram
- Use too many crossing lines
- Omit labels on arrows
- Mix abstraction levels
- Include implementation details in high-level diagrams

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Services | PascalCase | UserService, PaymentAPI |
| Databases | Name + type | PostgreSQL, Redis Cache |
| Queues | Name + purpose | OrderQueue, EmailQueue |
| External | Provider name | Stripe, SendGrid |
