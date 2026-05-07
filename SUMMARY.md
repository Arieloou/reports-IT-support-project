# Resumen Ejecutivo - reports-IT-support-project

This project is about an application to improve the process of create reports related to device delivery, exchange or devolution. The application includes a configuration that consider the name of the technician who prepares the report and the name of the headquarters to which it belongs.

## Table of Contents
1.  [Introduction](#introduction)
2.  [The Problem to Solve](#the-problem-to-solve)
3.  [Architectural Features](#architectural-features)
4.  [System Architecture](#system-architecture)
    -   [Layers](#layers)
    -   [Technology Stack](#technology-stack)
5.  [Getting Started](#getting-started)
    -   [Prerequisites](#prerequisites)
    -   [Running the Application](#running-the-application)
6.  [Authors](#authors)

## Introduction
Este proyecto consiste en una aplicación diseñada para optimizar y automatizar el proceso de generación de actas (reportes) relacionadas con la entrega, cambio o devolución de equipos y dispositivos. Facilita la labor de los técnicos al permitir configuraciones predeterminadas (como el nombre del técnico y la sede) y agilizar la creación de documentos en formatos estándar.

## The Problem to Solve
El problema principal que resuelve este proyecto es **mejorar los tiempos para el departamento de Soporte**. Anteriormente, la generación de actas de entrega, cambio o devolución consumía mucho tiempo debido a procesos manuales y repetitivos. Esta solución automatiza la recopilación de datos y la generación de los documentos correspondientes, permitiendo al equipo de soporte ser más eficiente y enfocar su tiempo en tareas de mayor impacto.

## Architectural Features
El proyecto cuenta con una arquitectura modular para facilitar el mantenimiento y la escalabilidad.

```text
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
La aplicación está estructurada en capas para separar las responsabilidades:
- **Capa de Presentación (UI):** Maneja la interfaz gráfica interactiva del usuario.
- **Capa de Servicios/Lógica de Negocio:** Encargada del procesamiento de datos y la generación de documentos.
- **Capa de Datos:** Se encarga de la lectura, escritura y almacenamiento de los registros.

### Technology Stack
-   **Frontend (UI):** Flet (Framework de Python).
-   **Backend:** Python (con librerías como `python-docx`, `docx2pdf` y `openpyxl`).
-   **Database:** Temporalmente la información se encuentra almacenada en un servidor privado de mi organización ____________________.
-   **Security:** (Se definirán e implementarán políticas de acuerdo a los requerimientos de la organización).

## Getting Started
Follow these steps to run the development environment locally.

### Prerequisites
- Python 3.8+
- Git

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
