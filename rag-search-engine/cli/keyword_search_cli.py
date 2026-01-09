#!/usr/bin/env python3

import argparse
import json
import string

def normalize(text: str) -> str:
    table = str.maketrans("", "", string.punctuation)
    return text.lower().translate(table)

def load_stopwords():
    with open("data/stopwords.txt", "r") as f:
        return set(f.read().splitlines())

def search_movies(query):
    with open("data/movies.json", "r") as f:
        data = json.load(f)

    stopwords = load_stopwords()
    movies = data["movies"]
    results = []

    for movie in movies:
        title = movie.get("title", "")

        normalized_title = normalize(title)
        normalized_query = normalize(query)

        title_tokens = [t for t in normalized_title.split() if t and t not in stopwords]
        query_tokens = [t for t in normalized_query.split() if t and t not in stopwords]

        match_found = False
        for q in query_tokens:
            for t in title_tokens:
                if q in t:
                    match_found = True
                    break
            if match_found:
                break

        if match_found:
            results.append(movie)

    results.sort(key=lambda m: m["id"])
    results = results[:5]

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
