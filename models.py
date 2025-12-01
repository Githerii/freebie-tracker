from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///freebies.db")
Session = sessionmaker(bind=engine)
session = Session()


# ---------------------------
# MODELS
# ---------------------------

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    # Relationships
    freebies = relationship("Freebie", backref="company")

    @property
    def devs(self):
        """All devs who have collected freebies from this company."""
        return list({freebie.dev for freebie in self.freebies})

    # Deliverable: give_freebie
    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(
            item_name=item_name,
            value=value,
            dev=dev,
            company=self
        )
        session.add(new_freebie)
        session.commit()
        return new_freebie

    # Deliverable: oldest_company
    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year.asc()).first()


class Dev(Base):
    __tablename__ = "devs"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship("Freebie", backref="dev")

    @property
    def companies(self):
        """All companies this dev has collected freebies from."""
        return list({freebie.company for freebie in self.freebies})

    # Deliverable: received_one
    def received_one(self, item_name):
        return any(f.item_name == item_name for f in self.freebies)

    # Deliverable: give_away
    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev
            session.commit()
            return True
        return False


class Freebie(Base):
    __tablename__ = "freebies"

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)
    dev_id = Column(Integer, ForeignKey("devs.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))

    # Deliverable: print_details
    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
