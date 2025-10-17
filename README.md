# Multi_Database_MCP_Client
A modular MCP client project connected to multiple SQL database servers (MySQL, PostgreSQL, etc.) with seamless database switching and query execution.


## Overview

This project implements an **MCP (Model Context Protocol) Client** that connects to multiple servers—**Filesystem, Custom Tools, MySQL, and PostgreSQL**—to execute certain tasks programmatically. The setup enables **dynamic database switching, query execution,** and **communication** through the MCP protocol. It enables seamless interaction with databases and file systems using a unified **tool-based architecture**. It is built to showcase **scalable back-end interaction** using **client-server architecture**. The setup is modular, extensible, and ideal for automation, backend logic, or intelligent agent workflows.


## Key Features

### Database Operations

**MySQL Integration** – Complete database management including listing databases, executing queries, and schema extraction.

**PostgreSQL Support** – Full PostgreSQL connectivity with query execution, transaction handling, and schema analysis.

**Multi-Database Queries** – Execute operations seamlessly across MySQL and PostgreSQL.

**Schema Extraction** – Comprehensive database structure analysis and documentation.

### File System Management

**File Operations** – Read, write, edit, move, and delete files programmatically.

**Directory Management** – Create directories, list contents with sizes, and generate directory trees.

**Advanced Search** – Search files by content and retrieve detailed file information.

**Media Support** – Handle text files, media files, and multi-file operations.

### Document Processing

**Word Document Tools** – Create, read, and edit DOCX files with structured content.

**Document Metadata** – Extract detailed metadata from various document types.

**File Management** – Delete, organize, and maintain document files programmatically.

**Custom Formatting** – Support headings, paragraphs, lists, and complex document structures.

### System Integration

**MCP Protocol** – Standardized communication across all server components.

**LangChain Integration** – Ready for AI agent interactions and workflow automation.

**Modular Architecture** – Four specialized servers (25 total tools) working in harmony.

**Unified Client** – Single interface to access all functionality through a conversational AI.

**Configuration Management** – JSON-based server configuration for flexible deployment.

### AI-Powered Workflows

**Conversational Interface** – Natural language interaction with all system components.

**Context Awareness** – Maintains conversation history across database and file operations.

**Intelligent Routing** – Automatically selects appropriate tools based on user requests.

**Multi-Modal Operations** – Combine database queries, file operations, and document processing in a single workflow.


## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Programming Language** | Python 3.8+ |
| **Protocol** | Model Context Protocol (MCP) |
| **Databases** | MySQL 8.0+, PostgreSQL 12+ |
| **Async Framework** | asyncio, aiomysql, aiopg |
| **AI Integration** | LangChain, Google Gemini API |
| **Document Processing** | python-docx |
| **Key Dependencies** | FastMCP, psycopg2, pymysql, loguru |


