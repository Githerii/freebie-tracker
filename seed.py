from models import session, Company, Dev, Freebie

# Clear existing data
session.query(Freebie).delete()
session.query(Company).delete()
session.query(Dev).delete()
session.commit()

# Create companies
apple = Company(name="Apple", founding_year=1976)
google = Company(name="Google", founding_year=1998)
microsoft = Company(name="Microsoft", founding_year=1975)

# Create devs
nate = Dev(name="Nate")
sam = Dev(name="Sam")
jane = Dev(name="Jane")

session.add_all([apple, google, microsoft, nate, sam, jane])
session.commit()

# Create freebies
f1 = Freebie(item_name="Sticker Pack", value=5, dev=nate, company=apple)
f2 = Freebie(item_name="T-Shirt", value=20, dev=sam, company=google)
f3 = Freebie(item_name="USB Drive", value=15, dev=jane, company=microsoft)

session.add_all([f1, f2, f3])
session.commit()

print("Database seeded.")
