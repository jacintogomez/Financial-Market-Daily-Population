# Stock Market API Backend

What does this do? 
- When running locally and visiting endpoint url/api/<stock_ticker> will return live data on the specified stock\
- Endpoint url/api/<stock_name>/<provider> will retrieve the data from a specific API provider, and update the database with current stock pricing info
- Endpoint url/api/stocks will return all stored data in our database

Structure: \
Django application connected to MongoDB database

Steps to run locally:
1. cd into the `stock_api_backend` folder
2. Install dependencies `pip install -r requirements.txt`
3. Apply migrations if necessary `python manage.py migrate` 
4. Run app `python manage.py runserver` and open on localhost