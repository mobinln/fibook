# FiBook

## Overview

A production-ready portfolio management app built with FastAPI, PostgreSQL, React, and MageAI.
The Idea behind this application is to have a portfolio management system that can manage almost anything
from crypto to stock and even gold assets with different currencies and exchange rates.

## How To Run

To run the application, you need Docker. After installing Docker, simply run `docker compose up -d` and everything will be up and running.

## Overall Structure

There are different modules inside this project, which I will explain briefly.
1. data: in this directory, we create our MageAI pipelines, where there is currently one data-loader which loads top crypto prices from Nobitex API to the PostgreSQL
2. ui: Here is the main frontend of the project created by React, Vitejs, Tailwind, and Shadcn
3. api: Here is the main api backend written with FastAPI and SQLAlchemy. For auth, I used FastAPI's OAuth middleware with JWT authentication. There are multiple entities in this app.

## Database Entities

1. User: representing the users and admins
2. Currency: representing the currencies (fiat or non-fiat, a currency can be BTC or even gold)
3. exchange-rate: which represents the exchange rates between currencies
4. asset and asset-type: which are the different entities that a user can add to their portfolio
5. portfolio, portfolio-holding, portfolio-transaction: here we keep track of the users' portfolio holdings
6. market-data: which is the market data used for assets, cryptos, etc...
