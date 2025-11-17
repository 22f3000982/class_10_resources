"""
Migration script to remove view_count column from resources table
Run this once to update your existing database
"""
import sqlite3
import os

def migrate_database():
    db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print("No database found. Skipping migration.")
        return
    
    print("Starting migration to remove view_count column...")
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        # Check if view_count column exists
        c.execute("PRAGMA table_info(resources)")
        columns = c.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'view_count' not in column_names:
            print("view_count column already removed. No migration needed.")
            conn.close()
            return
        
        print("Creating new resources table without view_count...")
        
        # Create new table without view_count
        c.execute('''CREATE TABLE IF NOT EXISTS resources_new
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      link TEXT,
                      filename TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        # Copy data from old table to new table (excluding view_count)
        c.execute('''INSERT INTO resources_new (id, name, link, filename, created_at)
                     SELECT id, name, link, filename, created_at FROM resources''')
        
        # Drop old table
        c.execute('DROP TABLE resources')
        
        # Rename new table to resources
        c.execute('ALTER TABLE resources_new RENAME TO resources')
        
        conn.commit()
        print("Migration completed successfully!")
        print("view_count column has been removed from the resources table.")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        raise
    
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
