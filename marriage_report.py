import sqlite3
import pandas as pd

def main():
    
    con = sqlite3.connect('social_network.db')
    cur = con.cursor()

   
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='people';")
    if not cur.fetchone():
        print("The 'people' table does not exist. Exiting.")
        return

  
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='relationships';")
    if not cur.fetchone():
        print("The 'relationships' table does not exist.")
        return

    
    all_relationships_query = """
    SELECT person1.name AS person1_name, person2.name AS person2_name, relationships.start_date, relationships.type
    FROM relationships
    JOIN people person1 ON relationships.person1_id = person1.id
    JOIN people person2 ON relationships.person2_id = person2.id;
    """

    
    cur.execute(all_relationships_query)
    all_relationships = cur.fetchall()

    
    if not all_relationships:
        print("No relationships found.")
    else:
        print("All relationships in the database:")
        for relationship in all_relationships:
            print(f"{relationship[0]} is a {relationship[3]} of {relationship[1]} since {relationship[2]}.")

    
    married_couples_query = """
    SELECT person1.name AS person1_name, person2.name AS person2_name, relationships.start_date
    FROM relationships
    JOIN people person1 ON relationships.person1_id = person1.id
    JOIN people person2 ON relationships.person2_id = person2.id
    WHERE relationships.type = 'spouse';
    """

    
    cur.execute(married_couples_query)
    married_couples = cur.fetchall()

    
    if not married_couples:
        print("No married couples found.")
    else:
       
        married_couples_df = pd.DataFrame(married_couples, columns=['Person 1', 'Person 2', 'Start Date'])

       
        married_couples_df.to_csv('married_couples_report.csv', index=False)
        print("Generated report for married couples")

    con.close()

if __name__ == "__main__":
    main()
