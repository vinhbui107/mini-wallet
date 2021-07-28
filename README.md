# Mini Wallet

This is an API backend service, for managing a simple mini wallet.

## Database Design

## ![Mini Wallet DB](https://github.com/vinhbui107/mini-wallet/blob/main/images/mini_wallet_db.png)

## API Design

This api followed by [Mini Wallet Exercise](https://documenter.getpostman.com/view/8411283/SVfMSqA3?version=latest)

## Requirements

-   Python (I'm using 3.8+)
-   PostgreSQL (I'm using 12+)
-   Linux or Mac for best practice

#### Database

```shell
Please create a new database with those configs

DATABASE NAME: mini_wallet
USER: postgres
PASSWORD: postgres
HOST: 127.0.0.1
PORT: 5432

That config works on my machine :(
If not on your machine please change config in .env file.
```

## Installation / Getting started

Here is a quick step-by-step minimal setup, to get the app up and running in your local workstation:

### Platform independent

Clone my project:

```shell
git clone https://github.com/vinhbui107/mini-wallet.git

cd mini-wallet
```

Create Python virtual enviroment:

```shell
python3 -m venv venv
```

Activate virtual enviroment (this command can change based on OS):

```shell
source venv/bin/activate
```

Install backend dependencies using pip:

```shell
pip install -r requirements.txt
```

Create database tables:

```shell
python manage.py migrate
```

Run server API:

```shell
python manage.py runserver
```

After finished config for API. Now test my API on http://localhost:8000 :)

#### Have fun :)

![Thanks!](https://media.giphy.com/media/l4KibK3JwaVo0CjDO/giphy.gif)
