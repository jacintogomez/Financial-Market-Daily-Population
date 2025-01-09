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
3. Add in `.env` file with variables specified in `.env.template`
4. Apply migrations if necessary `python manage.py migrate`
5. Run app `python manage.py runserver` and open on localhost


Steps to set up async and webhook:
1. Start Redis broker to accept async tasks `redis-server`
2. Start Celery worker to handle async tasks `celery -A stock_api_backend worker --loglevel=info -P threads --concurrency=8`
3. Start Celery beat for daily re-run tasks `celery -A stock_api_backend beat --loglevel=info`
4. Start local ngrok server `ngrok http 8000`
3. Start Zookeeper `bin/zookeeper-server-start.sh config/zookeeper.properties`
4. Start Kafka `bin/kafka-server-start.sh config/server.properties`
5. Check Kafka messages `bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic market_data --from-beginning`
