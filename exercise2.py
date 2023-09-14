import sqlite3

# Function to create the database and table
def create_database_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
            movieID INTEGER PRIMARY KEY,
            movieName TEXT,
            movieYear INTEGER,
            imdbRating REAL
        )
    ''')
    conn.commit()

# Function to insert data into the table
def insert_data(conn, data):
    cursor = conn.cursor()

    for movie_data in data:
        try:
            movie_year = int(movie_data[2])
            imdb_rating = float(movie_data[3])
        except ValueError:
            # Handle non-numeric values or invalid data gracefully
            continue

        cursor.execute('INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating) VALUES (?, ?, ?)',
                       (movie_data[0], movie_year, imdb_rating))

    conn.commit()

# Function to search for movies by name
def search_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieName LIKE ?', (f'%{name}%',))
    result = cursor.fetchall()
    return result

# Function to search for movies by year
def search_by_year(conn, year):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?', (year,))
    result = cursor.fetchall()
    return result

# Function to search for movies by rating
def search_by_rating(conn, rating):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?', (rating,))
    result = cursor.fetchall()
    return result

# Main program
if __name__ == "__main__":
    conn = sqlite3.connect('stephen_king_adaptations.db')
    create_database_table(conn)

    with open('stephen_king_adaptations.txt', 'r') as file:
        stephen_king_adaptations_list = [line.strip().split(',') for line in file.readlines()]

    insert_data(conn, stephen_king_adaptations_list)

    while True:
        print("Options:")
        print("1. Search by Movie Name")
        print("2. Search by Movie Year")
        print("3. Search by Movie Rating")
        print("4. STOP")
        option = input("Select an option: ")

        if option == "1":
            movie_name = input("Enter the movie name: ")
            result = search_by_name(conn, movie_name)
            if result:
                for row in result:
                    print(f"Movie Name: {row[1]}, Year: {row[2]}, Rating: {row[3]}")
            else:
                print("No such movie exists in our database.")
        elif option == "2":
            movie_year = int(input("Enter the movie year: "))
            result = search_by_year(conn, movie_year)
            if result:
                for row in result:
                    print(f"Movie Name: {row[1]}, Year: {row[2]}, Rating: {row[3]}")
            else:
                print("No movies were found for that year in our database.")
        elif option == "3":
            movie_rating = float(input("Enter the minimum rating: "))
            result = search_by_rating(conn, movie_rating)
            if result:
                for row in result:
                    print(f"Movie Name: {row[1]}, Year: {row[2]}, Rating: {row[3]}")
            else:
                print("No movies at or above that rating were found in the database.")
        elif option == "4":
            conn.close()
            break
        else:
            print("Invalid option. Please choose a valid option.")
