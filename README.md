# IMDb Scraper API

This project is designed to scrape IMDb data and expose it via a Django REST API. It allows fetching a list of movies, with pagination, and searching movies by their title.

## Project Setup

### Step 1: Setting up the Virtual Environment

To begin, create a Python virtual environment. Follow these steps:

1. **Create a Virtual Environment**:
    - If you're using `venv` (recommended):
      ```bash
      python3 -m venv venv
      ```

2. **Activate the Virtual Environment**:
    - **On macOS/Linux**:
      ```bash
      source venv/bin/activate
      ```
    - **On Windows**:
      ```bash
      venv\Scripts\activate
      ```

3. **Install Dependencies**:
    - Install the necessary Python packages by running the following command:
      ```bash
      pip install -r requirements.txt
      ```

### Step 2: Scraping Data

1. **Run the Scraping Script**:
    - The `script.py` file contains the logic to scrape IMDb data and save it to your Django database.
    - Run the script using the following command:
      ```bash
      python script.py
      ```

   The script will automatically fetch movie data from IMDb and store it in your Django model. Ensure you have already set up the database for the Django project before running the script.

### Step 3: Running the Django Development Server

To run the API server locally:

1. **Apply Migrations**:
    - Run the following command to apply migrations:
      ```bash
      python manage.py migrate
      ```

2. **Start the Development Server**:
    - Start the Django development server with the following command:
      ```bash
      python manage.py runserver
      ```

   Your API should now be accessible at `http://127.0.0.1:8000/`.

---

## API Endpoints

### 1. Get a List of All Movies (Paginated)

- **Endpoint**: `/movie/`
- **Method**: `GET`
- **Description**: This endpoint returns a paginated list of all movies in the database.
- **Query Parameters**:
    - `page`: The page number to retrieve (default is 1).
    - `page_size`: The number of movies per page (default is 10, configurable through `settings.py`).

- **Response Example**:
  ```json
  {
    "count": 100,
    "next": "http://127.0.0.1:8000/movie/?page=2",
    "previous": null,
    "results": [
      {
        "title": "Avengers: Endgame",
        "release_year": 2019,
        "imdb_rating": 8.4,
        "plot_summary": "The Avengers assemble once more in an attempt to undo the damage caused by Thanos.",
        "genre": "Action, Adventure, Sci-Fi"
      },
      {
        "title": "Inception",
        "release_year": 2010,
        "imdb_rating": 8.8,
        "plot_summary": "A skilled thief is given a chance at redemption if he can successfully perform an inception.",
        "genre": "Action, Adventure, Sci-Fi"
      }
    ]
  }
