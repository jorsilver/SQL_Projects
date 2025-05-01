Assignment 4: Playlist App
Jordan Silver
2352988
jorsilver@chapman.edu
CPSC-408-01

Description: 
    Updates were made to the playlist application to allow users to:
        Add new songs from a csv file to the playlist
        Update an attribute for a song in the playlist
        Delete a song from the playlist
        Delete all songs from the playlist with at least one null attribute value

Source Files:
    app.py
    db_operations.py
    helper.py

References:
    Class slides
    https://stackoverflow.com/questions/947215/how-to-get-a-list-of-column-names-on-sqlite3-database
    
Errors:
    Only after calling delete_all_with_null_attr(), calling search_by_artist or gernre or feature crashes the program
    
Terminal instructions:
    ./app.py