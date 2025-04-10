# Combined FastAPI and ASP.NET WebAPI Project

## Overview
This project contains two independent services that expose the same functionality using FastAPI (Python) and ASP.NET WebAPI (C#/.NET). Both services allow you to interact with different tools that are dynamically loaded and executed via reflection.

## FastAPI Service
- **Port**: `8000`
- **Endpoints**:
  - `GET /bot_capabilities`: Returns metadata of available tools.
  - `POST /bot_response`: Executes a tool with parameters and returns the result.

## ASP.NET WebAPI Service
- **Port**: `5048`
- **Endpoints**:
  - `GET /bot_capabilities`: Returns metadata of available tools.
  - `POST /bot_response`: Executes a tool with parameters and returns the result.

## Running the Services

### FastAPI
1. Install dependencies:
   `pip install pydantic fastapi uvicorn`
