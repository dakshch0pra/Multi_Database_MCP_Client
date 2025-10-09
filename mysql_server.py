#PYMYSQL TRIAL
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
            port=3306,
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
@mcp.tool(name="mysql_list_databases", description="List all databases present in the MySQL server.")
def list_databases_tool() -> str:
    """If the user asks for number of databases present in MySQL server, use this tool."""
    return list_databases()


#Database exists function

def database_exists(database_name: str) -> bool:
    """Check if a database exists."""
    try:
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="pass123"
            # Don't specify database here
        )
        cursor = conn.cursor()
        
        # MySQL-specific query
        cursor.execute("SHOW DATABASES LIKE %s", (database_name,))

        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Database check error: {e}")
        return False


#Simple Query Tool
current_connection = None
current_database = None

@mcp.tool(name="mysql_query_executor", description="Execute SQL queries on a specified MySQL database and return results in JSON format.")
def query_data(sql_query: str, database_name: str) -> str:
    """Execute MySQL queries safely with automatic database switching."""
    global current_connection, current_database
    
    logger.info(f"Received SQL query: {sql_query} for database: {database_name}")
    
    DB_USER = "root"
    DB_PASS = "pass123"
    DB_HOST = "localhost"
    DB_PORT = 3306
    
    try:
        # Check if we need to switch databases
        if current_database != database_name or current_connection is None:
            logger.info(f"Switching from {current_database} to {database_name}")
      
            # Validate database exists
            if not database_exists(database_name):
                return json.dumps({
                    "status": "error",
                    "error": f"Database '{database_name}' does not exist",
                    "available_databases": list_databases(),
                    "query": sql_query
                }, indent=2)
            
            # Close existing connection
            if current_connection:
                current_connection.close()
                logger.info(f"Closed connection to {current_database}")
            
            # Create new connection
            current_connection = pymysql.connect(
                database=database_name,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT
            )
            current_database = database_name
            logger.info(f"Established new connection to {database_name}")
        
        # Execute query on current connection
        cursor = current_connection.cursor()
        cursor.execute(sql_query)
        current_connection.commit()
        
        # Handle results (same as your existing logic)
        query_upper = sql_query.strip().upper()
        
        if query_upper.startswith(('SELECT', 'WITH', 'DESCRIBE', 'SHOW', 'EXPLAIN')):
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description] if cursor.description else []
            
            if colnames and rows:
                result = [dict(zip(colnames, row)) for row in rows]
            else:
                result = rows
            
            return json.dumps({
                "status": "success",
                "database": database_name,
                "data": result,
                "sql_query": sql_query,
                "row_count": len(rows) if rows else 0
            }, indent=2, default=str)
            
        else:
            affected_rows = cursor.rowcount if cursor.rowcount >= 0 else None
            
            return json.dumps({
                "status": "success", 
                "database": database_name,
                "message": f"Query executed successfully.",
                "sql_query": sql_query,
                "affected_rows": affected_rows,
                "query_type": "DDL/DML"
            }, indent=2)
            
    except Exception as e:
        return json.dumps({
            "status": "error",
            "database": database_name,
            "error": str(e),
            "query": sql_query
        }, indent=2)
        
    finally:
        if cursor is not None:
            cursor.close()

# # SCHEMA EXTRACTION TOOL
@mcp.tool(name="mysql_schema_extractor", description="Extract and return the schema of the specified mySQL database in a .txt file format.")
def extract_database_schema(database_name: str) -> str:
    """Extract comprehensive schema information from a mySQL database."""
    
    # Check if database exists first
    if not database_exists(database_name):
        return json.dumps({
            "status": "error",
            "error": f"Database '{database_name}' does not exist",
            "available_databases": list_databases()
        }, indent=2)
    
    try:
        # Connect to the specified database
        conn = pymysql.connect(
            database=database_name,
            user="root",
            password="pass123",
            host="localhost",
            port= 3306
        )
        cursor = conn.cursor()
        
        schema_info = []
        schema_info.append(f"DATABASE SCHEMA: {database_name}")
        schema_info.append("=" * 50)
        schema_info.append("")
        
        # 1. Get all table names
        cursor.execute(f"""
            SELECT table_name 
            FROM information_schema.tables
            WHERE table_schema = '{database_name}'
            ORDER BY table_name;""")


        tables = cursor.fetchall()
        
        schema_info.append("TABLE NAMES (Node Types):")
        schema_info.append("-" * 30)
        for table in tables:
            schema_info.append(f"• {table[0]}")
        schema_info.append("")
        
        # 2. For each table, get column definitions and constraints
        for table in tables:
            table_name = table[0]
            schema_info.append(f"TABLE: {table_name}")
            schema_info.append("=" * 40)
            
            # Get column information
            cursor.execute("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default,
                    character_maximum_length
                FROM information_schema.columns 
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position;
            """, (table_name,))
            
            columns = cursor.fetchall()
            
            schema_info.append("COLUMNS (Attributes/Properties):")
            schema_info.append("-" * 35)
            
            for col in columns:
                col_name, data_type, nullable, default, max_length = col
                
                # Format column info
                col_info = f"• {col_name}: {data_type}"
                if max_length:
                    col_info += f"({max_length})"
                if nullable == "NO":
                    col_info += " NOT NULL"
                if default:
                    col_info += f" DEFAULT {default}"
                
                schema_info.append(col_info)
            
            schema_info.append("")
            
            # 3. Get primary keys
            cursor.execute("""
                SELECT column_name
                FROM information_schema.key_column_usage
                WHERE table_name = %s 
                AND constraint_name IN (
                    SELECT constraint_name
                    FROM information_schema.table_constraints
                    WHERE table_name = %s AND constraint_type = 'PRIMARY KEY'
                );
            """, (table_name, table_name))
            
            primary_keys = cursor.fetchall()
            if primary_keys:
                schema_info.append("PRIMARY KEYS:")
                schema_info.append("-" * 15)
                for pk in primary_keys:
                    schema_info.append(f"• {pk[0]}")
                schema_info.append("")
            
            # 4. Get foreign key relationships
            # cursor.execute("""
            #     SELECT 
            #         kcu.column_name,
            #         ccu.table_name AS foreign_table_name,
            #         ccu.column_name AS foreign_column_name,
            #         tc.constraint_name
            #     FROM information_schema.table_constraints AS tc 
            #     JOIN information_schema.key_column_usage AS kcu
            #         ON tc.constraint_name = kcu.constraint_name
            #         AND tc.table_schema = kcu.table_schema
            #     JOIN information_schema.constraint_column_usage AS ccu
            #         ON ccu.constraint_name = tc.constraint_name
            #         AND ccu.table_schema = tc.table_schema
            #     WHERE tc.constraint_type = 'FOREIGN KEY' 
            #     AND tc.table_name = %s;
            # """, (table_name,))
            cursor.execute("""
                SELECT 
                    column_name,
                    referenced_table_name AS foreign_table_name,
                    referenced_column_name AS foreign_column_name,
                    constraint_name
                FROM information_schema.key_column_usage
                WHERE table_schema = %s 
                AND table_name = %s
                AND referenced_table_name IS NOT NULL;
                """, (database_name, table_name))
            
            foreign_keys = cursor.fetchall()
            if foreign_keys:
                schema_info.append("FOREIGN KEY RELATIONSHIPS (Node Connections):")
                schema_info.append("-" * 45)
                for fk in foreign_keys:
                    col_name, ref_table, ref_column, constraint_name = fk
                    schema_info.append(f"• {col_name} → {ref_table}.{ref_column}")
                schema_info.append("")
            
            # 5. Get check constraints and unique constraints
            cursor.execute("""
                SELECT constraint_name, check_clause
                FROM information_schema.check_constraints
                WHERE constraint_schema = 'public'
                AND constraint_name IN (
                    SELECT constraint_name
                    FROM information_schema.table_constraints
                    WHERE table_name = %s AND constraint_type = 'CHECK'
                );
            """, (table_name,))
            
            check_constraints = cursor.fetchall()
            if check_constraints:
                schema_info.append("CHECK CONSTRAINTS:")
                schema_info.append("-" * 20)
                for constraint in check_constraints:
                    constraint_name, check_clause = constraint
                    schema_info.append(f"• {constraint_name}: {check_clause}")
                schema_info.append("")
            
            schema_info.append("") # Extra spacing between tables
        
        # Close connection
        cursor.close()
        conn.close()
        
        # Join all schema information
        schema_text = "\n".join(schema_info)
        
        return json.dumps({
            "status": "success",
            "database": database_name,
            "schema_content": schema_text,
            "message": f"Schema extracted successfully from database '{database_name}'"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "database": database_name,
            "error": str(e)
        }, indent=2)

if __name__ == "__main__":
    mcp.run(transport='stdio')
