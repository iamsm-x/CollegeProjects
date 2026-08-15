<div align="center">

# 🏢 IP Session — Employee Management API

**A Spring Boot REST API for managing employees, departments, and users**

Built with Spring Boot 4.1, Spring Data JPA, PostgreSQL, and documented with Swagger/OpenAPI.

</div>

---

## ✨ Features

- 👤 **Employee CRUD** — create, read, update, partially update, and delete employees
- 🏬 **Department CRUD** — create, read, update, partially update, and delete departments
- 🔐 **User entity** — basic user model with username/password fields
- 🕒 **Audit tracking** — `createdBy`, `modifiedBy`, `createdAt`, `updatedAt` recorded automatically for employees
- ✅ **Validation** — employee salary constrained between 10,000 and 1,000,000
- 📜 **Structured logging** — console + rotating file log (`logs/application.log`)
- 📖 **Auto-generated API docs** — interactive Swagger UI via springdoc-openapi

---

## 📁 Project Structure

```
IndustryPracticeProject/
├── src/
│   ├── main/
│   │   ├── java/com/example/ip_session/
│   │   │   ├── IpSessionApplication.java     # Spring Boot entry point
│   │   │   ├── Entity/
│   │   │   │   ├── Audit.java                # Shared audit fields (@MappedSuperclass)
│   │   │   │   ├── Employee.java             # Employee entity (extends Audit)
│   │   │   │   ├── Department.java           # Department entity
│   │   │   │   └── User.java                 # User entity
│   │   │   ├── controller/
│   │   │   │   ├── EmployeeController.java   # /employees REST endpoints
│   │   │   │   └── DepartmentController.java # /department REST endpoints
│   │   │   └── repo/
│   │   │       ├── EmployeeRepo.java         # Spring Data JPA repository
│   │   │       ├── DepartmentRepo.java
│   │   │       └── UserRepo.java
│   │   └── resources/
│   │       └── application.yaml              # DB connection & logging config
│   └── test/
│       └── java/com/example/ip_session/
│           └── IpSessionApplicationTests.java
├── pom.xml
├── mvnw / mvnw.cmd
└── logs/application.log
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Language | Java 21 |
| Framework | Spring Boot 4.1.0 |
| Persistence | Spring Data JPA (Hibernate) |
| Database | PostgreSQL |
| Boilerplate reduction | Lombok |
| API documentation | springdoc-openapi (Swagger UI) |
| Build tool | Maven (with wrapper) |
| Testing | Spring Boot Test |

---

## 🚀 Getting Started

### Prerequisites
- **Java 21** or newer
- **PostgreSQL** running locally (or update the connection details below)
- Maven is not required to be installed separately — this project ships with the Maven Wrapper (`mvnw` / `mvnw.cmd`)

### 1. Create the database
```sql
CREATE DATABASE "ipSession";
```

### 2. Configure the connection
Database credentials are set in `src/main/resources/application.yaml`:
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/ipSession
    username: soham
    password: soham11
```
Update the `username` / `password` to match your local PostgreSQL setup. Tables are created and updated automatically on startup (`ddl-auto: update`).

### 3. Run the application
```bash
./mvnw spring-boot:run
```
On Windows:
```bash
mvnw.cmd spring-boot:run
```

The API starts on:
```
http://localhost:8080
```

### 4. Explore the API docs (Swagger UI)
```
http://localhost:8080/swagger-ui.html
```

---

## 🌐 API Reference

### Employees — `/employees`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/employees` | Create a new employee |
| `GET` | `/employees` | List all employees |
| `GET` | `/employees/{id}` | Get an employee by ID |
| `PUT` | `/employees/{id}` | Fully update an employee |
| `PATCH` | `/employees/{id}` | Partially update an employee (any subset of fields) |
| `DELETE` | `/employees/{id}` | Delete an employee |

**Employee fields:** `firstName`, `lastName`, `email` (unique), `salary` (10,000–1,000,000)

**Example — create an employee**
```bash
curl -X POST http://localhost:8080/employees \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "jane.doe@example.com",
    "salary": 75000
  }'
```

### Departments — `/department`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/department` | Create a new department |
| `GET` | `/department` | List all departments |
| `GET` | `/department/{id}` | Get a department by ID |
| `PUT` | `/department/{id}` | Fully update a department |
| `PATCH` | `/department/{id}` | Partially update a department |
| `DELETE` | `/department/{id}` | Delete a department |

**Department fields:** `name` (unique)

**Example — create a department**
```bash
curl -X POST http://localhost:8080/department \
  -H "Content-Type: application/json" \
  -d '{ "name": "Engineering" }'
```

---

## 🗃️ Data Model

| Entity | Table | Key Fields |
|---|---|---|
| `Employee` | `employee` | `id`, `firstName`, `lastName`, `email`, `salary`, + audit fields |
| `Department` | `departments` | `id`, `name` |
| `User` | `users` | `id`, `username`, `password` |

`Employee` inherits `createdBy`, `modifiedBy`, `createdAt`, and `updatedAt` from the shared `Audit` base class.

> **Note:** the `Employee ↔ Department` relationship (`@ManyToOne` / `@OneToMany`) is present in the code but currently commented out.

---

## 🧪 Running Tests

```bash
./mvnw test
```

---

## 📄 Logging

Logs are written both to the console and to `logs/application.log`, using the pattern:
```
yyyy-MM-dd HH:mm:ss LEVEL logger - message
```

---

<div align="center">

Spring Boot practice project · Employee & Department Management API

</div>