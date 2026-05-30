# Care Your Health Hospital

## Cloud-Based Healthcare Management System Using DevSecOps Practices

### Project Overview

Care Your Health Hospital is a cloud-hosted healthcare management system developed as a complete DevSecOps project. The application enables patients to access hospital services digitally while providing administrators with a centralized platform to manage doctors, appointments, patient visits, healthcare campaigns, and hospital communications.

The project demonstrates the practical implementation of modern cloud computing, web development, DevOps automation, security controls, containerization, continuous integration and continuous deployment practices using Amazon Web Services and open-source technologies.

The application was developed using Flask and deployed on AWS infrastructure with Docker containerization, Jenkins automation, Amazon RDS database integration, Amazon S3 media storage, NGINX reverse proxy configuration, CloudWatch monitoring, and GitHub-based source code management.

---

# Project Objectives

The primary objectives of this project are:

1. Develop a secure healthcare management platform.
2. Implement role-based access control for users and administrators.
3. Store healthcare data securely in a cloud database.
4. Deploy the application on AWS cloud infrastructure.
5. Implement DevSecOps principles throughout the deployment lifecycle.
6. Automate deployment using Jenkins CI/CD pipelines.
7. Store media files using cloud storage services.
8. Monitor infrastructure and application health.
9. Demonstrate cloud security best practices.
10. Create a production-ready healthcare application architecture.

---

# Problem Statement

Traditional healthcare appointment systems often rely on manual processes that create delays, increase administrative workload, and limit patient accessibility. Hospitals require a centralized digital platform that allows patients to book appointments, access doctor information, receive appointment confirmations, and stay informed about healthcare campaigns while enabling administrators to efficiently manage hospital operations.

This project addresses these challenges by providing a cloud-based healthcare management platform that is secure, scalable, automated, and accessible through a web interface.

---

# System Features

## Patient Features

The patient module provides the following capabilities:

### User Registration

Patients can create personal accounts using their email address and password. Passwords are securely hashed before being stored in the database.

### User Authentication

Registered users can securely log in and access protected healthcare services.

### Doctor Directory

Patients can browse doctors categorized by department and specialization.

### Doctor Profile View

Patients can view:

* Doctor name
* Department
* Qualification
* Experience
* Specialization
* Successful surgeries
* Achievements

### Appointment Booking

Patients can:

* Select a doctor
* Choose appointment date
* Select appointment time
* Provide health concerns

### Appointment Management

Patients can:

* View appointment history
* Read appointment confirmation letters
* Download appointment letters

### Healthcare Campaigns

Patients can view:

* Free medical camps
* Awareness programs
* Community health initiatives

### Contact System

Patients can submit inquiries directly to the hospital administration.

---

## Administrator Features

The administrator module includes:

### Doctor Management

Administrators can:

* Add new doctors
* Upload doctor profile images
* Update doctor details
* Organize doctors by department

### Campaign Management

Administrators can:

* Create health campaigns
* Publish awareness programs
* Update campaign schedules

### Recent Patient Records

Administrators can:

* Record recent patient visits
* Track diagnoses
* Maintain visit information

### Appointment Monitoring

Administrators can monitor all appointments booked through the system.

### Dashboard Analytics

The administrator dashboard provides an overview of:

* Total doctors
* Total appointments
* Total campaigns
* Total patient visits

---

# Development Environment

The application was developed using the following technologies:

Backend Framework:
Flask

Programming Language:
Python

Frontend Technologies:
HTML
CSS
Bootstrap

Authentication:
Flask Login

Password Security:
Flask Bcrypt

Database ORM:
SQLAlchemy

Database Driver:
PyMySQL

Media Storage:
Amazon S3

Database:
Amazon RDS MySQL

Containerization:
Docker

Web Server:
Gunicorn

Reverse Proxy:
NGINX

Source Control:
Git

Repository Hosting:
GitHub

CI/CD Platform:
Jenkins

Monitoring:
Amazon CloudWatch

Cloud Platform:
Amazon Web Services

Domain:
DuckDNS

---

# AWS Infrastructure Implementation

## Amazon EC2

An EC2 Ubuntu instance was launched to host the application.

The EC2 instance serves as:

* Application server
* Docker host
* Jenkins server
* NGINX server

### Activities Performed

1. Created AWS account resources.
2. Launched Ubuntu EC2 instance.
3. Configured key pair.
4. Configured security groups.
5. Connected through SSH.
6. Installed required software packages.
7. Increased EBS storage volume.
8. Configured firewall rules.

---

## Amazon RDS

Amazon RDS MySQL was used as the primary database service.

### Activities Performed

1. Created MySQL RDS instance.
2. Configured database credentials.
3. Created database schema.
4. Connected Flask application.
5. Created application tables using SQLAlchemy.

### Benefits

* Managed database service
* Automated backups
* Improved availability
* Better security
* Reduced maintenance effort

---

## Amazon S3

Amazon S3 was integrated for media storage.

### Activities Performed

1. Created S3 bucket.
2. Configured permissions.
3. Implemented boto3 integration.
4. Uploaded doctor profile images.
5. Verified object storage functionality.

### Benefits

* Durable storage
* High availability
* Scalability
* Cost efficiency

---

# Security Implementation

## Password Hashing

Passwords are hashed using bcrypt before storage.

Benefits:

* Prevents plaintext password storage.
* Protects user credentials during breaches.

---

## SQL Injection Protection

SQLAlchemy ORM was used to eliminate direct SQL query execution.

Benefits:

* Prevents SQL injection attacks.
* Provides safer database interactions.

---

## Role-Based Access Control

Two user roles were implemented:

Patient
Administrator

Benefits:

* Restricts administrative functions.
* Protects sensitive operations.

---

## Environment Variable Protection

Sensitive values were moved into .env files.

Protected values include:

* Database credentials
* AWS credentials
* Secret keys

Benefits:

* Prevents credential exposure.
* Improves deployment security.

---

## Docker Isolation

The application runs inside Docker containers.

Benefits:

* Process isolation
* Consistent deployments
* Easier scaling

---

# Docker Implementation

Docker was implemented to package the entire application and its dependencies into a portable container.

Activities performed:

1. Created Dockerfile.
2. Installed dependencies.
3. Configured Gunicorn.
4. Built Docker image.
5. Created Docker container.
6. Verified container functionality.

Benefits:

* Consistent environments.
* Faster deployments.
* Simplified maintenance.

---

# NGINX Reverse Proxy Configuration

NGINX was configured to:

* Accept requests on port 80.
* Forward requests to Flask application on port 8000.
* Improve application accessibility.

Benefits:

* Cleaner URLs.
* Better security.
* Improved performance.

---

# Domain Configuration Using DuckDNS

A free domain was configured.

Domain:

careyourhealth.duckdns.org

Activities performed:

1. Created DuckDNS subdomain.
2. Mapped EC2 public IP.
3. Verified DNS resolution.
4. Connected domain to NGINX.

Benefits:

* User-friendly URL.
* Easier access than raw IP addresses.

---

# Jenkins CI/CD Pipeline

Jenkins was implemented for deployment automation.

Pipeline stages:

Source Code Checkout

↓

Docker Build

↓

Stop Previous Container

↓

Remove Previous Container

↓

Deploy New Container

Activities performed:

1. Installed Jenkins.
2. Configured Java runtime.
3. Installed plugins.
4. Connected GitHub repository.
5. Added credentials.
6. Created pipeline.
7. Configured deployment automation.
8. Tested successful deployments.

Benefits:

* Faster releases.
* Reduced human error.
* Automated deployments.

---

# Monitoring and Logging

Amazon CloudWatch was used for monitoring.

Monitored metrics include:

* CPU utilization
* Memory utilization
* Disk usage
* Application logs

Benefits:

* Improved visibility.
* Early issue detection.
* Better system reliability.

---

# Backup Strategy

Database backups are automated.

Activities performed:

1. Created backup script.
2. Generated database dumps.
3. Uploaded backups to S3.
4. Configured scheduled execution.

Benefits:

* Disaster recovery.
* Data protection.
* Business continuity.

---

# Project Outcomes

The project successfully demonstrated:

* Full-stack web application development.
* Cloud-native deployment.
* Secure database integration.
* DevSecOps implementation.
* CI/CD automation.
* Infrastructure monitoring.
* Cloud storage integration.
* Production deployment practices.

---

# Future Enhancements

Potential improvements include:

* HTTPS with ACM and Load Balancer.
* Multi-factor authentication.
* Email notifications.
* SMS appointment reminders.
* AI-powered healthcare chatbot.
* Kubernetes orchestration.
* Terraform infrastructure automation.
* Mobile application integration.

---

# Author

Abhinav Aji

Cloud DevSecOps Healthcare Management System

Academic Project Submission

2026
