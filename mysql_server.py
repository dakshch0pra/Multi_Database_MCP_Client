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

import asyncio
import aiomysql
import json
from loguru import logger
from mcp.server.fastmcp import FastMCP
from typing import Optional

class AsyncMySQLServer:
    def __init__(self):
        self.pool: Optional[aiomysql.Pool] = None
        self.db_config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'pass123',
            # Don't specify 'db' here - we'll switch databases as needed
        }
    
    async def initialize_pool(self):
        """Initialize connection pool once during server startup"""
        if self.pool is None:
            logger.info("Creating MySQL connection pool...")
            self.pool = await aiomysql.create_pool(
                minsize=1,
                maxsize=10,
                **self.db_config
            )
            logger.info("MySQL connection pool created successfully")
    
    async def execute_query(self, sql_query: str, database: str):
        """
        Execute SQL query on specified database using connection pool
        
        Key Concepts:
        1. Use existing pool (no opening/closing connections)
        2. Acquire connection from pool temporarily
        3. Switch to target database for this connection
        4. Execute query with appropriate transaction handling
        5. Connection automatically returns to pool
        """
        
        # Ensure pool exists
        if not self.pool:
            await self.initialize_pool()
        
        try:
            # Step 1: Get connection from pool (async context manager)
            async with self.pool.acquire() as connection:
                logger.info(f"Acquired connection from pool for database: {database}")
                
                # Step 2: Switch to target database
                await connection.select_db(database)
                
                # Step 3: Determine if we need transaction
                query_type = sql_query.strip().upper()
                is_read_query = query_type.startswith(('SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN'))
                
                if is_read_query:
                    # READ queries - no transaction needed
                    async with connection.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute(sql_query)
                        results = await cursor.fetchall()
                        
                        return {
                            'success': True,
                            'query_type': 'READ',
                            'database': database,
                            'row_count': len(results),
                            'data': results
                        }
                else:
                    # WRITE queries - use transaction
                    async with connection.cursor(aiomysql.DictCursor) as cursor:
                        # Start transaction
                        await connection.begin()
                        logger.info(f"Transaction started for write query on {database}")
                        
                        try:
                            await cursor.execute(sql_query)
                            await connection.commit()
                            logger.info(f"Transaction committed successfully on {database}")
                            
                            return {
                                'success': True,
                                'query_type': 'WRITE',
                                'database': database,
                                'rows_affected': cursor.rowcount
                            }
                            
                        except Exception as query_error:
                            await connection.rollback()
                            logger.error(f"Query failed, rolled back transaction on {database}")
                            raise query_error
                            
        except Exception as e:
            logger.error(f"Query execution failed on {database}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'database': database,
                'query': sql_query
            }
    
    async def close_pool(self):
        """Clean shutdown of connection pool"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("MySQL connection pool closed")

# Initialize server and MCP
mcp = FastMCP("MySQL Async Server")
mysql_server = AsyncMySQLServer()

@mcp.tool()
async def query_executor(sql_query: str, database: str) -> str:
    """
    Execute SQL queries on MySQL database with proper async connection pooling
    
    Args:
        sql_query: The SQL query to execute
        database: Target database name (required)
    
    Returns:
        Formatted result string with query results or error information
    """
    
    # Validation
    if not database or not database.strip():
        return " Database name is required and cannot be empty"
    
    if not sql_query or not sql_query.strip():
        return " SQL query is required and cannot be empty"
    
    logger.info(f"Executing query on '{database}': {sql_query[:100]}...")
    
    # Execute query using connection pool
    result = await mysql_server.execute_query(sql_query, database)
    
    # Format response based on result
    if result['success']:
        if result['query_type'] == 'READ':
            # Format SELECT results
            data_preview = ""
            if result['data']:
                # Show first few rows as preview
                preview_count = min(3, len(result['data']))
                data_preview = "\n" + json.dumps(result['data'][:preview_count], indent=2, default=str)
                if len(result['data']) > preview_count:
                    data_preview += f"\n... and {len(result['data']) - preview_count} more rows"
            
            return f""" Query executed successfully on '{database}'
    Query Type: {result['query_type']}
    Rows returned: {result['row_count']}{data_preview}"""
            
        else:
            # Format WRITE results
            return f""" Query executed successfully on '{database}'
    Query Type: {result['query_type']}
    Rows affected: {result['rows_affected']}"""
    else:
        # Format error response
        return f""" Query failed on '{database}'
    Error: {result['error']}
    Query: {result['query'][:400]}"""

# Server lifecycle management
async def startup():
    """Initialize server resources"""
    await mysql_server.initialize_pool()

async def shutdown():
    """Cleanup server resources"""
    await mysql_server.close_pool()

if __name__ == "__main__":
    try:
        # Initialize pool before starting MCP server
        asyncio.run(startup())
        mcp.run(transport='stdio')
    finally:
        # Clean shutdown
        asyncio.run(shutdown())


