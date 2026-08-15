package com.example.ip_session.controller;

import com.example.ip_session.Entity.Employee;
import com.example.ip_session.repo.EmployeeRepo;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


import java.lang.reflect.Field;
import java.util.List;
import java.util.Map;

@Tag(
        name = "Employee Controller",
        description = "Provides CRUD operations and search functionality for Employee Management."
)
@RestController
@RequestMapping("/employees")
public class EmployeeController {

    private static final Logger logger = LoggerFactory.getLogger(EmployeeController.class);

    @Autowired
    private final EmployeeRepo employeeRepo;

    public EmployeeController(EmployeeRepo employeeRepo) {
        this.employeeRepo = employeeRepo;
    }

    // Create Employee
    @Operation(
            summary = "Create Employee",
            description = "Creates a new employee and stores it in the database."
    )
    @ApiResponses({
            @ApiResponse(responseCode = "201", description = "Employee created successfully"),
            @ApiResponse(responseCode = "400", description = "Invalid employee details")
    })
    @PostMapping
    public ResponseEntity<Employee> createEmployee(@RequestBody Employee employee) {

        try {
            employee.setCreatedBy("admin");
            employee.setModifiedBy("admin");

            Employee savedEmployee = employeeRepo.save(employee);

            logger.info("Employee added successfully.");

            return ResponseEntity.status(HttpStatus.CREATED).body(savedEmployee);

        } catch (Exception e) {

            logger.error("Error while adding employee.", e);

            return ResponseEntity.internalServerError().build();
        }
    }

    // Get Employee by ID
    @Operation(
            summary = "Get Employee by ID",
            description = "Returns an employee for the given ID."
    )
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Employee found"),
            @ApiResponse(responseCode = "404", description = "Employee not found")
    })
    @GetMapping("/{id}")
    public ResponseEntity<Employee> getEmployee(
            @Parameter(description = "Employee ID", example = "1")
            @PathVariable Long id) {

        logger.info("Fetching employee with ID: {}", id);

        return employeeRepo.findById(id)
                .map(employee -> {
                    logger.info("Employee fetched successfully.");
                    return ResponseEntity.ok(employee);
                })
                .orElseGet(() -> {
                    logger.warn("Employee not found with ID: {}", id);
                    return ResponseEntity.notFound().build();
                });
    }

    // Get All Employees
    @Operation(
            summary = "Get All Employees",
            description = "Returns a list of all employees."
    )
    @ApiResponse(responseCode = "200", description = "Employees retrieved successfully")
    @GetMapping
    public ResponseEntity<List<Employee>> getAllEmployees() {

        logger.info("Fetching all employees.");

        return ResponseEntity.ok(employeeRepo.findAll());
    }

    // Update Employee
    @Operation(
            summary = "Update Employee",
            description = "Updates all employee details for the specified ID."
    )
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Employee updated successfully"),
            @ApiResponse(responseCode = "404", description = "Employee not found")
    })
    @PutMapping("/{id}")
    public ResponseEntity<Employee> updateEmployee(

            @Parameter(description = "Employee ID", example = "1")
            @PathVariable Long id,

            @RequestBody Employee updatedEmployee) {

        try {

            logger.info("Updating employee with ID: {}", id);

            Employee employee = employeeRepo.findById(id).orElse(null);

            if (employee == null) {
                logger.warn("Employee not found for update. ID: {}", id);
                return ResponseEntity.notFound().build();
            }

            employee.setFirstName(updatedEmployee.getFirstName());
            employee.setLastName(updatedEmployee.getLastName());
            employee.setEmail(updatedEmployee.getEmail());
//          employee.setDepartment(updatedEmployee.getDepartment());
            employee.setSalary(updatedEmployee.getSalary());

            logger.info("Employee updated successfully.");

            return ResponseEntity.ok(employeeRepo.save(employee));

        } catch (Exception e) {

            logger.error("Error while updating employee.", e);

            return ResponseEntity.internalServerError().build();
        }
    }

    // Partial Update
    @Operation(
            summary = "Partially Update Employee",
            description = "Updates only the fields provided in the request body."
    )
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Employee updated successfully"),
            @ApiResponse(responseCode = "400", description = "Invalid field supplied"),
            @ApiResponse(responseCode = "404", description = "Employee not found")
    })
    @PatchMapping("/{id}")
    public ResponseEntity<Employee> patchEmployee(

            @Parameter(description = "Employee ID", example = "1")
            @PathVariable Long id,

            @RequestBody Map<String, Object> updates) {

        logger.info("Partially updating employee with ID: {}", id);

        Employee employee = employeeRepo.findById(id).orElse(null);

        if (employee == null) {
            logger.warn("Employee not found for patch. ID: {}", id);
            return ResponseEntity.notFound().build();
        }

        for (Map.Entry<String, Object> entry : updates.entrySet()) {

            try {

                Field field = Employee.class.getDeclaredField(entry.getKey());

                field.setAccessible(true);

                field.set(employee, entry.getValue());

            } catch (NoSuchFieldException | IllegalAccessException e) {

                logger.error("Invalid field supplied for patch.", e);

                return ResponseEntity.badRequest().build();
            }
        }

        logger.info("Employee patched successfully.");

        return ResponseEntity.ok(employeeRepo.save(employee));
    }

    // Delete Employee
    @Operation(
            summary = "Delete Employee",
            description = "Deletes an employee using its ID."
    )
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Employee deleted successfully"),
            @ApiResponse(responseCode = "404", description = "Employee not found")
    })
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteEmployee(

            @Parameter(description = "Employee ID", example = "1")
            @PathVariable Long id) {

        logger.info("Deleting employee with ID: {}", id);

        try {

            if (!employeeRepo.existsById(id)) {

                logger.warn("Employee not found for deletion. ID: {}", id);

                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body("Employee not found");
            }

            employeeRepo.deleteById(id);

            logger.info("Employee deleted successfully.");

            return ResponseEntity.ok("Employee deleted successfully");

        } catch (Exception e) {

            logger.error("Error while deleting employee.", e);

            return ResponseEntity.internalServerError()
                    .body("Unable to delete employee");
        }
    }
}