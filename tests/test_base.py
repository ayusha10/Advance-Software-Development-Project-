import unittest
import sqlite3
import os
import uuid

class RepositoryTestCase(unittest.TestCase):
    def setUp(self):
        # Use a unique file for each test method
        self.test_db = f"test_db_{uuid.uuid4().hex}.sqlite3"
        os.environ["DB_PATH"] = self.test_db
        
        # Create schema
        conn = sqlite3.connect(self.test_db)
        with open("horizon_db.sql", "r") as f:
            sql = f.read()
            conn.executescript(sql)
        conn.close()

    def tearDown(self):
        # Clear environment variable
        if "DB_PATH" in os.environ:
            del os.environ["DB_PATH"]
        
        # Cleanup file
        try:
            import time
            time.sleep(0.2)
            if os.path.exists(self.test_db):
                os.remove(self.test_db)
                # Cleanup WAL files too
                for suffix in ['-shm', '-wal']:
                    if os.path.exists(self.test_db + suffix):
                        os.remove(self.test_db + suffix)
        except:
            pass
