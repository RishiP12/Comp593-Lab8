import sqlite3
from random import randint, choice
from faker import Faker

def main():
    
    con = sqlite3.connect('social_network.db')
    cur = con.cursor()

    
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='people';")
    if not cur.fetchone():
        print("The 'people' table does not exist in the database. Exiting.")
        return

    
    create_relationships_tbl_query = """
    CREATE TABLE IF NOT EXISTS relationships
    (
        id INTEGER PRIMARY KEY,
        person1_id INTEGER NOT NULL,
        person2_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        start_date DATE NOT NULL,
        FOREIGN KEY (person1_id) REFERENCES people (id),
        FOREIGN KEY (person2_id) REFERENCES people (id)
    );
    """
    
    cur.execute(create_relationships_tbl_query)
    con.commit()
    print("Created 'relationships' table.")

    
    add_relationship_query = """
    INSERT INTO relationships
    (
        person1_id,
        person2_id,
        type,
        start_date
    )
    VALUES (?, ?, ?, ?);
    """

    fake = Faker()

    
    for _ in range(100):
        
        person1_id = randint(1, 200)
        
        person2_id = randint(1, 200)
        while person2_id == person1_id:
            person2_id = randint(1, 200)

        
        rel_type = choice(('friend', 'spouse', 'partner', 'relative'))

        
        start_date = fake.date_between(start_date='-50y', end_date='today')

        
        new_relationship = (person1_id, person2_id, rel_type, start_date)

        
        cur.execute(add_relationship_query, new_relationship)

    con.commit()
    con.close()
    print("Inserted 100 fake relationships into the 'relationships' table.")

if __name__ == "__main__":
    main()
