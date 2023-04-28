import snowflake.connector
from snowflake.connector import DictCursor, ProgrammingError
import os
from fastapi import HTTPException


#Snowflake credentials
user = os.getenv('SNOWFLAKE_USER')
password = os.getenv('SNOWFLAKE_PASSWORD')
account = os.getenv('SNOWFLAKE_ACCOUNT')
warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
database = os.getenv('SNOWFLAKE_DATABASE')
schema = os.getenv('SNOWFLAKE_SCHEMA')

def snowflake_conn():
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )
    return conn
#Function to Create User
def create_user(full_name, username, tier, hashed_password):
    # Set up connection to Snowflake
    conn = snowflake_conn()
    try:
        # Create a cursor object using the DictCursor to work with dictionaries
        with conn.cursor(DictCursor) as cursor:
            # Execute the INSERT statement to add the new user to the table
            cursor.execute(
                "INSERT INTO users (full_name, username, tier, hashed_password, created_at) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP())",
                (full_name, username, tier, hashed_password)
            )
            
            # Commit the transaction
            conn.commit()
            
            # Return the ID of the new user
            return 1
            
    except ProgrammingError as e:
        print(f"Error: {e.msg}")
        


def get_users():
    
    try:
        # Create a cursor object using the DictCursor to work with dictionaries
        conn = snowflake_conn()
        with conn.cursor(DictCursor) as cursor:
    
            cursor.execute(f"select  username, full_name, username, tier, hashed_password, disabled from users")
            x = cursor.fetchall()
            # print(x)
            users_dict = dict()
            for i in x:
                users_dict[i['USERNAME']] = i

            return users_dict
            
    except ProgrammingError as e:
        print(f"Error: {e.msg}")
        

#Check if user exists
def check_user_exists(username):
    
    try:
        # Create a cursor object using the DictCursor to work with dictionaries
        conn = snowflake_conn()
        with conn.cursor(DictCursor) as cursor:
            cursor.execute(f"select  username, full_name, username, tier, hashed_password, disabled from users where username = '{username}'")
            users_dict = cursor.fetchall()[0]
            # users_dict = dict()
            # print(users_dict)
            if users_dict['USERNAME'] == username:
                return True
            else:
                raise Exception(False)
    except Exception as e:
        return e

#Function to get user tier
def get_user_tier(username):
    try:
        # Create a cursor object using the DictCursor to work with dictionaries
        conn = snowflake_conn()
        with conn.cursor(DictCursor) as cursor:
            cursor.execute(f"select  username, full_name, username, tier, hashed_password, disabled from users where username = '{username}'")
            x = cursor.fetchall()
            # print(x)
            users_dict = dict()
            for i in x:
                users_dict[i['USERNAME']] = i
            if len(users_dict) > 0:
                return users_dict[username]['TIER']
            else:
                raise Exception(False)
    except Exception as e:
        return e


#Function to count api calls
def count_api_calls(username,tier):
    conn = snowflake_conn()
    with conn.cursor(DictCursor) as cursor:

        query1 = f"SELECT COUNT(*) FROM API_CALLS WHERE USERNAME = '{username}' AND TIER = '{tier}' AND time >= DATEADD(HOUR, -1, CURRENT_TIMESTAMP());"
        cursor.execute(query1)
        api_calls_in_last_hour = cursor.fetchall()[0]
        api_calls_in_last_hour = api_calls_in_last_hour['COUNT(*)']
        query2 = f"SELECT hourly_limit FROM api_plans WHERE tier = '{tier}';"
        cursor.execute(query2)
        hourly_limit = cursor.fetchall()
        if len(hourly_limit) <= 0:
            return True
        else:
            print('iran')
            hourly_limit=hourly_limit[0]
            hourly_limit = hourly_limit['HOURLY_LIMIT']
            if api_calls_in_last_hour <= hourly_limit:
                return True
            else:
                return False

def add_api_call(username,tier):
    conn = snowflake_conn()
    with conn.cursor(DictCursor) as cursor:
        query = f"INSERT INTO API_CALLS (USERNAME, TIER, TIME) VALUES ('{username}', '{tier}', CURRENT_TIMESTAMP());"
        cursor.execute(query)
        conn.commit()
        return True

def update_user_password(new_hashed_password, username):
    conn = snowflake_conn()
    with conn.cursor(DictCursor) as cursor:
        query = f"UPDATE users SET hashed_password = '{new_hashed_password}' WHERE username = '{username}';"
        cursor.execute(query)
        conn.commit()
        return True
    

def count_api_calls_left(username):
    conn = snowflake_conn()
    with conn.cursor(DictCursor) as cursor:

        query1 = f"SELECT COUNT(*) FROM API_CALLS WHERE USERNAME = '{username}' AND time >= DATEADD(HOUR, -1, CURRENT_TIMESTAMP());"
        cursor.execute(query1)
        api_calls_in_last_hour = cursor.fetchall()[0]
        return api_calls_in_last_hour['COUNT(*)']
    

# #Run all the functions
if __name__ == "__main__":
    print(check_user_exists("vikas"))
    # print(get_user_tier("midhun"))
    # print(count_api_calls("midhun","gold"))









###############Test Code################


# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# def get_password_hash(password):
#     return pwd_context.hash(password)



# print(get_password_hash("secret"))
create_user("vikas", "vikas", 1, "$2b$12$o/w42FyTMySTPbsxDO7pm.D61XPTH4XA62xtDSmFJ44PYCKj2ZKBa")
    

