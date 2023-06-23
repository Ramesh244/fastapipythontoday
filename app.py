from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Dict
import pymysql
# import mysql.connector
# def get_db():
#     db = mysql.connector.connect(
#         host="localhost",
#         user="your-username",
#         password="your-password",
#         database="your-database"
#     )
#     return db



# Database connection settings
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'Ramesh244@'
DB_NAME = 'Todolistapi'

# Create FastAPI app instance
app = FastAPI()

# Basic authentication
security = HTTPBasic()

# Define models
class TodoItem(BaseModel):
    id: int
    title: str
    description: str

class TodoItemCreate(BaseModel):
    title: str
    description: str

# Database connection dependency
def get_db_conn():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    return conn

# Authentication dependency
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    # Replace with your own authentication logic
    if credentials.username != "admin" or credentials.password != "admin":
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return True

# Retrieve all todo items
@app.get("/todos")
def get_todo_list(db_conn: pymysql.Connection = Depends(get_db_conn), auth: bool = Depends(authenticate)):
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM todo_items")
        result = cursor.fetchall()
        todo_items = []
        for row in result:
            todo_item = TodoItem(id=row[0], title=row[1], description=row[2])
            todo_items.append(todo_item)
        return todo_items

# Create a new todo item
@app.post("/todos")
def create_todo_item(todo_item: TodoItemCreate, db_conn: pymysql.Connection = Depends(get_db_conn),
                     auth: bool = Depends(authenticate)):
    with db_conn.cursor() as cursor:
        cursor.execute("INSERT INTO todo_items (title, description) VALUES (%s, %s)",
                       (todo_item.title, todo_item.description))
        db_conn.commit()
        return {"message": "Todo item created successfully"}

# Update an existing todo item
@app.put("/todos/{item_id}")
def update_todo_item(item_id: int, todo_item: TodoItemCreate, db_conn: pymysql.Connection = Depends(get_db_conn),
                     auth: bool = Depends(authenticate)):
    with db_conn.cursor() as cursor:
        cursor.execute("UPDATE todo_items SET title = %s, description = %s WHERE id = %s",
                       (todo_item.title, todo_item.description, item_id))
        db_conn.commit()
        return {"message": f"Todo item with ID {item_id} updated successfully"}

# Delete a todo item
@app.delete("/todos/{item_id}")
def delete_todo_item(item_id: int, db_conn: pymysql.Connection = Depends(get_db_conn),
                     auth: bool = Depends(authenticate)):
    with db_conn.cursor() as cursor:
        cursor.execute("DELETE FROM todo_items WHERE id = %s", (item_id,))
        db_conn.commit()
        return {"message": f"Todo item with ID {item_id} deleted successfully"}

# if __name__ == "__main__":
#     app.run()



from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import pymysql

# Database connection settings
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'Ramesh244@'
DB_NAME = 'Todolistapi'

# Create FastAPI app instance
app = FastAPI()

# Basic authentication
security = HTTPBasic()

# Define models

class TodoItem(BaseModel):
    """
    Represents a todo item.
    """
    id: int
    title: str
    description: str

class TodoItemCreate(BaseModel):
    """
    Represents a todo item creation request.
    """
    title: str
    description: str

# Database connection dependency
def get_db_conn():
    """
    Dependency function to establish a database connection.
    """
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    return conn

# Authentication dependency
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Dependency function to perform basic authentication.
    """
    # Replace with your own authentication logic
    if credentials.username != "admin" or credentials.password != "admin":
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return True

@app.get("/todos")
def get_todo_list(db_conn: pymysql.Connection = Depends(get_db_conn), auth: bool = Depends(authenticate)):
    """
    Retrieve all todo items.

    Requires authentication.

    Returns:
        List[TodoItem]: List of todo items.
    """
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM todo_items")
        result = cursor.fetchall()
        todo_items = []
        for row in result:
            todo_item = TodoItem(id=row[0], title=row[1], description=row[2])
            todo_items.append(todo_item)
        return todo_items

@app.post("/todos")
def create_todo_item(todo_item: TodoItemCreate, db_conn: pymysql.Connection = Depends(get_db_conn),
                     auth: bool = Depends(authenticate)):
    """
    Create a new todo item.

    Requires authentication.

    Args:
        todo_item (TodoItemCreate): Todo item data.

    Returns:
        Dict[str, str]: Success message.
    """
    with db_conn.cursor() as cursor:
        cursor.execute("INSERT INTO todo_items (title, description) VALUES (%s, %s)",
                       (todo_item.title, todo_item.description))
        db_conn.commit()
        return {"message": "Todo item created successfully"}

@app.put("/todos/{item_id}")
def update_todo_item(item_id: int, todo_item: TodoItemCreate, db_conn: pymysql.Connection = Depends(get_db_conn),
                     auth: bool = Depends(authenticate)):
    """
    Update an existing todo item.

    Requires authentication.

    Args:
        item_id (int): ID of the todo item to update.
        todo_item (TodoItemCreate): Updated todo item data.

    Returns:
        Dict[str, str]: Success message.
    """
    with db_conn.cursor() as cursor:
        cursor.execute("UPDATE todo_items SET title = %s, description = %s WHERE id = %s",
                       (todo_item.title, todo_item.description, item_id))
        db_conn.commit()
        return {"message": f"Todo item with ID {item_id} updated successfully"}

@app.delete("/todos/{item_id}")
def delete_todo_item(item_id: int, db_conn: pymysql.Connection = Depends(get_db_conn),
                     auth: bool = Depends(authenticate)):
    """
    Delete a todo item.

    Requires authentication.

    Args:
        item_id (int): ID of the todo item to delete.

    Returns:
        Dict[str, str]: Success message.
    """
    with db_conn.cursor() as cursor:
        cursor.execute("DELETE FROM todo_items WHERE id = %s", (item_id,))
        db_conn.commit()
        return {"message": f"Todo item with ID {item_id} deleted successfully"}
