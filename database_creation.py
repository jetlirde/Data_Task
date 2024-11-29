import sqlite3

def setup_database():
    conn = sqlite3.connect('vikings.db')
    cursor = conn.cursor()
    
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        actor TEXT,
        photo_url TEXT,
        source_id INTEGER,
        FOREIGN KEY (source_id) REFERENCES sources(id),
        UNIQUE(name, source_id) 
    )
    ''')
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            year INTEGER
        )
    ''')
    
    
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_character_name ON characters(name)
    ''')
    
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_source_name ON sources(name)
    ''')

    
    sources_data = [
        ('Vikings TV Series', 'A historical drama based on Viking legends.', '2013'),
        ('Norsemen TV Series', 'A Norwegian comedy series set in the Viking Age.', '2016'),
        ('Vikings NFL Team', 'The NFL team based in Minnesota.', '2021')
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO sources (name, description, year) VALUES (?, ?, ?)
    ''', sources_data)
    
    conn.commit()
    conn.close()


setup_database()
