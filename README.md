# Tool Service API – Combined FastAPI and ASP.NET WebAPI MCP Project

This repository contains a unified project with **two independent MCP (Model Context Protocol) servers** – one built in **FastAPI (Python)** and the other in **ASP.NET WebAPI (C#/.NET)** – exposing tools via reflective discovery and dynamic execution. Additionally, a FastAPI client service is provided to interact with these MCP servers using OpenAI Agent SDK for **FastAPI (Python) server**.

---

## 📦 Repository Structure

```
tool-service-api/
│
├── fastapi_service/
│   ├── mcp_project/              # Prototype MCP server with static and dynamic loaders
│   ├── office_mcp/               # Main FastAPI MCP server with 13 property tools
│   ├── office_mcp_client/        # FastAPI client using OpenAI Agent SDK (runs on port 9000)
│
├── dotnet_service/
│   ├── MyDotNetApi/              # Prototype .NET client (not functional under development)
│   ├── office_mcp_dotnet/        # Main .NET MCP server with same 13 property tools
```

---

## 🚀 FastAPI MCP Server (`office_mcp`)

- **URL (SSE Transport) (Default run)**: `http://127.0.0.1:8000/sse`
- **URL (HTTP Transport) (not default)**: `http://127.0.0.1:8000/mcp`
- **Tools**: 13 tools that retrieve property info using parameters:
  - `objectType`
  - `objectId`
  - `QueryText`
- **Defaults**: If no parameters provided, defaults to Walnut property query.
- **Tool Execution**: Tools are dynamically discovered and executed via decorators.
- **Extra**: `request.py` can be used to test raw JSON queries locally.

### 🧠 Features of (`/mcp_project`) folder server

- Static loader (MathTool, StringTool)
- Dynamic loader (fetch tools from local MySQL database)
- **Default MCP URL**: `http://localhost:8000/sse` 

### ✅ Setup & Running intended mcp server (Python)

-- Install **uv** and set up our Python project and environment if not already installed :

```bash
# For windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# For macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# From repo root
cd fastapi_service/office_mcp

# Install dependencies
uv add mcp[cli] httpx uvicorn requests

# Run the MCP server
uv run python server.py
```

---

## 🧠 FastAPI Client (`office_mcp_client`)

- **Client running port**: `9000`
- **Base MCP URL**: `http://localhost:8000/sse`

### 🔌 Endpoints

- `POST /ask_bot`: Use OpenAI Agent SDK to answer user query using tools on SSE MCP server
- `GET /bot_capabilities`: Lists available tools on SSE MCP server
- `POST /bot_response`: Runs tools present on SSE MCP server

### ✅ Setup & Running mcp client (Python)

```bash
# From repo root
cd fastapi_service/office_mcp_client

# Install dependencies
uv add mcp[cli] httpx uvicorn openai-agents anyio click

# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-key"

# Run the FastAPI client
uvicorn main:app --reload --port 9000
```

---

## 🧠 If running test on Postman (For python server)

- Connect to http on port : `http://127.0.0.1:8000/sse`
- Select tool and run directly for running with default parameter or provide specific parameter to the tool.

## ⚙️ .NET MCP Server (`office_mcp_dotnet`)

- **URL (HTTP Transport)**: `http://localhost:3001`
- **Tools**: Same 13 tools as FastAPI version with same input/output behavior

### ✅ Setup & Run

```bash
# From repo root
cd dotnet_service/office_mcp_dotnet

# Restore and build
dotnet restore
dotnet build

# Add required packages (one-time setup)
dotnet add package ModelContextProtocol --prerelease
# OR fallback
dotnet add package ModelContextProtocol --version 0.2.0-preview.1

# Add OpenTelemetry & Hosting packages
dotnet add package Microsoft.Extensions.Hosting
dotnet add package OpenTelemetry.Instrumentation.AspNetCore
dotnet add package OpenTelemetry.Instrumentation.Http
dotnet add package ModelContextProtocol.AspNetCore
dotnet add package OpenTelemetry.Exporter.OpenTelemetryProtocol

# Run the MCP server
dotnet run
```

---

## 🧠 If running test on Postman (For dotnet server)

- Connect to http on port : `http://localhost:3001`
- Select tool and run directly for running with default parameter or provide specific parameter to the tool.

---

## 🚫 .NET Client (`MyDotNetApi`)

> This project is currently not complete or functional. You can ignore the `MyDotNetApi` folder.

---

## 📋 Summary of Ports

| Component          | Port | Description                                 |
| ------------------ | ---- | ------------------------------------------- |
| FastAPI MCP Server | 8000 | SSE (`/sse`) & HTTP (`/mcp`) endpoints      |
| FastAPI Client     | 9000 | Uses OpenAI Agent SDK to talk to SSE server |
| .NET MCP Server    | 3001 | HTTP-based .NET implementation of MCP       |
| .NET Client        | N/A  | Not implemented                             |

---

## 🧰 Dependencies Overview

### FastAPI

- `pydantic`
- `fastapi`
- `uvicorn`
- `httpx`
- `requests`
- `openai-agents` (for client only)

### .NET

- `ModelContextProtocol` (pre-release)
- `OpenTelemetry.Instrumentation.AspNetCore`
- `OpenTelemetry.Instrumentation.Http`
- `ModelContextProtocol.AspNetCore`
- `OpenTelemetry.Exporter.OpenTelemetryProtocol`
- `Microsoft.Extensions.Hosting`

---

## 🤖 Use Cases

- Dynamically discover tools (from code or DB)
- Reflective execution of tools (Python decorators / .NET attributes)
- AI-based tool orchestration using OpenAI Assistant SDK
- Cross-platform parity: FastAPI & ASP.NET WebAPI

---

## 🛠️ Author & License

> Developed by [@ysidm2025](https://github.com/ysidm2025)  
> Licensed under MIT – Feel free to use and extend!
