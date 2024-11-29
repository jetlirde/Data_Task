import streamlit as st
import sqlite3


def get_data(query, params=()):
    conn = sqlite3.connect('vikings.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


if 'selected_character' not in st.session_state:
    st.session_state.selected_character = None

if 'search_query' not in st.session_state:
    st.session_state.search_query = ""


def show_character_list():
    
    st.title("Viking Characters")

    
    search_query = st.text_input("Search characters:", value=st.session_state.search_query)

    
    st.session_state.search_query = search_query

    
    if search_query:
        query = "SELECT * FROM characters WHERE name LIKE ? OR description LIKE ?"
        characters = get_data(query, (f'%{search_query}%', f'%{search_query}%'))
    else:
        characters = get_data("SELECT * FROM characters")

    
    num_cols = 3  
    cols = st.columns(num_cols)

    for i, character in enumerate(characters):
        with cols[i % num_cols]:  
            st.image(character[4], width=150)  
            st.subheader(character[1])  
            st.write(f"**Played by**: {character[3]}")  
            st.write(character[2])  

            if st.button(f"View details for {character[1]}",character[0]):
                st.session_state.selected_character = character[0]
                st.rerun()  

def show_character_details():
    character_id = st.session_state.selected_character
    if character_id:
        character_details = get_data("SELECT * FROM characters WHERE id=?", (character_id,))
        if character_details:
            char = character_details[0]
            st.title(f"Details for {char[1]}")
            st.image(char[4], width=300)
            st.write(f"**Name**: {char[1]}")
            st.write(f"**Description**: {char[2]}")
            st.write(f"**Actor**: {char[3]}")

            
            if st.button("Back to character list"):
                st.session_state.selected_character = None
                st.rerun()
    else:
        st.warning("No character selected. Please go back and select a character.")


if st.session_state.selected_character:
    show_character_details()
else:

    show_character_list()
