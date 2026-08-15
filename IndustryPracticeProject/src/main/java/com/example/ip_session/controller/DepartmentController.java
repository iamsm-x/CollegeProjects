package com.example.ip_session.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.example.ip_session.Entity.Department;
import com.example.ip_session.repo.DepartmentRepo;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/department")
public class DepartmentController {
    @Autowired
    private  DepartmentRepo departmentRepo;

    @PostMapping
    public ResponseEntity<Department> createDepartment(@RequestBody Department department) {

        Department savedDepartment = departmentRepo.save(department);

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(savedDepartment);
    }

    // Get All Departments
    @GetMapping
    public ResponseEntity<List<Department>> getAllDepartments() {

        return ResponseEntity.ok(departmentRepo.findAll());
    }

    // Get Department By Id
    @GetMapping("/{id}")
    public ResponseEntity<Department> getDepartmentById(@PathVariable Long id) {

        return departmentRepo.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // Update Department
    @PutMapping("/{id}")
    public ResponseEntity<Department> updateDepartment(
            @PathVariable Long id,
            @RequestBody Department updatedDepartment) {

        Department department = departmentRepo.findById(id).orElse(null);

        if (department == null) {
            return ResponseEntity.notFound().build();
        }

        department.setName(updatedDepartment.getName());

        return ResponseEntity.ok(departmentRepo.save(department));
    }

    // Patch Department
    @PatchMapping("/{id}")
    public ResponseEntity<Department> patchDepartment(
            @PathVariable Long id,
            @RequestBody Department updatedDepartment) {

        Department department = departmentRepo.findById(id).orElse(null);

        if (department == null) {
            return ResponseEntity.notFound().build();
        }

        if (updatedDepartment.getName() != null) {
            department.setName(updatedDepartment.getName());
        }

        return ResponseEntity.ok(departmentRepo.save(department));
    }

    // Delete Department
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteDepartment(@PathVariable Long id) {

        if (!departmentRepo.existsById(id)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("Department not found");
        }

        departmentRepo.deleteById(id);

        return ResponseEntity.ok("Department deleted successfully");
    }
}


