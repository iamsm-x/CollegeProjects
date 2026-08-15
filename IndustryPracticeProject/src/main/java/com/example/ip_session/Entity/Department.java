package com.example.ip_session.Entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.*;

import java.util.List;

@Entity
@Table(name = "departments")
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor

public class Department {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 50)
    private String name;

//    @OneToMany(mappedBy = "department" , cascade = CascadeType.ALL)
//    @JsonIgnore
//    private List<Employee> employees;


}