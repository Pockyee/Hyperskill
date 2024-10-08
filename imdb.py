import csv
import time


# Function to read movies from a CSV file.
# It returns a list of tuples where each tuple contains the movie title and rating.
def read_movies(file_name):
    movies = []
    with open(file_name, encoding="UTF-8") as file:
        reader = csv.reader(file)
        for row in reader:
            title = row[0].strip('"')
            rating = float(row[1])
            movies.append((title, rating))
    return movies


# Function to print the list of movies and their ratings.
def print_movies(movies):
    for title, rating in movies:
        print(f"{title} - {rating}")


# Linear search function to find movies with a specific rating.
# It returns a list of all movies that match the given rating.
def movie_linear_select(movies, rating):
    selection = []
    for movie in movies:
        if movie[1] == rating:
            selection.append(movie)
    return selection


# Bubble sort algorithm to sort movies based on their rating.
# It iterates through the list repeatedly, swapping adjacent elements if they are in the wrong order.
def bubble_sort(movies):
    n = len(movies)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if movies[j][1] > movies[j + 1][1]:
                movies[j], movies[j + 1] = movies[j + 1], movies[j]
                swapped = True
        if not swapped:
            break
    return movies


# Merge sort algorithm to recursively divide the movie list into two halves, sort each half, and merge them back together.
# This is an efficient sorting algorithm with a time complexity of O(n log n).
def merge_sort(movies):
    if len(movies) <= 1:
        return movies
    else:
        mid = len(movies) // 2
        left = movies[0:mid]
        right = movies[mid:]
        left_sorted = merge_sort(left)
        right_sorted = merge_sort(right)
        return merge(left_sorted, right_sorted)


# Helper function to merge two sorted lists (left and right) into a single sorted list.
def merge(left, right):
    merged = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i][1] < right[j][1]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# Binary search function to find the first occurrence of a movie with a given rating in a sorted list.
def movie_binary_first(movies, rating):
    low, high, index = 0, len(movies) - 1, 0
    while low <= high:
        mid = (low + high) // 2
        if movies[mid][1] == rating:
            index = mid
            high = (
                mid - 1
            )  # Continue searching on the left side for the first occurrence.
        elif movies[mid][1] < rating:
            low = mid + 1
        else:
            high = mid - 1
    return index


# Binary search function to find the last occurrence of a movie with a given rating in a sorted list.
def movie_binary_last(movies, rating):
    low, high, index = 0, len(movies) - 1, 0
    while low <= high:
        mid = (low + high) // 2
        if movies[mid][1] == rating:
            index = mid
            low = (
                mid + 1
            )  # Continue searching on the right side for the last occurrence.
        elif movies[mid][1] < rating:
            low = mid + 1
        else:
            high = mid - 1
    return index


# Function to select all movies with a specific rating using binary search.
# It uses two binary searches to find the first and last occurrence of the rating in the sorted list.
def movie_binary_selection(movies, rating):
    return movies[
        movie_binary_first(movies, rating) : movie_binary_last(movies, rating) + 1
    ]


# Main program execution
file_name = "movies.csv"
movies = read_movies(file_name)

# Measure the time taken to sort the movies using bubble sort.
start_time = time.time()
sorted_movies = bubble_sort(movies)
end_time = time.time()

# Use binary search to find movies with a rating of 6 from the sorted list.
matching_movies = movie_binary_selection(sorted_movies, 6)

# Print the matching movies and the time taken for sorting.
print_movies(matching_movies)
print(end_time - start_time)
