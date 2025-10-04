import pymysql
import json
from loguru import logger
from mcp.server.fastmcp import FastMCP
from typing import Optional

mcp = FastMCP("Mysql_Server")

#List Database Function
def list_databases() -> str:
    """List all databases present in the MySQL server."""
    
    conn = pymysql.connect(
        host="localhost",
        database="sys",  # Connect to the default 'sys' database
        user="root",
        password="pass123"
    )

    cursor = conn.cursor()

    cursor.execute("SHOW DATABASES;")

    databases = cursor.fetchall()

    for db in databases:
        print(db[0])

    cursor.close()
    conn.close()

    return json.dumps(databases)

#Small list database tool
@mcp.tool(name="list_databases", description="List all databases present in the MySQL server.")
def list_databases_tool() -> str:
    """If the user asks for number of databases present in MySQL server, use this tool."""
    return list_databases()


#Database exists function


#Simple Query Tool


if __name__ == "__main__":
    mcp.run(transport='stdio')
