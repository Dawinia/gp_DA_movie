FROM python:3.7.6
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["scrapy", "crawl", "movie"]