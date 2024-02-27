# Web-Scrapper---Real-Estate-Data

- This project scrapes data from real estate websites.
- Store results as a .csv and loads it into an S3 Bucket.
- From the S3 Bucket it goes into Amazon Redshift for datawarehousing.
- And finally, enables this data to be retrieve through a REST API.

## Scraped Sites:

- Encuentra24
- Mitula

<br>
<img src="https://i.imgur.com/QektISc.png" alt="Real Estate Web Scraper">

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
