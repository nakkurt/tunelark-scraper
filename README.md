## tunelark-scraper

Scrapes 8000+ high schools' pages on a domain and retrieves data in a .csv or .json file.

### Installation:
  1. Fork/clone repo to your machine
  2. Follow [Scrapy installation guide](doc.scrapy.org/en/latest/intro/install.html) to install Scrapy in a [**virtual environment**](https://virtualenv.pypa.io/en/stable/installation/)
  3. Make sure the virtual environment is running
  4. In your terminal navigate to your repo's */tunelark_schools/tunelark_schools/spiders* folder
  5. To start the scraper:
     - a) for *.csv* output run this in the terminal: `scrapy runspider -o schools.csv school_list_scraper.py`
     - b) for *.json* output run this instead: `scrapy runspider -o schools.json school_list_scraper.py`
  6. Data will be in the schools.csv file 
   
  
