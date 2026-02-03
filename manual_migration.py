#!/usr/bin/env python
"""Direct SQL migration for adding created_at and updated_at to Product"""
import os
import sqlite3
from datetime import datetime

# Get database path
db_path = 'd:\\web\\FashioHub\\db.sqlite3'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(Hub_product)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'created_at' not in columns:
            print("Adding created_at column...")
            now = datetime.now().isoformat()
            cursor.execute(f"ALTER TABLE Hub_product ADD COLUMN created_at DATETIME DEFAULT '{now}'")
            print("✓ created_at added")
        else:
            print("✓ created_at already exists")
        
        if 'updated_at' not in columns:
            print("Adding updated_at column...")
            now = datetime.now().isoformat()
            cursor.execute(f"ALTER TABLE Hub_product ADD COLUMN updated_at DATETIME DEFAULT '{now}'")
            print("✓ updated_at added")
        else:
            print("✓ updated_at already exists")
        
        conn.commit()
        print("\n✓ Migration completed successfully!")
    except Exception as e:
        print(f"✗ Error: {e}")
        conn.rollback()
    finally:
        conn.close()
else:
    print(f"Database not found at {db_path}")
