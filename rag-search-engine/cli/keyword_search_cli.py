#!/usr/bin/env python3

import argparse
import json
import string

def normalize(text: str) -> str:
    table = str.maketrans("", "", string.punctuation)
    return text.lower().translate(table)

def search_movies(query):
    with open("data/movies.json", "r") as f:
        data = json.load(f)

    movies = data["movies"]
    results = []

    # Collect matches
    for movie in movies:
        title = movie.get("title", "")
        if normalize(query) in normalize(title):
            results.append(movie)
        if query.lower() in title.lower():   # case-sensitive substring
            results.append(movie)

    # Sort by id ascending
    results.sort(key=lambda m: m["id"])

    # Limit to 5
    results = results[:5]

    # Print output
    print(f"Searching for: {query}")
    for i, movie in enumerate(results, start=1):
        print(f"{i}. {movie['title']}")

def main():
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command")

    search_parser = subparsers.add_parser("search", help="Search movies")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    if args.command == "search":
        search_movies(args.query)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
