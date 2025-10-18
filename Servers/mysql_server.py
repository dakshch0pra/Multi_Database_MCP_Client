# AIOMYSQL TRIAL
# import asyncio
# import aiomysql
# import json
# from loguru import logger
# from mcp.server.fastmcp import FastMCP
# from typing import Optional

# class AsyncMySQLServer:
#     """Simple Async MySQL MCP Server"""

#     host = 'localhost'
#     port = 3306
#     user = 'root'             # ← Update these
#     password = 'pass123' # ← Update these
#     db = 'college'

#     def __init__(self):
#         self.pool: Optional[aiomysql.Pool] = None
#         self.db_config = {
#             'host': self.host,
#             'user': self.user,
#             'port': self.port,
#             'password': self.password,
#             'db': self.db
#         }
    
#     async def initialize_pool(self):
#         """Step 1: Create connection pool"""
#         if self.pool is None:
#             logger.info("Creating MySQL connection pool...")
#             try:
#                 self.pool = await aiomysql.create_pool(**self.db_config)
#                 logger.info("MySQL pool created successfully")
#                 #NEW
#                 # async with self.pool.acquire() as conn:
#                 #     async with conn.cursor() as cur:
#                 #         await cur.execute("SELECT VERSION(), DATABASE();")
#                 # result = await cur.fetchone()
#                 # print(f"Connected to MySQL Server Version: {result[0]}")
#                 # print(f"Using Database: {result[1]}")
#                 #NEW END
#             except Exception as e:
#                 logger.info(f"Failed to create pool: {e}")
#                 raise
    
#     async def close_pool(self):
#         """Clean up connection pool"""
#         if self.pool:
#             self.pool.close()
#             await self.pool.wait_closed()
#             logger.info("MySQL pool closed")

# # NEW TRANSACTION
#     async def execute_query_with_transaction(self, sql_query: str, database: str):
#         """Execute query with proper transaction management - database is REQUIRED"""
#         if not database:
#             raise ValueError("Database name is required for all queries")
        
#         await self.initialize_pool()
        
#         try:
#             async with self.pool.acquire() as conn:
#                 # Always switch to the specified database
#                 await conn.select_db(database)
#                 logger.info(f"Connected to database: {database}")
                
#                 async with conn.cursor(aiomysql.DictCursor) as cursor:
#                     await conn.begin()
#                     logger.info(f"Transaction started on '{database}' for query: {sql_query[:50]}...")
                    
#                     try:
#                         await cursor.execute(sql_query)
                        
#                         if sql_query.strip().upper().startswith('SELECT'):
#                             results = await cursor.fetchall()
#                             await conn.commit()
#                             logger.info(f"SELECT query executed on '{database}' and committed")
#                             return {
#                                 'success': True,
#                                 'query_type': 'SELECT',
#                                 'database': database,
#                                 'rows_returned': len(results),
#                                 'data': results
#                             }
#                         else:
#                             await conn.commit()
#                             logger.info(f"Write query executed on '{database}', rows affected: {cursor.rowcount}")
#                             return {
#                                 'success': True,
#                                 'query_type': 'MODIFY',
#                                 'database': database,
#                                 'rows_affected': cursor.rowcount
#                             }
                            
#                     except Exception as query_error:
#                         await conn.rollback()
#                         logger.error(f"Query failed on '{database}', transaction rolled back: {query_error}")
#                         raise query_error
                            
#         except Exception as e:
#             logger.error(f"Transaction failed on '{database}': {e}")
#             return {
#                 'success': False,
#                 'error': str(e),
#                 'query': sql_query,
#                 'database': database
#             }
# # MULTIPLE DBS
#     async def execute_multi_database_queries(self, queries_with_dbs: list):
#         """Execute queries on multiple databases concurrently - ASYNC MAGIC!"""
#         await self.initialize_pool()
        
#         logger.info(f"Executing {len(queries_with_dbs)} queries across multiple databases concurrently")
        
#         # Create tasks for concurrent execution
#         tasks = []
#         for db_name, sql_query in queries_with_dbs:
#             task = self.execute_query_with_transaction(sql_query, db_name)
#             tasks.append((db_name, sql_query, task))
        
#         # Execute all queries concurrently
#         results = []
#         for db_name, sql_query, task in tasks:
#             try:
#                 result = await task
#                 result['database_name'] = db_name
#                 result['original_query'] = sql_query
#                 results.append(result)
#             except Exception as e:
#                 results.append({
#                     'success': False,
#                     'error': str(e),
#                     'database_name': db_name,
#                     'original_query': sql_query
#                 })
        
#         return {
#             'success': True,
#             'total_queries': len(queries_with_dbs),
#             'results': results,
#             'execution_type': 'concurrent'
#         }

#     # SINGLE TABLE
#     async def create_table_in_database(self, database: str, table_name: str, columns: dict):
#         """Create a test table in specified database"""
#         await self.initialize_pool()
        
#         # Build CREATE TABLE query
#         column_definitions = []
#         for col_name, col_type in columns.items():
#             column_definitions.append(f"`{col_name}` {col_type}")
        
#         create_query = f"""
#         CREATE TABLE IF NOT EXISTS `{table_name}` (
#             {', '.join(column_definitions)}
#         )
#         """
        
#         logger.info(f"Creating table '{table_name}' in database '{database}'")
#         return await self.execute_query_with_transaction(create_query, database)

#     async def list_databases(self):
#         """Simple function to list all databases in MySQL server"""
#         await self.initialize_pool()

#         try:
#             async with self.pool.acquire() as conn:
#                 async with conn.cursor() as cursor:
#                     # MySQL command to show all databases
#                     await cursor.execute("SHOW DATABASES")
#                     results = await cursor.fetchall()

#                     # Extract database names from tuples
#                     database_names = [db[0] for db in results]

#                     return {
#                         'success': True,
#                         'databases': database_names,
#                         'count': len(database_names)
#                     }

#         except Exception as e:
#             return {
#                 'success': False,
#                 'error': str(e),
#                 'databases': [],
#                 'count': 0
#             }

    
#     # async def execute_query(self, sql_query: str):
#     #     """Step 2: Execute a single query"""
#     #     await self.initialize_pool()
        
#     #     try:
#     #         async with self.pool.acquire() as conn:
#     #             async with conn.cursor(aiomysql.DictCursor) as cursor:
#     #                 await cursor.execute(sql_query)
                    
#     #                 # Handle different query types
#     #                 if sql_query.strip().upper().startswith('SELECT'):
#     #                     results = await cursor.fetchall()
#     #                     return {
#     #                         'success': True,
#     #                         'query_type': 'SELECT',
#     #                         'rows_returned': len(results),
#     #                         'data': results
#     #                     }
#     #                 else:
#     #                     # INSERT, UPDATE, DELETE, etc.
#     #                     await conn.commit()
#     #                     return {
#     #                         'success': True,
#     #                         'query_type': 'MODIFY',
#     #                         'rows_affected': cursor.rowcount
#     #                     }
                        
#     #     except Exception as e:
#     #         return {
#     #             'success': False,
#     #             'error': str(e),
#     #             'query': sql_query
#     #         }
        
# mcp = FastMCP("MySQL Async Server")
# mysql_server = AsyncMySQLServer()

# @mcp.tool()
# async def list_databases() -> str:
#     """List all available databases in the MySQL server"""
#     print("Listing all databases...")
    
#     result = await mysql_server.list_databases()
    
#     if result['success']:
#         if result['count'] > 0:
#             databases_list = "\n".join([f"  • {db}" for db in result['databases']])
#             return f"Found {result['count']} database(s):\n{databases_list}"
#         else:
#             return "No databases found"
#     else:
#         return f"Failed to list databases: {result['error']}"
    
# @mcp.tool()
# async def query_database(sql_query: str, database: str) -> str:
#     """Execute SQL query with transaction management on specified database
    
#     Args:
#         database: The database name to execute the query on (REQUIRED)
#     """
#     if not database:
#         return "Database name is required. Please specify which database to query."
    
#     logger.info(f"Executing query on database '{database}': {sql_query}")
    
#     result = await mysql_server.execute_query_with_transaction(sql_query, database)
    
#     if result['success']:
#         if result['query_type'] == 'SELECT':
#             return f"Query successful on '{result['database']}'!\nRows returned: {result['rows_returned']}\nData: {json.dumps(result['data'], indent=2, default=str)}"
#         else:
#             return f"Query successful on '{result['database']}'!\nRows affected: {result['rows_affected']}"
#     else:
#         return f"Query failed on '{result['database']}': {result['error']}"

# @mcp.tool()
# async def query_multiple_databases(queries: str) -> str:
#     """
#     Execute mysql queries on multiple databases simultaneously
#     """
#     logger.info("Processing multi-database queries")
    
#     try:
#         query_pairs = []
#         for query_pair in queries.split(';'):
#             if ':' in query_pair:
#                 db_name, sql = query_pair.split(':', 1)
#                 db_name = db_name.strip()
#                 sql = sql.strip()
                
#                 if not db_name:
#                     return f"Database name missing in query: '{query_pair}'"
#                 if not sql:
#                     return f"SQL query missing for database '{db_name}'"
                    
#                 query_pairs.append((db_name, sql))
#             else:
#                 return f"Invalid format in: '{query_pair}'. Use 'database:query' format"
        
#         if not query_pairs:
#             return "No valid queries found. Format: 'db1:query1;db2:query2'"
        
#         result = await mysql_server.execute_multi_database_queries(query_pairs)
        
#         if result['success']:
#             output = f"Executed {result['total_queries']} queries concurrently:\n\n"
            
#             for i, query_result in enumerate(result['results'], 1):
#                 if query_result['success']:
#                     if query_result.get('query_type') == 'SELECT':
#                         output += f"{i}. {query_result['database_name']}: {len(query_result['data'])} rows\n"
#                     else:
#                         output += f"{i}. {query_result['database_name']}: {query_result['rows_affected']} rows affected\n"
#                 else:
#                     output += f"{i}. {query_result['database_name']}: {query_result['error']}\n"
            
#             return output
#         else:
#             return f"Multi-database execution failed: {result.get('error', 'Unknown error')}"
            
#     except Exception as e:
#         return f"Failed to parse or execute multi-database queries: {str(e)}"

# @mcp.tool()
# async def create_table(database: str, table_name: str) -> str:
#     """Create a table to verify database operations
    
#     Args:
#         database: The database name where to create the table (REQUIRED)
#         table_name: The name of the table to create
#     """
#     if not database:
#         return "Database name is required"
    
#     logger.info(f"Creating test table '{table_name}' in database '{database}'")
    
#     test_columns = {
#         'id': 'INT AUTO_INCREMENT PRIMARY KEY',
#         'name': 'VARCHAR(50) NOT NULL',
#         'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
#     }
    
#     result = await mysql_server.create_table_in_database(database, table_name, test_columns)
    
#     if result['success']:
#         return f"Successfully created table '{table_name}' in database '{database}'"
#     else:
#         return f"Failed to create table '{table_name}' in database '{database}': {result['error']}"

# # @mcp.tool()
# # async def get_database_info(database: str) -> str:
# #     """Get information about a specific database
    
# #     Args:
# #         database: The database name to get info about (REQUIRED)
# #     """
# #     if not database:
# #         return "Database name is required"
    
# #     info_query = f"""
# #     SELECT 
# #         '{database}' as database_name,
# #         COUNT(*) as table_count,
# #         SUM(data_length + index_length) / 1024 / 1024 as size_mb
# #     FROM information_schema.tables 
# #     WHERE table_schema = '{database}'
# #     """
    
# #     result = await mysql_server.execute_query_with_transaction(info_query, 'information_schema')
    
# #     if result['success'] and result['data']:
# #         data = result['data'][0]
# #         return f"Database '{database}' Info:\n• Tables: {data['table_count']}\n• Size: {data['size_mb']:.2f} MB"
# #     else:
# #         return f"Failed to get info for database '{database}': {result.get('error', 'Unknown error')}"





# # @mcp.tool()
# # async def query_database(sql_query: str) -> str:
# #     """Execute SQL queries on MySQL database"""
# #     print(f"🔍 Executing query: {sql_query}")
    
# #     result = await mysql_server.execute_query(sql_query)
    
# #     if result['success']:
# #         if result['query_type'] == 'SELECT':
# #             return f"✅ Query successful!\nRows returned: {result['rows_returned']}\nData: {json.dumps(result['data'], indent=2, default=str)}"
# #         else:
# #             return f"✅ Query successful!\nRows affected: {result['rows_affected']}"
# #     else:
# #         return f"❌ Query failed: {result['error']}"

# if __name__ == "__main__":
#     # print("=== Starting MySQL MCP Server ===")
#     # print("Available tools: query_database, test_connection, show_tables")
#     # asyncio.run(mysql_server.initialize_pool())
#     mcp.run(transport='stdio')

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