from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

class Base(DeclarativeBase):
	__abstract__ = True
	__table_args__ = {'extend_existing': True}

	id: Mapped[int] = mapped_column(primary_key=True)

	@declared_attr.directive
	def __tablename__(cls) -> str:
		return cls.__name__.lower()