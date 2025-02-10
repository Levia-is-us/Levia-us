import os
import pymysql
from dbutils.pooled_db import PooledDB
from typing import Optional, List
import logging
from dotenv import load_dotenv


class MySQLPool:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLPool, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'pool'):
            self._load_config()
            self._create_pool()

    def _load_config(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.path.join(project_root, '.env')
        load_dotenv(env_path)
        
        self.environment = os.getenv('ENVIRONMENT', 'prod')
        if self.environment == 'local':
            return
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'max_connections': int(os.getenv('DB_MAX_CONNECTIONS', 10)),
            'min_cached': int(os.getenv('DB_MIN_CACHED', 5))
        }
        
        # Validate required configuration
        missing_vars = [k for k, v in self.config.items() if v is None]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    def _create_pool(self):
        if self.environment == 'local':
            logging.info("Running in local environment, database pool not created")
            return
            
        try:
            self.pool = PooledDB(
                creator=pymysql,
                maxconnections=self.config['max_connections'],
                mincached=self.config['min_cached'],
                blocking=True,
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                port=self.config['port'],
                charset='utf8mb4',
                autocommit=True
            )
            logging.info("Successfully initialized MySQL connection pool")
        except Exception as e:
            logging.error(f"Failed to initialize MySQL connection pool: {e}")
            raise

    def _check_environment(self, operation_name: str) -> bool:
        """Check if database operations should be executed based on environment"""
        if self.environment == 'local':
            logging.info(f"Running in local environment, skipping {operation_name}")
            return False
        return True

    def execute(self, sql: str, params: Optional[tuple] = None) -> int:
        if not self._check_environment("execute"):
            return 0
            
        conn = None
        cursor = None
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()
            if params:
                result = cursor.execute(sql, params)
            else:
                result = cursor.execute(sql)
            conn.commit()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Failed to execute SQL: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def query_one(self, sql: str, params: Optional[tuple] = None) -> Optional[tuple]:
        if not self._check_environment("query_one"):
            return None
            
        conn = None
        cursor = None
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            return cursor.fetchone()
        except Exception as e:
            logging.error(f"Failed to query database: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def query_all(self, sql: str, params: Optional[tuple] = None) -> List[tuple]:
        if not self._check_environment("query_all"):
            return []
            
        conn = None
        cursor = None
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Failed to query database: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def executemany(self, sql: str, params: List[tuple]) -> int:
        if not self._check_environment("executemany"):
            return 0
            
        conn = None
        cursor = None
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()
            result = cursor.executemany(sql, params)
            conn.commit()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Failed to execute batch SQL: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()