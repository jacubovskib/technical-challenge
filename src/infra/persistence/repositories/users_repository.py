from sqlalchemy import desc, asc, update, or_

from src.domain.exceptions import IntegrityException
from src.domain.notification.notification import Notification
from src.domain.pagination.pagination import Pagination
from src.domain.pagination.search_query import SearchQuery
from src.domain.user.user import User
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.persistence.entities.users import UserEntity
from src.domain.user.abs_user_gateway import AbsUsersGateway

class UsersRepository(AbsUsersGateway):

    @classmethod
    def insert_usr(cls, user: User) -> User:
        with DBConnectionHandler() as db:
            notification = cls._check_existing_fields(db.session, user.name, user.email)

            if notification.has_errors():
                raise IntegrityException(notification.get_errors())

            try:
                user = UserEntity.from_domain(user)
                db.session.add(user)
                db.session.commit()
                return user.to_domain()
            except Exception as e:
                db.session.rollback()
                raise e

    @classmethod
    def get_user(cls, an_id: int) -> User | None:
        with DBConnectionHandler() as db:
            user = db.session.query(UserEntity).where(UserEntity.id == int(an_id)).first()
            if user: return user.to_domain()
            return None

    @classmethod
    def list_all_users(cls, a_query: SearchQuery) -> Pagination[UserEntity]:
        _page = int(a_query.page)
        _per_page = int(a_query.per_page)
        _terms: str = a_query.terms
        _sort: str = a_query.sort
        _direction: str = a_query.direction

        with DBConnectionHandler() as db:
            query = db.session.query(UserEntity)

            if _terms:
                search_term = f"%{_terms}%"
                query = query.filter(
                    UserEntity.name.ilike(search_term) |
                    UserEntity.email.ilike(search_term)
                )

            if _sort and hasattr(UserEntity, _sort):
                order_func = asc if _direction.lower() == 'asc' else desc
                query = query.order_by(order_func(getattr(UserEntity, _sort)))

            total_records = query.count()
            offset = (_page - 1) * _per_page
            users = query.offset(offset).limit(_per_page).all()

            return Pagination(
                current_page=_page,
                per_page=_per_page,
                total=total_records,
                items=[user.to_dict() for user in users]
            )

    @classmethod
    def update_user(cls, an_user: User) -> None:
        with DBConnectionHandler() as db:
            try:
                update_statement = (
                    update(UserEntity)
                    .where(UserEntity.id == an_user.id)
                    .values(
                        name=an_user.name,
                        email=an_user.email
                    )
                )
                db.session.execute(update_statement)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

    @classmethod
    def delete_user(cls, an_id: int) -> bool:
        with DBConnectionHandler() as db:
            try:
                user = db.session.query(UserEntity).filter(UserEntity.id == an_id).first()
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    return True
                else:
                    return False
            except Exception as e:
                db.session.rollback()
                raise e

    @classmethod
    def _check_existing_fields(cls, db_session, a_name: str, an_email: str) -> Notification:
        notification = Notification()

        existing_records = db_session.query(UserEntity).filter(
            or_(
                UserEntity.email == an_email,
                UserEntity.name == a_name
            )
        ).all()

        for record in existing_records:
            if record.email == an_email:
                notification.add_error("Este email já está cadastrado no sistema")
            if record.name == a_name:
                notification.add_error("Este nome já está cadastrado no sistema")

        return notification