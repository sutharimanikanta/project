# streamlit_app.py
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Station, Product, Inventory, DemandHistory, Distribution

# Database setup
engine = create_engine("sqlite:///resource_tracking.db")
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit interface
st.set_page_config(page_title="Resource Tracker", layout="wide")

menu = ["Stations", "Products", "Inventory", "Demand", "Distributions"]
choice = st.sidebar.selectbox("Menu", menu)


def crud_template(model_cls, form_fields, display_columns):
    """Generic CRUD template for different models"""
    items = session.query(model_cls).all()

    # Display data
    st.header(f"{model_cls.__name__} Management")
    if items:
        st.dataframe(
            [{col: getattr(item, col) for col in display_columns} for item in items]
        )
    else:
        st.info("No records found")

    # Create/update form
    st.subheader("Add/Edit Record")
    form_container = st.form(f"{model_cls.__name__}_form")
    form_data = {}
    for field in form_fields:
        if isinstance(form_fields[field], list):
            options = form_fields[field]
            form_data[field] = form_container.selectbox(field, options)
        else:
            form_data[field] = form_container.text_input(field, form_fields[field])

    submit = form_container.form_submit_button("Save")
    if submit:
        if model_cls == Station:
            item = Station(**form_data)
        elif model_cls == Product:
            item = Product(**form_data)
        # Add other model conditions here
        session.add(item)
        session.commit()
        st.success("Record saved successfully")


# Stations page
if choice == "Stations":
    crud_template(
        Station,
        {"name": "", "location": "", "description": ""},
        ["name", "location", "description"],
    )

# Products page
elif choice == "Products":
    crud_template(Product, {"name": "", "description": ""}, ["name", "description"])

# Inventory page
elif choice == "Inventory":
    stations = {s.name: s.id for s in session.query(Station).all()}
    products = {p.name: p.id for p in session.query(Product).all()}

    st.header("Inventory Management")
    inventory = session.query(Inventory).join(Station).join(Product).all()

    # Display inventory
    if inventory:
        st.dataframe(
            [
                {
                    "Station": i.station.name,
                    "Product": i.product.name,
                    "Quantity": i.quantity,
                }
                for i in inventory
            ]
        )
    else:
        st.info("No inventory records")

    # Inventory form
    with st.form("inventory_form"):
        station = st.selectbox("Station", list(stations.keys()))
        product = st.selectbox("Product", list(products.keys()))
        quantity = st.number_input("Quantity", min_value=0)

        if st.form_submit_button("Add Inventory"):
            inv = Inventory(
                station_id=stations[station],
                product_id=products[product],
                quantity=quantity,
            )
            session.add(inv)
            session.commit()
            st.success("Inventory added")

# Demand page
elif choice == "Demand":
    stations = {s.name: s.id for s in session.query(Station).all()}
    products = {p.name: p.id for p in session.query(Product).all()}

    st.header("Demand History")
    demands = session.query(DemandHistory).join(Station).join(Product).all()

    if demands:
        st.dataframe(
            [
                {
                    "Station": d.station.name,
                    "Product": d.product.name,
                    "Quantity Requested": d.quantity_requested,
                    "Date": d.date,
                }
                for d in demands
            ]
        )
    else:
        st.info("No demand records")

    with st.form("demand_form"):
        station = st.selectbox("Station", list(stations.keys()))
        product = st.selectbox("Product", list(products.keys()))
        quantity = st.number_input("Quantity Requested", min_value=0)

        if st.form_submit_button("Log Demand"):
            demand = DemandHistory(
                station_id=stations[station],
                product_id=products[product],
                quantity_requested=quantity,
            )
            session.add(demand)
            session.commit()
            st.success("Demand logged")

# Distributions page
elif choice == "Distributions":
    stations = {s.name: s.id for s in session.query(Station).all()}
    products = {p.name: p.id for p in session.query(Product).all()}

    st.header("Resource Distributions")
    distributions = (
        session.query(Distribution)
        .join(Station, Distribution.from_station)
        .join(Product)
        .all()
    )

    if distributions:
        st.dataframe(
            [
                {
                    "From": d.from_station.name,
                    "To": d.to_station.name,
                    "Product": d.product.name,
                    "Quantity": d.quantity,
                    "Date": d.date,
                }
                for d in distributions
            ]
        )
    else:
        st.info("No distribution records")

    with st.form("distribution_form"):
        from_station = st.selectbox("From Station", list(stations.keys()))
        to_station = st.selectbox("To Station", list(stations.keys()))
        product = st.selectbox("Product", list(products.keys()))
        quantity = st.number_input("Quantity", min_value=0)

        if st.form_submit_button("Record Distribution"):
            distribution = Distribution(
                from_station_id=stations[from_station],
                to_station_id=stations[to_station],
                product_id=products[product],
                quantity=quantity,
            )
            session.add(distribution)
            session.commit()
            st.success("Distribution recorded")

# Database models (same as previous implementation)
# Create models.py file with:
# from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
#
# Base = declarative_base()
#
# class Station(Base):
#     __tablename__ = 'station'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100), nullable=False)
#     location = Column(String(100), nullable=False)
#     description = Column(Text)
#     # ... (rest of the model definitions as before)
