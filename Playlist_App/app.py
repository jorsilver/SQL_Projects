#imports
from helper import helper
from db_operations import db_operations

#global variables
db_ops = db_operations("/Users/jordansilver1/Documents/CPSC_Courses/CPSC_408/Projects/SQLite_DBs/playlist.db")

#functions
def startScreen():
    print("Welcome to your playlist!")
    #db_ops.create_songs_table()
    db_ops.populate_songs_table("songs.csv")

#show user menu options
def options():
    print('''Select from the following menu options: 
    1. Find songs by artist
    2. Find songs by genre
    3. Find songs by feature
    4. Load new songs
    5. Update song information
    6. Delete song
    7. Delete all songs with null attributes
    8. Exit''')
    return helper.get_choice([1,2,3,4,5,6,7,8])

#search for songs by artist
def search_by_artist():
    #get list of all artists in table
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist: ")
    artists = db_ops.single_attribute(query)

    #show all artists, create dictionary of options, and let user choose
    choices = {}
    for i in range(len(artists)):
        print(i, artists[i])
        choices[i] = artists[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Artist =:artist ORDER BY RANDOM()
    '''
    dictionary = {"artist":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#search songs by genre
def search_by_genre():
    #get list of genres
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist:")
    genres = db_ops.single_attribute(query)

    #show genres in table and create dictionary
    choices = {}
    for i in range(len(genres)):
        print(i, genres[i])
        choices[i] = genres[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Genre =:genre ORDER BY RANDOM()
    '''
    dictionary = {"genre":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#search songs table by features
def search_by_feature():
    #features we want to search by
    features = ['Danceability', 'Liveness', 'Loudness']
    choices = {}

    #show features in table and create dictionary
    choices = {}
    for i in range(len(features)):
        print(i, features[i])
        choices[i] = features[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #what order does the user want this returned in?
    print("Do you want results sorted in asc or desc order?")
    order = input("ASC or DESC: ")

    #print results
    query = "SELECT DISTINCT name FROM songs ORDER BY "+choices[index]+" "+order
    dictionary = {}
    if num != 0:
        query +=" LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#add new songs from a csv file to the playlist
def load_new_songs():
    filepath = input("Enter the location of the file containing new songs: \n")
    data = helper.data_cleaner(filepath)
    attribute_count = len(data[0])
    placeholders = ("?,"*attribute_count)[:-1]
    query = "INSERT INTO songs VALUES("+placeholders+")"
    db_ops.bulk_insert(query, data)
    print("Songs added successfuly")

#Update an attribute for a song in the playlist
def update_song_info():
    #get the name of a song to update
    song_name = input("Enter the name of the song you want to update:\n")
    query = '''
    SElECT *
    FROM songs
    WHERE Name =:name
    '''
    #get the list of attributes for the specified song
    song_info = db_ops.select_query_params(query, {"name": song_name})
    
    #check that the song exists
    if not song_info:
        print("Song not found.")
        return
    
    #map modifiable attributes to their index in song_info[0]
    modifiable_attributes = {1: "Name", 2: "Artist", 3: "Album", 4: "releaseDate", 6: "Explicit"}

    #print all the attributes for the song
    print(f"\nAttributes for {song_name} by {song_info[0][2]}\n(N/M -> Not Modifiable)\n")
    for i, attribute_value in enumerate(song_info[0]):
        if i in modifiable_attributes.keys():#current attribute is modifiable
            print(f"{i}.) {modifiable_attributes[i]}: {attribute_value}")
        else:
            print(f"N/M: {attribute_value}")

    #get the attribute to modify        
    index = helper.get_choice(modifiable_attributes.keys())#attribute to be modified

    #get the new value for the selected attribute
    new_value = input(f"Enter new value for {modifiable_attributes[index]}:\n")
    query = f'''
    UPDATE songs
    SET {modifiable_attributes[index]} =:newValue
    WHERE songID =:songID
    '''
    db_ops.modify_query_params(query, {"newValue": new_value, "songID": song_info[0][0]})

    #tell the user the operation was completed successfuly
    print(f"{modifiable_attributes[index]} updated successfully.")

#delete a song from the playlist
def delete_song():
    #get the name of the song to delete
    song_name = input("Enter the name of the song you want to delete:\n")
    query = '''
    SElECT songID
    FROM songs
    WHERE Name =:name
    '''
    song_ID = db_ops.single_record_params(query, {"name": song_name})
    #check that the song exists
    if not song_ID:
        print("Song not found.")
        return
    
    query = '''
    DELETE FROM songs
    WHERE songID =:songid
    '''
    #commit the query
    db_ops.modify_query_params(query, {"songid": song_ID})

    #tell the user the operation was completed successfuly
    print(f"{song_name} deleted successfully.")

#delete all songs from the playlist with at least one null attribute value
def delete_all_with_null_attr():
    schema = db_ops.select_query("PRAGMA table_info(songs);")
    attributes = [attribute[1] for attribute in schema]
    query = '''
    DELETE FROM songs
    WHERE '''
    for i, attribute in enumerate(attributes):
        query += attribute + " IS NULL"
        if i < len(attributes) - 1: query += "\n    OR "
    db_ops.modify_query(query)
    print("All songs with null attributes deleted successfully.")

#main method
startScreen()

#program loop
while True:
    user_choice = options()
    if user_choice == 1:
        search_by_artist()
    if user_choice == 2:
        search_by_genre()
    if user_choice == 3:
        search_by_feature()
    if user_choice == 4:
        load_new_songs()
    if user_choice == 5:
        update_song_info()
    if user_choice == 6:
        delete_song()
    if user_choice == 7:
        delete_all_with_null_attr()
    if user_choice == 8:
        print("Goodbye!")
        break

db_ops.destructor()