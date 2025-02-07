from sqlalchemy.ext.asyncio import AsyncSession

from main.schemas.user.user import AllUserResponse, UserBase, UserDetail, CreditCard
from main.services import (
    user_service,
    city_service,
    street_service,
    state_service,
)
from main.misc.exceptions import NotFound


async def get_users(session: AsyncSession, page: int, per_page: int) -> AllUserResponse:
    user_models, count = await user_service.get_users(
        session=session, page=page, per_page=per_page
    )
    users: list[UserBase] = []
    for user in user_models:
        users.append(
            UserBase(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                dob=user.dob,
                email=user.email,
                gender=user.gender,
            )
        )
    return AllUserResponse(items=users, page=page, per_page=per_page, total=count)


async def get_user_details(session: AsyncSession, user_id: int) -> UserDetail | None:
    user = await user_service.get_user(session=session, user_id=user_id)
    if not user:
        raise NotFound(error_message=f"User with id {user_id} not found")

    city = await city_service.get_city(session=session, city_id=user.city_id)
    state = await state_service.get_state(session=session, state_id=user.state_id)
    street = await street_service.get_street(session=session, street_id=user.street_id)

    credit_cards = await user_service.get_user_credit_cards(
        session=session, user_id=user_id
    )

    return UserDetail(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        dob=user.dob,
        email=user.email,
        gender=user.gender,
        job=user.job,
        street=street.name,
        city=city.name,
        state=state.name,
        zip=user.zip,
        credit_cards=[CreditCard.from_orm(credit_card) for credit_card in credit_cards],
    )
