"""
User Authentication and Management
"""
import sqlite3
import hashlib
import secrets
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from src.my_personal_agent.config import settings


class UserManager:
    """Manage user authentication and sessions"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.database_path
        self._init_database()
    
    def _init_database(self):
        """Initialize user database"""
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                api_keys TEXT,
                preferences TEXT
            )
        """)
        
        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_user(
        self,
        username: str,
        password: str,
        email: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new user"""
        user_id = secrets.token_urlsafe(16)
        password_hash = self._hash_password(password)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users (id, username, email, password_hash)
                VALUES (?, ?, ?, ?)
            """, (user_id, username, email, password_hash))
            
            conn.commit()
            
            return {
                "user_id": user_id,
                "username": username,
                "email": email,
                "created_at": datetime.now().isoformat(),
            }
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Username or email already exists: {e}")
        finally:
            conn.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, password_hash
            FROM users
            WHERE username = ?
        """, (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
        
        user_id, db_username, email, password_hash = result
        
        if not self._verify_password(password, password_hash):
            return None
        
        # Update last login
        self._update_last_login(user_id)
        
        return {
            "user_id": user_id,
            "username": db_username,
            "email": email,
        }
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, created_at, last_login
            FROM users
            WHERE id = ?
        """, (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
        
        return {
            "user_id": result[0],
            "username": result[1],
            "email": result[2],
            "created_at": result[3],
            "last_login": result[4],
        }
    
    def create_session(self, user_id: str, expiration_hours: int = 24) -> str:
        """Create a new session"""
        session_id = secrets.token_urlsafe(32)
        
        from datetime import timedelta
        expires_at = datetime.now() + timedelta(hours=expiration_hours)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sessions (session_id, user_id, expires_at)
            VALUES (?, ?, ?)
        """, (session_id, user_id, expires_at.isoformat()))
        
        conn.commit()
        conn.close()
        
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[str]:
        """Validate session and return user_id"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, expires_at
            FROM sessions
            WHERE session_id = ?
        """, (session_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
        
        user_id, expires_at_str = result
        expires_at = datetime.fromisoformat(expires_at_str)
        
        if datetime.now() > expires_at:
            # Session expired
            self.delete_session(session_id)
            return None
        
        return user_id
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        
        conn.commit()
        conn.close()
    
    def _hash_password(self, password: str) -> str:
        """Hash a password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password"""
        return self._hash_password(password) == password_hash
    
    def _update_last_login(self, user_id: str):
        """Update last login timestamp"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users
            SET last_login = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (user_id,))
        
        conn.commit()
        conn.close()

