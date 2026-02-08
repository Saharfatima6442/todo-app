from typing import Dict, List, Optional
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from src.models.todo import Todo
import os
from datetime import datetime

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/dbname")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    owner_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# Create tables
Base.metadata.create_all(bind=engine)


class DatabaseStorageService:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_todo(self, todo_data: Todo) -> Todo:
        """Create a new todo item in the database"""
        from uuid import uuid4
        
        db = self.SessionLocal()
        try:
            todo_id = str(uuid4())
            
            db_todo = TodoDB(
                id=todo_id,
                title=todo_data.title,
                description=todo_data.description,
                completed=todo_data.completed,
                owner_id=todo_data.owner_id
            )
            
            db.add(db_todo)
            db.commit()
            db.refresh(db_todo)
            
            # Convert DB model back to Pydantic model
            return Todo(
                id=db_todo.id,
                title=db_todo.title,
                description=db_todo.description,
                completed=db_todo.completed,
                owner_id=db_todo.owner_id,
                created_at=db_todo.created_at
            )
        finally:
            db.close()

    def get_todo_by_id(self, todo_id: str, owner_id: str) -> Optional[Todo]:
        """Get a todo by ID for a specific owner from the database"""
        db = self.SessionLocal()
        try:
            db_todo = db.query(TodoDB).filter(
                TodoDB.id == todo_id,
                TodoDB.owner_id == owner_id
            ).first()
            
            if db_todo:
                return Todo(
                    id=db_todo.id,
                    title=db_todo.title,
                    description=db_todo.description,
                    completed=db_todo.completed,
                    owner_id=db_todo.owner_id,
                    created_at=db_todo.created_at
                )
            return None
        finally:
            db.close()

    def get_todos_by_owner(self, owner_id: str) -> List[Todo]:
        """Get all todos for a specific owner from the database"""
        db = self.SessionLocal()
        try:
            db_todos = db.query(TodoDB).filter(TodoDB.owner_id == owner_id).all()
            
            return [
                Todo(
                    id=db_todo.id,
                    title=db_todo.title,
                    description=db_todo.description,
                    completed=db_todo.completed,
                    owner_id=db_todo.owner_id,
                    created_at=db_todo.created_at
                )
                for db_todo in db_todos
            ]
        finally:
            db.close()

    def update_todo(self, todo_id: str, owner_id: str, update_data: dict) -> Optional[Todo]:
        """Update a todo if it belongs to the owner"""
        db = self.SessionLocal()
        try:
            # Find the todo that belongs to the owner
            db_todo = db.query(TodoDB).filter(
                TodoDB.id == todo_id,
                TodoDB.owner_id == owner_id
            ).first()
            
            if not db_todo:
                return None
            
            # Update the todo with new values
            for field, value in update_data.items():
                if hasattr(db_todo, field) and value is not None:
                    setattr(db_todo, field, value)
            
            db.commit()
            db.refresh(db_todo)
            
            # Convert DB model back to Pydantic model
            return Todo(
                id=db_todo.id,
                title=db_todo.title,
                description=db_todo.description,
                completed=db_todo.completed,
                owner_id=db_todo.owner_id,
                created_at=db_todo.created_at
            )
        finally:
            db.close()

    def delete_todo(self, todo_id: str, owner_id: str) -> bool:
        """Delete a todo if it belongs to the owner"""
        db = self.SessionLocal()
        try:
            # Find the todo that belongs to the owner
            db_todo = db.query(TodoDB).filter(
                TodoDB.id == todo_id,
                TodoDB.owner_id == owner_id
            ).first()
            
            if not db_todo:
                return False
            
            db.delete(db_todo)
            db.commit()
            return True
        finally:
            db.close()


# Global instance
db_storage_service = DatabaseStorageService()