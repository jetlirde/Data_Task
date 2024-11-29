import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import os
import re




def insert_data_to_db(destination, data):
    conn = sqlite3.connect('vikings.db')
    cursor = conn.cursor()

    
    if destination == 'vikings_cast':
        source_name = 'Vikings TV Series'
    elif destination == 'norsemen_characters':
        source_name = 'Norsemen TV Series'
    elif destination == 'vikings_nfl_roster':
        source_name = 'Vikings NFL Team'
    else:
        print(f"Unknown table name: {table_name}")
        return
    
    
    cursor.execute('''
    SELECT id FROM sources WHERE name = ?
    ''', (source_name,))
    source_id = cursor.fetchone()
    
    if source_id:
        source_id = source_id[0]
    else:
        
        print(f"Source '{source_name}' not found! Skipping characters from this source.")
        return

    
    for character in data:
        cursor.execute('''
        INSERT OR IGNORE INTO characters (name, description, actor, photo_url, source_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (character['name'], character['description'], character.get('actor', 'Unknown'), character['photo_url'], source_id))
    
    conn.commit()
    conn.close()


def scrape_vikings_cast():
    url = "https://www.history.com/shows/vikings/cast"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    characters = []
    
    cast_elements = soup.find_all('li')

    for cast in cast_elements:
        
        name_tag = cast.find('strong')
        description_tag = cast.find('small')
        image_tag = cast.find('img')
        
        if not name_tag:
            continue

        name = name_tag.text.strip() if name_tag else 'Unknown'
        
        actor_text = description_tag.text.strip() if description_tag else 'Unknown'
        actor_match = re.search(r"Played by (.+)", actor_text)
        actor = actor_match.group(1) if actor_match else 'Unknown'

        photo_url = image_tag['src'] if image_tag else 'No image'

        description = description_tag.text.strip() if description_tag else 'No description available'
        photo_url = image_tag['src'] if image_tag else 'No image'

        characters.append({
            'name': name,
            'actor': actor,
            'description': description,
            'photo_url': photo_url
        })
    
    return characters


vikings_cast = scrape_vikings_cast()









def scrape_norsemen_characters():
    url = "https://www.imdb.com/title/tt5905354/fullcredits/?ref_=tt_cst_sm"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    characters = []
    cast_table = soup.find_all('table', class_='cast_list')
    
    for table in cast_table:      
        rows = table.find_all('tr')
        
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 3:
                character_details = cols[3].find_all('a')
                name = character_details[0].text.strip()
                description = character_details[1].text.strip()
                
                actor = cols[1].text.strip()
                
                photo_url = cols[0].find('img')
                if photo_url.has_attr('loadlate'):
                    photo_url = photo_url['loadlate']
                else:
                    photo_url = photo_url['src']
                
                characters.append({
                    'name': name,
                    'actor': actor,
                    'description': description,
                    'photo_url': photo_url
                    
                })
    
    return characters


norsemen_characters = scrape_norsemen_characters()

insert_data_to_db('vikings_cast', vikings_cast)
insert_data_to_db('norsemen_characters', norsemen_characters)




def run_pipeline():
    print("Running the scraping pipeline...")
    

    vikings_cast = scrape_vikings_cast()
    if vikings_cast:
        insert_data_to_db('vikings_cast', vikings_cast)

    
    norsemen_characters = scrape_norsemen_characters()
    if norsemen_characters:
        insert_data_to_db('norsemen_characters', norsemen_characters)


schedule.every().day.at("03:00").do(run_pipeline)


while True:
    schedule.run_pending()
    time.sleep(1)
