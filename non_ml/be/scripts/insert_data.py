import asyncio
import csv
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main._db import get_db_session
from main.models import (
    UserModel,
    StreetModel,
    StateModel,
    CityModel,
    CreditCardModel,
    MerchantModel,
    TransactionModel,
)
from pydantic import BaseModel


class CSVData(BaseModel):
    id: int
    trans_datetime: datetime
    cc_num: str
    merchant_name: str
    category: str
    amt: float
    first_name: str
    last_name: str
    gender: str
    street: str
    city: str
    state: str
    zip: str
    lat: float
    longi: float
    city_pop: int
    job: str
    dob: datetime
    trans_num: str
    unix_time: int
    merch_lat: float
    merch_long: float
    is_fraud: bool


class UserData(BaseModel):
    first_name: str
    last_name: str
    dob: datetime
    gender: str
    job: str

    def __hash__(self):
        return hash((self.first_name, self.last_name, self.dob, self.gender, self.job))


def read_first_n_rows(no_of_rows: int) -> list[CSVData]:
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "fraudTrain.csv")
    rows = []
    with open(file_path, "r") as file:
        csvreader = csv.reader(file)
        for i, row in enumerate(csvreader):
            if i < no_of_rows:
                if i == 0:
                    continue

                row_data = CSVData(
                    id=int(row[0]),
                    trans_datetime=datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S"),
                    cc_num=row[2],
                    merchant_name=row[3],
                    category=row[4],
                    amt=float(row[5]),
                    first_name=row[6],
                    last_name=row[7],
                    gender=row[8],
                    street=row[9],
                    city=row[10],
                    state=row[11],
                    zip=row[12],
                    lat=float(row[13]),
                    longi=float(row[14]),
                    city_pop=int(row[15]),
                    job=row[16],
                    dob=datetime.strptime(row[17], "%Y-%m-%d"),
                    trans_num=row[18],
                    unix_time=int(row[19]),
                    merch_lat=float(row[20]),
                    merch_long=float(row[21]),
                    is_fraud=bool(int(row[22])),
                )

                rows.append(row_data)
            else:
                break
    return rows


def read_first_n_rows_data_check(no_of_rows: int = 1000000000):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "fraudTrain.csv")
    with open(file_path, "r") as file:
        csvreader = csv.reader(file)
        user_data = {}
        for i, row in enumerate(csvreader):
            if i < no_of_rows:
                if i == 0:
                    continue

                row_data = CSVData(
                    id=int(row[0]),
                    trans_datetime=datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S"),
                    cc_num=row[2],
                    merchant_name=row[3],
                    category=row[4],
                    amt=float(row[5]),
                    first_name=row[6],
                    last_name=row[7],
                    gender=row[8],
                    street=row[9],
                    city=row[10],
                    state=row[11],
                    zip=row[12],
                    lat=float(row[13]),
                    longi=float(row[14]),
                    city_pop=int(row[15]),
                    job=row[16],
                    dob=datetime.strptime(row[17], "%Y-%m-%d"),
                    trans_num=row[18],
                    unix_time=int(row[19]),
                    merch_lat=float(row[20]),
                    merch_long=float(row[21]),
                    is_fraud=bool(row[22]),
                )
                if (
                    user_data.get(
                        f"{row_data.first_name}_{row_data.last_name}_{row_data.dob}_{row_data.gender}_{row_data.job}"
                    )
                    is not None
                ):
                    if (
                        user_data[
                            f"{row_data.first_name}_{row_data.last_name}_{row_data.dob}_{row_data.gender}_{row_data.job}"
                        ]
                        != f"{row_data.city}_{row_data.state}_{row_data.street}"
                    ):
                        pass

                user_data[
                    f"{row_data.first_name}_{row_data.last_name}_{row_data.dob}_{row_data.gender}_{row_data.job}"
                ] = f"{row_data.city}_{row_data.state}_{row_data.street}"

            else:
                break


async def insert_data(data: list[CSVData]):
    async for session in get_db_session():
        duplicate_user_track = set()
        state_mapping = {}
        city_mapping = {}
        street_mapping = {}
        user_mapping = {}
        credit_card_mapping = {}
        merchant_mapping = {}

        for index, row in enumerate(data):
            if state_mapping.get(row.state) is None:
                state_data = StateModel(name=row.state)
                session.add(state_data)
                await session.flush()
                state_mapping[row.state] = state_data.id
                state_id = state_data.id
            else:
                state_id = state_mapping[row.state]

            if city_mapping.get(row.city) is None:
                city_data = CityModel(
                    name=row.city, state_id=state_id, population=row.city_pop
                )
                session.add(city_data)
                await session.flush()
                city_mapping[row.city] = city_data.id
                city_id = city_data.id
            else:
                city_id = city_mapping[row.city]

            if street_mapping.get(row.street) is None:
                street_data = StreetModel(name=row.street, city_id=city_id)
                session.add(street_data)
                await session.flush()
                street_mapping[row.street] = street_data.id
                street_id = street_data.id
            else:
                street_id = street_mapping[row.street]

            user_data_schema = UserData(
                first_name=row.first_name,
                last_name=row.last_name,
                dob=row.dob,
                job=row.job,
                gender=row.gender,
            )
            if user_data_schema not in duplicate_user_track:
                user = UserModel(
                    dob=row.dob,
                    gender=row.gender,
                    email=f"{row.first_name}_{row.last_name}_{index}@gmail.com",
                    password="123456",
                    first_name=row.first_name,
                    last_name=row.last_name,
                    job=row.job,
                    zip=row.zip,
                    street_id=street_id,
                    city_id=city_id,
                    state_id=state_id,
                )
                session.add(user)
                await session.flush()
                duplicate_user_track.add(user_data_schema)
                user_mapping[
                    f"{row.first_name}_{row.last_name}_{row.dob}_{row.job}_{row.gender}"
                ] = user.id
                user_id = user.id
            else:
                user_id = user_mapping[
                    f"{row.first_name}_{row.last_name}_{row.dob}_{row.job}_{row.gender}"
                ]

            if credit_card_mapping.get(row.cc_num) is None:
                credit_card = CreditCardModel(number=row.cc_num, owner_user_id=user_id)
                session.add(credit_card)
                await session.flush()
                credit_card_mapping[row.cc_num] = credit_card.id
                credit_card_id = credit_card.id
            else:
                credit_card_id = credit_card_mapping[row.cc_num]

            merchant_name = (
                row.merchant_name[6:]
                if row.merchant_name.startswith("fraud_")
                else row.merchant_name
            )
            if merchant_mapping.get(merchant_name) is None:
                merchant = MerchantModel(
                    name=merchant_name, merchant_category=row.category
                )
                session.add(merchant)
                await session.flush()
                merchant_mapping[merchant_name] = merchant.id
                merchant_id = merchant.id
            else:
                merchant_id = merchant_mapping[merchant_name]

            transaction = TransactionModel(
                transaction_number=row.trans_num,
                transaction_time=row.trans_datetime,
                is_fraud=row.is_fraud,
                amount=row.amt,
                user_id=user_id,
                merchant_id=merchant_id,
                credit_card_id=credit_card_id,
                coordination_metadata={
                    "user": {"latitude": row.lat, "longitude": row.longi},
                    "merchant": {
                        "latitude": row.merch_lat,
                        "longitude": row.merch_long,
                    },
                },
            )
            session.add(transaction)
            await session.flush()

        await session.commit()


if __name__ == "__main__":
    NUMBER_OF_ROWS = 10000
    csv_data = read_first_n_rows(no_of_rows=NUMBER_OF_ROWS)
    asyncio.run(insert_data(data=csv_data))
