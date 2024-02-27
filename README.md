# Web-Scrapper---Real-Estate-Data

- This project scrapes data from real estate websites.
- Store results as a .csv and load it into an S3 Bucket.
- From the S3 Bucket, it goes into Amazon Redshift for data warehousing.
- And finally, enables this data to be retrieved through a REST API.

## Scraped Sites

- Encuentra24
- Mitula

![image](https://github.com/kevinknights29/Web-Scrapper--Real-Estate-Data/assets/74464814/911b5e03-8dd0-4b02-83fe-60a0049d3ae8)

## Getting Started

### Docker

- Build container with:

    ```bash
    docker build . -t web-scrapper-real-estate
    ```

- Run the containerized application with:

    ```bash
    docker run web-scrapper-real-estate
    ```

You should start seeing the following output from the processing script.

![image](https://github.com/kevinknights29/Web-Scrapper--Real-Estate-Data/assets/74464814/e742bf91-eef2-40d2-aa89-7533d73c27fc)
