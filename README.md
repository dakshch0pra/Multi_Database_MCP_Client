# Multi_Database_MCP_Client
A modular MCP client project connected to multiple SQL database servers (MySQL, PostgreSQL, etc.) with seamless database switching and query execution.


## Overview

This project implements an **MCP (Model Context Protocol) Client** that connects to multiple servers—**Filesystem, Custom Tools, MySQL, and PostgreSQL**—to execute certain tasks programmatically. The setup enables **dynamic database switching, query execution,** and **communication** through the MCP protocol. It enables seamless interaction with databases and file systems using a unified **tool-based architecture**. It is built to showcase **scalable back-end interaction** using **client-server architecture**. The setup is modular, extensible, and ideal for automation, backend logic, or intelligent agent workflows.


## Key Features

### Database Operations

- **MySQL Integration** – Complete database management including listing databases, executing queries, and schema extraction.
- **PostgreSQL Support** – Full PostgreSQL connectivity with query execution, transaction handling, and schema analysis.
- **Multi-Database Queries** – Execute operations seamlessly across MySQL and PostgreSQL.
- **Schema Extraction** – Comprehensive database structure analysis and documentation.

### File System Management

- **File Operations** – Read, write, edit, move, and delete files programmatically.
- **Directory Management** – Create directories, list contents with sizes, and generate directory trees.
- **Advanced Search** – Search files by content and retrieve detailed file information.
- **Media Support** – Handle text files, media files, and multi-file operations.

### Document Processing

- **Word Document Tools** – Create, read, and edit DOCX files with structured content.
- **Document Metadata** – Extract detailed metadata from various document types.
- **File Management** – Delete, organize, and maintain document files programmatically.
- **Custom Formatting** – Support headings, paragraphs, lists, and complex document structures.

### System Integration

- **MCP Protocol** – Standardized communication across all server components.
- **LangChain Integration** – Ready for AI agent interactions and workflow automation.
- **Modular Architecture** – Four specialized servers (25 total tools) working in harmony.
- **Unified Client** – Single interface to access all functionality through a conversational AI.
- **Configuration Management** – JSON-based server configuration for flexible deployment.

### AI-Powered Workflows

- **Conversational Interface** – Natural language interaction with all system components.
- **Context Awareness** – Maintains conversation history across database and file operations.
- **Intelligent Routing** – Automatically selects appropriate tools based on user requests.
- **Multi-Modal Operations** – Combine database queries, file operations, and document processing in a single workflow.


## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Programming Language** | Python 3.8+ |
| **Protocol** | Model Context Protocol (MCP) |
| **Databases** | MySQL 8.0+, PostgreSQL 12+ |
| **Frameworks** | pymysql, psycopg2 |
| **AI Integration** | LangChain, Google Gemini API |
| **Document Processing** | python-docx |
| **Key Dependencies** | FastMCP, psycopg2, pymysql, loguru |


## Tools per Server

### **Filesystem Server (pre-installed npx server)** `14 tools`
> **Complete file and directory management**

**Tools:**
- File Operations: `read_file`, `write_file`, `edit_file`
- Multi-File Support: `read_multiple_files`, `read_text_file`, `read_media_file`
- Directory Management: `create_directory`, `move_file`, `list_directory`
- Advanced Features: `search_files`, `get_file_info`, `directory_tree`

**Use Cases:** File automation, document workflows, script-based access control

---

### **Custom Tools Server** `5 tools`
> **Specialized document processing capabilities**

**Core Capabilities:**
- Document Creation: `create_docx`
- Document Reading: `read_docx`
- Document Editing: `edit_docx`
- File Management: `delete_file`
- Metadata Extraction: `Extract_Document_Metadata`

**Use Cases:** Automated documentation, reporting workflows, Office integration

---

### **MySQL Server** `3 tools`
> **Production-ready MySQL database integration**

**Core Capabilities:**
- Database Discovery: `mysql_list_databases`
- Query Execution: `mysql_query_executor`
- Schema Analysis: `mysql_schema_extractor`

**Use Cases:** Backend automation, data pipelines, database agents

---

### **PostgreSQL Server** `3 tools`
> **Enterprise PostgreSQL database management**

**Core Capabilities:**
- Database Exploration: `postgres_list_databases`
- Query Processing: `postgres_query_executor`
- Schema Extraction: `postgres_schema_extractor`

**Use Cases:** Multi-DB connectivity, real-time operations, enterprise data management


## Workflow

**Flow:** User Input → React Agent (Request Handler) → MCP Server Selection → Tool Execution → Response Processing → User Output


## Project Structure

```
Multi_Database_MCP_Client/
│
├── MCP_Client/
│   ├── app_langchain.py
│   ├── mcp_config.json
│
├── Servers/
│   ├── custom_tools_server.py
│   ├── mysql_server.py
│   ├── postgres_server.py
│
├── Full_Schema.txt
├── requirements.txt
└── README.md
```


## Installation & Setup Instructions
### Prerequisites:
- Python version 3.8
- mysql version 8+
- postgresql version 18+
- mysql, Postgresql server credentials
- MCP libraries installed (essentially FastMCP)

### Steps:
```
# Clone the repository
git clone https://github.com/dakshch0pra/Multi_Database_MCP_Client

# Navigate into the project
cd Multi_Database_MCP_Client

# Optional: Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

# Usage Snapshots
<img width="989" height="605" alt="image" src="https://github.com/user-attachments/assets/020e2277-1ca5-4b7f-be39-c2a169fd5696" />

## Eg 1: Databases Retrieval
<img width="1000" height="498" alt="image" src="https://github.com/user-attachments/assets/940c4572-70e0-475d-abc5-942b63244790" />


## Eg 2: MySQL DDL Command
<img width="996" height="327" alt="image" src="https://github.com/user-attachments/assets/ff87d963-7097-428f-af3e-38ebea921afa" />
The new table is present in mysql workbench:
<img width="571" height="440" alt="image" src="https://github.com/user-attachments/assets/58089fea-a686-42b8-946f-afeff6a81953" />

In case of a table already existing:
<img width="992" height="334" alt="image" src="https://github.com/user-attachments/assets/9ef259c0-a0fb-4695-b4c3-df9dff20c39b" />


## Eg 3: MySQL DML Command
<img width="1003" height="461" alt="image" src="https://github.com/user-attachments/assets/4e91e0a4-4bcb-4c8a-8be5-a3f10e9f0dca" />
The updated table is present in mysql workbench:
<img width="568" height="482" alt="image" src="https://github.com/user-attachments/assets/ba319944-5e70-46dc-844a-de669d09e5d9" />


## Eg 4: PostgreSQL DDL Command
<img width="1002" height="362" alt="image" src="https://github.com/user-attachments/assets/d37ba9ce-e94c-407a-9136-f52c88d53b65" />
The new table is present in pgadmin4 is:
<img width="748" height="494" alt="image" src="https://github.com/user-attachments/assets/ffbf1bee-57ff-424c-8f47-c0eb8efe7d75" />


## Eg 5: PostgreSQL DML Command
<img width="999" height="414" alt="image" src="https://github.com/user-attachments/assets/5f766667-2cb0-424f-b06c-978a413868c9" />


## Eg 6: Saving Extracted Schema
```
 {
      "type": "HumanMessage",
      "content": "Extract schema of each table in each database in both mysql and postgresql and present it in a readable form"
    },
    {
      "type": "AIMessage",
      "content": "Okay, I will extract the schemas for each table in each database for both MySQL and PostgreSQL and present them in a readable format.\n\n**MySQL Schemas:**\n\n*   **Database:** college\n    *   **Table:** department\n        ```\n        CREATE TABLE department (\n            dept_id INT PRIMARY KEY,\n            dept_name VARCHAR(50)\n        );\n        ```\n    *   **Table:** payment\n        ```\n        CREATE TABLE payment (\n            roll_no INT,\n            course_id INT,\n            amount DECIMAL(10, 2),\n            FOREIGN KEY (roll_no) REFERENCES students(roll_no)\n        );\n        ```\n    *   **Table:** students\n        ```\n        CREATE TABLE students (\n            roll_no INT PRIMARY KEY,\n            name VARCHAR(50),\n            age INT,\n            city VARCHAR(50)\n        );\n        ```\n    *   **Table:** students2\n        ```\n        CREATE TABLE students2 (\n            roll_no INT PRIMARY KEY,\n           
 name VARCHAR(50),\n            age INT,\n            city VARCHAR(50)\n        );\n        ```\n    *   **Table:** teacher\n        ```\n        CREATE TABLE teacher (\n            teacher_id INT PRIMARY KEY,\n            name VARCHAR(50),\n            dept_id INT,\n            
FOREIGN KEY (dept_id) REFERENCES department(dept_id)\n        );\n        ```\n\n*   **Database:** daksh\\_here\n    *   **Table:** game\n        ```\n        CREATE TABLE game (\n            roll_no INT PRIMARY KEY,\n            name VARCHAR(50),\n            age INT,\n         
   city VARCHAR(50)\n        );\n        ```\n    *   **Table:** good\n        ```\n        CREATE TABLE good (\n            roll_no INT PRIMARY KEY,\n            name VARCHAR(50),\n            age INT,\n            city VARCHAR(50)\n        );\n        ```\n    *   **Table:** king\n        ```\n        CREATE TABLE king (\n            roll_no INT PRIMARY KEY,\n            name VARCHAR(50),\n            age INT,\n            city VARCHAR(50)\n        );\n        ```\n    *   **Table:** newtable\n        ```\n        CREATE TABLE NewTable (\n            roll_no INT,\n            Name VARCHAR(255),\n            Books VARCHAR(255)\n        );\n        ```\n    *   **Table:** ring\n        ```\n        CREATE TABLE ring (\n            roll_no INT PRIMARY KEY,\n            name VARCHAR(50),\n            age INT,\n            city VARCHAR(50)\n        );\n        ```\n    *   **Table:** students\n        ```\n        CREATE TABLE students (\n            roll_no INT PRIMARY KEY,\n            name VARCHAR(50),\n            age INT,\n            city VARCHAR(50)\n        );\n        ```\n    *   **Table:** teacher\n        ```\n        CREATE TABLE teacher (\n            teacher_id INT PRIMARY KEY,\n            name VARCHAR(50),\n            dept_id INT\n        );\n        ```\n    *   **Table:** user\n        ```\n        CREATE TABLE user (\n            roll_no INT PRIMARY KEY,\n            name VARCHAR(50),\n            age INT,\n            city VARCHAR(50)\n        );\n        ```\n\n*   **Database:** leetcode\n    *   **Table:** customer\n        ```\n        CREATE TABLE customer (\n            id INT,\n            name VARCHAR(50),\n            referee_id INT\n        );\n        ```\n    *   **Table:** q1\\_products\n        ```\n        CREATE TABLE q1_products (\n            product_id INT,\n            product_name VARCHAR(50),\n            sale_price INT\n        );\n        ```\n    *   **Table:** tweets\n        ```\n        CREATE TABLE tweets (\n            tweet_id INT,\n            content VARCHAR(255)\n        );\n        ```\n    *   **Table:** views\n        ```\n        CREATE TABLE views (\n            article_id INT,\n            author_id INT,\n            viewer_id INT,\n           
 view_date DATE\n        );\n        ```\n    *   **Table:** world\n        ```\n        CREATE TABLE world (\n            name VARCHAR(50),\n            continent VARCHAR(50),\n            area INT,\n            population INT,\n            gdp INT\n        );\n        ```\n\n*   **Database:** sakila\n    *   Due to the large number of tables in the sakila database, I will only show the schema for the 'actor' table as an example.  If you would like the schemas for the other tables, please request them individually.\n        ```\n        CREATE TABLE actor (\n            actor_id SMALLINT,\n            first_name VARCHAR(45),\n            last_name VARCHAR(45),\n            last_update TIMESTAMP\n        );\n        ```\n\n**PostgreSQL Schemas:**\n\n*   **Database:** postgres\n    *   **Table:** college\n        ```\n        CREATE TABLE college (\n            roll_no integer,\n            name character varying,\n            age integer\n        );\n        ```\n    *   **Table:** people\n        ```\n        CREATE TABLE people (\n            name character varying,\n            age integer\n        );\n        ```\n    *   **Table:** shivin\n        ```\n        CREATE TABLE shivin (\n            name character varying,\n            age integer\n        );\n        ```\n\n*   **Database:** books\n    *   **Table:** fantasy\n        ```\n        CREATE TABLE fantasy (\n            book_id integer,\n            name character varying,\n            reviews integer,\n            CONSTRAINT fantasy_reviews_check CHECK ((reviews >= 0) AND (reviews <= 5))\n        );\n        ```\n    *   **Table:** mythology\n        ```\n        CREATE TABLE mythology (\n            book_id integer,\n            name character varying(255),\n            reviews integer,\n            CONSTRAINT mythology_reviews_check CHECK ((reviews >= 0) AND (reviews <= 5))\n        );\n        ```\n\nI have presented the schemas in a readable format.  Do you want me to save this information to the \"Full\\_Schema.txt\" file in the C:\\\\testfolder directory?"
    },
    {
      "type": "HumanMessage",
      "content": "yes, save it"
    },
    {
      "type": "AIMessage",
      "content": "I have updated the \"Full\\_Schema.txt\" file in the C:\\\\testfolder directory with the schemas in the readable format as presented above."
    }
  ]
}
```
Extracted Schema saved in file: Full_Schema.txt.



