from sqlalchemy import Integer, Column, DateTime

from db.config import Base


class Image(Base):
    __tablename__ = "image"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    size = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Image "{self.title}">'
