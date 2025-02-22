# Stock Market API Backend

What does this do? 
- Reload our DB with all market data from the APIs FMP and EOD once per day.
- Uses 8 concurrent threads during API data collection and DB population tasks for significant reduction in time.

Steps to run locally:
1. cd into the `stock_api_backend` folder
2. Install dependencies `pip install -r requirements.txt`
3. Add in `.env` file with variables specified in `.env.template`
4. Apply migrations if necessary `python manage.py migrate`
5. Build Docker images `docker-compose build`
6. Start Docker containers `docker-compose up`

Steps to set things up manually (via terminal):
1. Run app `python manage.py runserver` and open on localhost
2. Start Redis broker to accept async tasks `redis-server` (run `redis-cli shutdown` if an error pops up that a background redis server is already running)
3. Start Celery worker to handle async tasks `celery -A stock_api_backend worker --loglevel=info -P threads --concurrency=8`
4. Start Celery beat for daily re-run tasks `celery -A stock_api_backend beat --loglevel=info`
5. Start local ngrok server `ngrok http 8000` and add the "Forwarding" url to the .env file as the WEBHOOK_URL


Steps to set up Kafka (optional):
1. Start Zookeeper `bin/zookeeper-server-start.sh config/zookeeper.properties`
2. Start Kafka `bin/kafka-server-start.sh config/server.properties`
3. Check Kafka messages `bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic market_data --from-beginning`
