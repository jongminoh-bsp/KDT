package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class TestApp {
    public static void main(String[] args) {
        SpringApplication.run(TestApp.class, args);
    }
}

@RestController
class TestController {
    @GetMapping("/")
    public String hello() {
        return "Hello from Test Skyline App!";
    }
    
    @GetMapping("/health")
    public String health() {
        return "OK";
    }
}
