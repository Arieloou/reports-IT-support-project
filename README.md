# reports-IT-support-project
This project is about an application to improve the process of create reports related to device delivery, exchange or devolution. The application includes a configuration that consider the name of the technician who prepares the report and the name of the headquarters to which it belongs.

## Table of Contents
1.  [Introduction](#introduction)
2.  [The Problem to Solve](#the-problem-to-solve)
3.  [Architectural Features](#architectural-features)
4.  [System Architecture](#system-architecture)
    -   [Microservices](#microservices)
    -   [Technology Stack](#technology-stack)
5.  [Getting Started](#getting-started)
    -   [Prerequisites](#prerequisites)
    -   [Running the Application](#running-the-application)
6.  [Architecture Diagrams](#architecture-diagrams)
7.  [Source Code Repository](#source-code-repository)
8.  [Authors](#authors)

## Introduction

## The Problem to Solve

## Architectural Features
```
reports-IT-support-project/
├── src/
│ ├── config/ # Application configuration
│ ├── data/ # Data layer (handled by Gemini Knowledge API)
│ ├── services/ # AI and processing services
│ │ ├── gemini_service.py # Interface with Gemini AI
│ │ └── knowledge_api.py # Interface with Knowledge Base API
│ ├── ui/ # User Interface (Flet)
│ │ ├── app.py # Main app component
│ │ └── components/ # Reusable components
│ └── main.py # Application entry point
├── tests/ # Unit tests
└── requirements.txt # Project dependencies
```
## System Architecture

### Layers

### Technology Stack
-   **Backend:** 
-   **Database:** 
-   **Security:** 

## Getting Started
Follow these steps to run the development environment locally.

### Prerequisites

### Running the Application
1.  Clone the repository to your local machine:
    ```bash
    git clone https://github.com/Arieloou/reports-IT-support-project.git
    cd SPSM
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    # source .venv/bin/activate  # Linux/Mac
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

Once the script finishes, the entire platform will be running and ready to use.

## Authors
This project was developed by:
-   **Carlos Tapia:** Backend Developer
-   **Ariel Anchapaxi:** UI/UX Designer and Technical Writer and Backend Developer and Software Architect
