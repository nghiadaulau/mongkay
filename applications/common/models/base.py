from datetime import datetime
from typing import Union

from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column
from typing_extensions import Annotated
from applications.common.utils.timezone import timezone

'''
mapped_column:  The mapped_column() function provides an ORM-aware and Python-typing-compatible construct which is used with declarative mappings to indicate an attribute that’s mapped to a Core Column object. It provides the equivalent feature as mapping an attribute to a Column object directly when using Declarative, specifically when using Declarative Table configuration.
'''
id_key = Annotated[
    int, mapped_column(primary_key=True, index=True, autoincrement=True, sort_order=-999, comment='primary_key')
]


class UserMixin(MappedAsDataclass):
    create_user: Mapped[int] = mapped_column(sort_order=998)
    update_user: Mapped[Union[int, None]] = mapped_column(init=False, default=None, sort_order=998)


class DateTimeMixin(MappedAsDataclass):
    created_time: Mapped[datetime] = mapped_column(
        init=False, default_factory=timezone.now, sort_order=999, comment='创建时间'
    )
    updated_time: Mapped[Union[datetime, None]] = mapped_column(
        init=False, onupdate=timezone.now, sort_order=999, comment='更新时间'
    )


class MappedBase(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class DataClassBase(MappedAsDataclass, MappedBase):
    __abstract__ = True
