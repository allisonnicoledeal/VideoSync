from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session


engine = create_engine("sqlite:///tracks.db", echo=True)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush=False))

Base = declarative_base()
Base.query = session.query_property()


# Class declarations

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True)
    filename = Column(String(64), nullable=False)
    title = Column(String(64), nullable=True)
    artist = Column(String(64), nullable=True)
    event = Column(String(64), nullable=True)
    bytes = Column(Integer, nullable=True)
    length = Column(Integer, nullable=True)
    date_uploaded = Column(DateTime, nullable=True)
    path = Column(String(128), nullable=True)
    filename_webm = Column(String(64), nullable=True)
    youtube_url = Column(String(256), nullable=True)
    thumbnail_url = Column(String(64), nullable=True)

    # analysis_track


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    sync_point = Column(Integer, nullable=False)  # num milliseconds?

    analyses_group = relationship("Group", backref=backref("analysis_group"), order_by=id)
    analysis_track = relationship("Track", backref=backref("analysis_track"))  # uselist=False

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=True)
    

    # analysis_group



# class AnalyzeTrack(Base):
#     __tablename__ = "analyze_tracks"

#     analyze_track_id = Column(Integer, primary_key=True)
#     track_id = relationship("Track", backref=backref("analysis_details"), order_by=id)
#     raw_data = Column
#     samples = Column
#     fourier = Column
#     max_freq = Column
#     time_freq_table

# End of class declarations



# def connect():
#     global ENGINE
#     global Session

#     ENGINE = create_engine("sqlite:///tracks.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()


def main():
    pass

if __name__ == "main":
    main()
