# DevOps Task Manager

A Flask-based Task Manager application deployed on AWS EC2 using Docker and Docker Compose, with an automated CI/CD pipeline using Jenkins and GitHub Webhooks.

## Project Overview

DevOps Task Manager is a simple web application that allows users to add, complete, and delete tasks. The application demonstrates containerization, automated testing, continuous integration, and continuous deployment.

## Technologies Used

- **Cloud:** AWS EC2
- **Operating System:** Ubuntu Linux
- **Application:** Python, Flask
- **Database:** SQLite
- **Containerization:** Docker
- **Container Orchestration:** Docker Compose
- **Version Control:** Git, GitHub
- **CI/CD:** Jenkins
- **Testing:** Python Unit Testing

## Architecture

Developer → GitHub → GitHub Webhook → Jenkins Pipeline → Docker Build → Docker Compose → AWS EC2 → Flask Application

## CI/CD Pipeline

1. Developer pushes code changes to GitHub.
2. GitHub Webhook automatically triggers Jenkins.
3. Jenkins checks out the source code.
4. Automated unit tests are executed.
5. Docker image is built.
6. Docker Compose deploys the updated application on AWS EC2.

## Application Features

- Add new tasks
- View existing tasks
- Mark tasks as completed
- Delete tasks
- Health-check endpoint

## Deployment

The application runs inside a Docker container on an AWS EC2 Ubuntu instance.

**Application URL:** `http://YOUR-EC2-PUBLIC-IP:5000`

## Project Outcome

Successfully implemented an automated CI/CD workflow where pushing code to GitHub triggers Jenkins to test, build, and deploy the application automatically.
