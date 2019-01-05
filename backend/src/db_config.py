from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.orm import sessionmaker

from src.models import Base

dialect = "mysql+pymysql"

login = "test"
password = "test"
host = "localhost"
db_name = "vsutestrunner"
options = ""

connection_string = "{dialect}://{login}:{password}@{host}/{db_name}{options}".format(dialect=dialect,
                                                                                      login=login,
                                                                                      password=password,
                                                                                      host=host,
                                                                                      db_name=db_name,
                                                                                      options=options)
print "Connection string: {}".format(connection_string)


engine = create_engine(connection_string, echo=True)
Session = sessionmaker(engine)

