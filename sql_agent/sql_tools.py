from sql_database import SQLDatabase

QUERY_CHECKER = """
{query}
Double check the SQL Server query above for common mistakes, including:
- Using TOP instead of LIMIT
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

Output the final SQL query only.

SQL Query: """

class SQLTools:
    def __init__(self, llm, sql_database: SQLDatabase):
        sql_db_query_description = """
        Input to this tool is a detailed and correct SQL query, output is a result from the database. 
        If the query is not correct, an error message will be returned. 
        If an error is returned, rewrite the query, check the query, and try again. 
        If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields.
        """
        sql_db_schema_description = """
        Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables.    

        Example Input: "table1, table2, table3"
        """
        sql_db_list_tables_description = "Input is an empty string, output is a comma separated list of tables in the database."
        sql_db_query_checker_description = """
        Use this tool to double check if your query is correct before executing it.
        Always use this tool before executing a query with sql_db_query!
        """

        self.descriptions = {
            'sql_db_query': sql_db_query_description,
            'sql_db_list_tables': sql_db_list_tables_description,
            'sql_db_schema': sql_db_schema_description,
            'sql_db_query_checker': sql_db_query_checker_description
            }
        
        self.llm = llm
        self.sql_database = sql_database
        
    def sql_db_query(self, command):
        return self.sql_database.run_sql(command)
    
    def sql_db_list_tables(self):
        return self.sql_database.get_usable_table_names()
    
    def sql_db_schema(self, table_names: str):
        table_names_list = [t.strip() for t in table_names.split(",")]
        result = ""
        for table_name in table_names_list:
            create_table_command_str = self.sql_database.get_table_indexes(table_name)
            result += create_table_command_str
            sample_rows_str = self.sql_database.get_sample_rows(table_name)
            result += sample_rows_str

        return result
    
    def sql_db_query_checker(self, query):
        prompt = QUERY_CHECKER.format(query=query)
        response = self.llm.get_response(prompt)
        
        return response