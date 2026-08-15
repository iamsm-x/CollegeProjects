package com.example.ip_session.repo;

import com.example.ip_session.Entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Component;

@Component
public interface UserRepo extends JpaRepository<User,Long> {

}
