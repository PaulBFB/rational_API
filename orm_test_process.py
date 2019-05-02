from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, DateTime, String, Boolean
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///database.sqlite')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()


class ProcessORM(Base):
    __tablename__ = 'process'
    batch_id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    app_version = Column(String)
    care_recipe = Column(Boolean)
    category = Column(Integer)
    chamber_id = Column(Integer)
    device_family = Column(String)
    device_name = Column(String)
    device_serialnumber = Column(String)
    finished = Column(Boolean)
    group_id = Column(Integer)
    group_name = Column(String)
    process_id = Column(Integer)
    recipe_id = Column(Integer)
    recipe_name = Column(String)
    start = Column(DateTime)
    temp_unit = Column(String)


newprocess = ProcessORM(batch_id=1,
                        created=datetime.now(),
                        app_version='rand',
                        care_recipe=False,
                        category=12,
                        chamber_id=1000,
                        device_family='blank',
                        device_name='699-124_SAT',
                        device_serialnumber='E11SH13022340226',
                        finished=False,
                        group_id=1,
                        group_name='03-Sattledt',
                        process_id=1,
                        recipe_id=195,
                        recipe_name='schnell',
                        start=datetime.now()-timedelta(hours=1, minutes=15))

session.add(newprocess)
session.commit()
