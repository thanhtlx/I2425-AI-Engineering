# 2425I_INT7024_Fraud_Transaction_BE


### Install dependencies

```shell
poetry config virtualenvs.in-project true
poetry install
poetry shell
```

### Setup database

Create a database

```shell
mysql -u root -p
mysql> CREATE DATABASE transaction_database;
mysql> exit
```

In `.env` file (create one if it doesn't exist), add database uri

```
SQLALCHEMY_DATABASE_URI=mysql+aiomysql://root:123456@127.0.0.1/transaction_database
```

Then upgrade database

```shell
alembic upgrade head
```
```
alembic revision --autogenerate -m "<your_message>"
alembic upgrade head
```

### Install `pre-commit` hooks

- Install `pre-commit`: https://pre-commit.com/ (should be installed globally)
- Install `pre-commit` hooks:

  ```shell
  make install-git-hooks
  ```

## Running

Inside the virtual environment, run

```shell
make run
```

### Run tests

Inside the virtual environment, run

```shell
make test
```

### Insert data into database

```shell
python scripts/insert_data.py
```

### Run with Docker Compose, Database and Frontend

```shell
docker-compose up --build -d
```