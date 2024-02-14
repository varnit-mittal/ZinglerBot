
# Automated Travel and Trading Bot Web App with an addition of mail read

This project was created for Zense Hackathon- HACKNITE which is a 36 hour Hackathon.

Creators:  Varnit Mittal (IMT2022025)
           Aditya Priyadarshi (IMT2022075)

Team Name:  Open Source Dalle

Institution: International Institute of Information Technology Bangalore(IIITB)

This Web App is a a type of bot which has three features:

1) Travel information of hotels and trains which gives you a proper list according to filters you choose and travel places you want to visit.

2) Trading bot which is created keeping in mind both a new comer in this field and an expert in this field. This bot uses Alpaca API for trading in real world with fake money and this is called paper trading. Our bot also recommends the user whether to buy the stock or sell it. It also gives the user a graph created by long term study of markets.

3) Email read is created with the help of Gmail RESTful API and BeautifulSoup (bs4) library in python. This provides you with top 5 to 7 gmails from your account for which .pickle file is created.






## API Reference



  alpaca_trade_api

| Parameter |   Description                |
| :-------- |  :------------------------- |
| `api_key` |   **Required**. PKN6GDAUTTEG136IG0KK|

| Parameter |  Description                       |
| :-------- | :-------------------------------- |
| `id`      | ` **Required**. r8BcO9jQhIT0SgJWmx4fZVl7n2IhxlTQiumd8LB0 |


google RESTful API

| Parameter |   Description                |
| :-------- |  :------------------------- |
| `api_key` |   **Required**. AIzaSyDRYy6uYpNvGBD2LrjkM05p35Ate8fqLhk|

| Parameter |  Description                       |
| :-------- | :-------------------------------- |
| `id`      |  **Required**. 877922172198-aqqu9q1dooua3lb8gblcpdbtrvuiaeo8.apps.googleusercontent.com |






  


## Run Locally

Clone the project

```bash
  git clone https://github.com/varnit-mittal/web_scrapping_hacknite.git
```

Go to the project directory

```bash
  cd web_scrapping_hacknite
```

## Install Dependencies
Install chrome webdriver and make changes in the train and hotel backend in os.PATH

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  streamlit run frontend.py
```

## Deployment

To deploy this project 

You can deploy using streamlit library
## Demo

https://youtu.be/ppb5AKOUUYE

## Authors

- [@varnit-mittal](https://github.com/varnit-mittal)
- [@ap5967ap](https://github.com/ap5967ap)

Linkedin:

https://www.linkedin.com/in/varnit-mittal-44a904254/

https://www.linkedin.com/in/aditya-priyadarshi-a2375b256


## License

[MIT](https://choosealicense.com/licenses/mit/)

