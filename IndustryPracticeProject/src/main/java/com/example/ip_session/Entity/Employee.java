package com.example.ip_session.Entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import lombok.*;

@Entity
@Table(name = "employee")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Builder

public class Employee extends Audit {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String firstName;

    @Column(nullable = false)
    private String lastName;

    @Column(unique = true, nullable = false)
    private String email;


    @DecimalMin("10000")
    @DecimalMax("1000000")
    private Double salary;

//    @ManyToOne
//    @JoinColumn(name = "dept_id")
//    private Department department;
}
