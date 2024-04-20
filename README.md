# Mankhool FastAPI Web Application

Mankhool is a FastAPI web application designed to provide a robust search and book reading interface with integrated Elasticsearch for enhanced searching capabilities across multiple book documents. This guide will walk you through the setup and running of the Mankhool application.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.6 or higher
- pip (Python package installer)
- Elasticsearch 7.x

Elasticsearch should be running on localhost and default port (9200). Refer to the [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html) for installation instructions.

## Installation

Follow these steps to get your development environment running:

### 1. Clone the Repository

Start by cloning the repository to your local machine. To do this, run the following command in your terminal:

```bash
git clone <repository-url>
cd Mankhool
```

Replace `<repository-url>` with the URL of the repository.

### 2. Set Up a Python Virtual Environment

It's recommended to use a virtual environment to manage dependencies for your project. Create and activate a virtual environment by running:

```bash
python -m venv venv
source venv/bin/activate  # Unix/Linux/MacOS
venv\Scripts\activate  # Windows
```

### 3. Install Required Python Packages

Install all required packages using the `requirements.txt` file with pip:

```bash
pip install -r requirements.txt
```

### 4. Index Books into Elasticsearch

Before running the application, make sure to index your book data into Elasticsearch. Execute the indexing script if provided, or use the following Python snippet to index:

```python
# Assuming you have a function `index_books()` in main.py
from main import index_books
index_books()
```

Make sure your book JSON files are placed in the appropriate directory as expected by the script.

## Running the Application

With all dependencies installed and Elasticsearch running, you can start the FastAPI application by running:

```bash
uvicorn main:app --reload
```

This command starts the application with live reloading enabled, making it suitable for development.

## Accessing the Application

Open your web browser and navigate to `http://localhost:8000/` to access the Mankhool application. You can browse books, search for keywords, and read book content.

## Troubleshooting

If you encounter issues with starting the application or other operational challenges:
- Ensure that Elasticsearch is running and accessible.
- Check that all dependencies are correctly installed in the virtual environment.
- Verify the network settings if you cannot access the application at `localhost:8000`.

## Author

**Name**: Anis Hamadouche أنيس حمادوش

**Role**: Data Engineer & Solutions Architect

**Email**: a.hamadouche.igee@gmail.com

For further inquiries or assistance, feel free to contact the author via email.
