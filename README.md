# $Trade

Welcome to $Trade, an innovative trading platform specifically designed for investors who want to efficiently and effectively manage their trading strategies. The use of cutting-edge technologies ensures an optimal user experience and the implementation of comprehensive trading operations.

## Project Overview

$Trade combines advanced frontend and backend technologies in a Docker-based setup to ensure scalability and easy maintainability. Our platform is aimed at supporting both amateur investors and experienced traders with essential tools needed for successful trading decisions.

### Architecture

The project is divided into two main areas: the frontend, which is responsible for user interaction, and the backend, which handles data processing and API management.

#### Frontend

Our frontend is a single-page application (SPA), developed with React, and uses a variety of JavaScript libraries to provide a smooth and interactive user experience.

##### Technology Stack:

- **ApexCharts & React-ApexCharts**: Used for creating dynamic and interactive charts.
- **Axios**: A promise-based HTTP client for making HTTP requests in JavaScript.
- **React Icons**: Provides popular icons as React components, making it easy to include them in your project.
- **React Router DOM**: A package for implementing dynamic routing in a React application.
- **Chart.js & React-Chartjs-2**: Used for creating beautiful charts and graphs.
- **Chartjs Adapter Date-FNS**: Provides date adapter functions for Chart.js to support date-based data.

##### Docker Compose Configuration:

```yaml
frontend:
  build:
    context: ./Frontend/strade
    dockerfile: Dockerfile
  ports:
    - "3000:3000"
  volumes:
    - ./Frontend/strade:/app
    - /app/node_modules
  environment:
    - NODE_ENV=development
```

#### Backend

The backend of the $Trade project relies on several key Python packages to function effectively.

##### Technology Stack:

- **FastAPI**: Provides a robust, fast API framework for high-performance requirements.
- **Uvicorn**: A powerful ASGI server that enables asynchronous running of Python code.
- **SQLAlchemy**: Serves as an ORM tool to abstract database operations.
- **Pydantic**: Strengthens data integrity through strict typing and validation.
- **bcrypt**: Used for hashing passwords for secure storage.
- **Python-Jose**: Generates and verifies JWT tokens.
- **email-validator**: Validates email addresses to ensure proper formatting.
- **paypalrestsdk**: Integrates PayPal payment processing.
- **ccxt**: A cryptocurrency trading library with support for many exchanges.
- **python-dotenv**: Loads environment variables from a .env file for configuration.

##### Docker Compose Configuration:

```yaml
backend:
  build:
    context: ./Backend/Server
    dockerfile: Dockerfile
  ports:
    - "8001:8001"
  volumes:
    - ./Backend/Server:/app
  environment:
    - PYTHONUNBUFFERED=1
```

## Quick Start

Follow these steps to start the project on your local machine:

1. Ensure that Docker and Docker Compose are installed on your system.
2. Open a terminal and navigate to the root directory of the project.
3. Execute the command `docker-compose up --build` to build and launch the containers.

## Development

Want to contribute to development? Great! $Trade welcomes new contributors. Fork the repository and send your pull requests. You can also report issues in the GitHub repository if you discover problems or have suggestions for improvement.

## Contact

- Simon Fedrau - [GitHub](https://github.com/SimBezzo)
- Philipp Deimel - [GitHub](https://github.com/PDeimel)
- Wael Eskeif - [GitHub](https://github.com/weski17)
- Anna Heim - [GitHub](https://github.com/AnnaSabr)

## Additional Links

- [Project Repository](https://github.com/Business-Makers/Produkt)
