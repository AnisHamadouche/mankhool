from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.templating import Jinja2Templates
import json
import os
from elasticsearch import Elasticsearch

def index_books(directory="./books"):
    es = Elasticsearch("http://localhost:9200")  # Default connection URL
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            path = os.path.join(directory, filename)
            with open(path, 'r', encoding='utf-8') as file:
                book_data = json.load(file)
            book_id = filename[:-5]  # Assuming the filename is "book_id.json"
            # Index each book
            es.index(index="books", id=book_id, document=book_data)
            print(f"Indexed {book_id}")


# def search_books(query, directory="./books"):
#     """Search for a query across all books' pages."""
#     results = []
#     query = query.lower()  # Lowercase the query for case-insensitive search
#     for filename in os.listdir(directory):
#         if filename.endswith(".json"):
#             path = os.path.join(directory, filename)
#             with open(path, 'r', encoding='utf-8') as file:
#                 book_data = json.load(file)
#             book_id = filename.split('_')[1].split('.')[0]  # Extract book ID
#             # Search for the query in each page of the book
#             for chapter in book_data.get("chapters", []):
#                 for page in chapter.get("pages", []):
#                     if query in page.get("text", "").lower():
#                         results.append({
#                             "id": book_id,
#                             "title": book_data.get("title", "No Title"),
#                             "chapter": chapter.get("chapterTitle", "No Chapter Title"),
#                             "text_preview": page.get("text", "")[:150]  # Preview of the text
#                         })
#                         break  # Optionally break after the first match in each book
#     return results


def search_books(query):
    es = Elasticsearch("http://localhost:9200")
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "chapters.pages.text"]
            }
        }
    }
    results = es.search(index="books", body=body)
    return results['hits']['hits']


def list_books(directory="./books"):
    """List all books in the given directory."""
    books = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            book_id = filename.split('_')[1].split('.')[0]  # Extract book ID from filename, assumes format 'book_ID.json'
            path = os.path.join(directory, filename)
            with open(path, 'r', encoding='utf-8') as file:
                book_data = json.load(file)
            books.append({
                "id": book_id,
                "title": book_data.get("title", "No Title")
            })
    return books

app = FastAPI()
templates = Jinja2Templates(directory="./templates")

# @app.get("/")
# async def homepage(request: Request, query: str = None):
#     books = list_books()  # Get list of books
#     search_results = []
#     if query:
#         search_results = search_books(query)  # Perform search if query is present
#     return templates.TemplateResponse("homepage.html", {
#         "request": request,
#         "books": books,
#         "search_results": search_results
#     })

@app.get("/")
async def homepage(request: Request, query: str = None):
    books = list_books()  # List of books
    search_results = []
    if query:
        search_results = search_books(query)  # Search using Elasticsearch
    return templates.TemplateResponse("homepage.html", {
        "request": request,
        "books": books,
        "search_results": search_results
    })


@app.get("/books/{book_id}/")
async def read_book_page(request: Request, book_id: int, chapter: int = Query(0), page: int = Query(0)):
    try:
        with open(f'books/book_{book_id}.json', 'r') as file:
            book_data = json.load(file)
        
        # Check and update next_page and previous_page with continuity across chapters
        if page + 1 < len(book_data['chapters'][chapter]['pages']):
            next_page = page + 1
            next_chapter = chapter
        else:
            if chapter + 1 < len(book_data['chapters']):
                next_page = 0
                next_chapter = chapter + 1
            else:
                next_page = None
                next_chapter = None
        
        if page > 0:
            previous_page = page - 1
            previous_chapter = chapter
        else:
            if chapter > 0:
                previous_chapter = chapter - 1
                previous_page = len(book_data['chapters'][previous_chapter]['pages']) - 1
            else:
                previous_page = None
                previous_chapter = None

        page_data = book_data['chapters'][chapter]['pages'][page]
        return templates.TemplateResponse("page_viewer.html", {
            "request": request,
            "book_data": book_data,
            "page_data": page_data,
            "next_page": next_page,
            "previous_page": previous_page,
            "chapter_index": chapter,
            "next_chapter": next_chapter,
            "previous_chapter": previous_chapter
        })
    except IndexError:
        raise HTTPException(status_code=404, detail="Page not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")

