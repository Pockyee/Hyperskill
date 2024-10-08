import csv


def read_movies(file_name):
    movies = []
    with open(file_name, encoding="UTF-8") as file:
        reader = csv.reader(file)
        for row in reader:
            title = row[0].strip('"')
            rating = row[1]
            movies.append((title, rating))

    return movies


def print_movies(movies):
    for title, rating in movies:
        print(f"{title} - {rating}")


file_name = "movies.csv"
movies = read_movies(file_name)
print_movies(movies)
