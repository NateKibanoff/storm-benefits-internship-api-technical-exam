#import the necessary libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import fnmatch

#initialize database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///companies.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#company entity
class Companies(db.Model):
    id = db.Column("company_id", db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    employees = db.Column(db.Integer)
    location = db.Column(db.String(100))
    email = db.Column(db.String(50))
    industry = db.Column(db.String(50))
    def __init__(self, name, employees, location, email, industry):
        self.name = name
        self.employees = employees
        self.location = location
        self.email = email
        self.industry = industry

db.create_all()

#insert a new company record
def addCompanyRecord(name, employees, location, email, industry):
    db.session.add(Companies(name, employees, location, email, industry))

#update an existing company record
def updateCompanyRecord(id_num, name, employees, location, email, industry):
    if len(Companies.query.filter_by(id = id_num).all()) > 0:
        Companies.query.filter_by(id = id_num).all()[0].name = name
        Companies.query.filter_by(id = id_num).all()[0].employees = employees
        Companies.query.filter_by(id = id_num).all()[0].location = location
        Companies.query.filter_by(id = id_num).all()[0].email = email
        Companies.query.filter_by(id = id_num).all()[0].industry = industry    

#delete company record
def deleteCompanyRecord(id_num):
    c = Companies.query.filter_by(id = id_num).all()[0]
    db.session.delete(c)

#get company record details
def getRecordDetails(comp):
    if(type(comp)==int):
        matching_list = Companies.query.filter_by(id = comp).all()
        if len(matching_list) > 0:
            c = matching_list[0]
        else:
            return
            
    else:
        c = comp
    print("Company name:",c.name)
    print("Number of employees:",c.employees)
    print("Location:",c.location)
    print("E-mail address:",c.email)
    print("Industry:",c.industry)
    print()

#list all company records
def listAllRecords():
    for c in Companies.query.all():
        getRecordDetails(c)

#filter list of companies by company name using wildcard search
def wildcardSearch(company_name):
    company_list = Companies.query.all()
    matching = []
    for c in company_list:
        if fnmatch.fnmatch(c.name, company_name):
            matching.append(c)
    return matching
