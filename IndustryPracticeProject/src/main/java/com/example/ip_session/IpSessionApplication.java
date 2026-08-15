package com.example.ip_session;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@OpenAPIDefinition(
        info = @Info(
                title = "IP Session API",
                version = "1.0",
                description = "Learning Spring Boot APIs"
        )
)
public class IpSessionApplication {

	public static void main(String[] args) {
		SpringApplication.run(IpSessionApplication.class, args);
	}

}
