package com.example.ip_session.repo;

import com.example.ip_session.Entity.Department;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Component;

@Component
public interface DepartmentRepo extends JpaRepository<Department,Long  > {

}
