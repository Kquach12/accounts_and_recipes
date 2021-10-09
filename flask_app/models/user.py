# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash 
from flask_app.models import recipe
# model the class after the friend table from our database

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipe_schema').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users



    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at ) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipe_schema').query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('recipe_schema').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipe_schema').query_db(query, data)
        return cls(results[0])
        
    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE emails SET email = %(email)s, updated_at = NOW() WHERE id = %(id)s"
    #     return connectToMySQL('recipe_schema').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM userss WHERE id = %(id)s"
        return connectToMySQL('recipe_schema').query_db(query, data)

    @staticmethod
    def validate_email(user):
        is_valid = True
        # test whether a field matches the pattern
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipe_schema').query_db(query,user)
        if len(results) >= 1:
            flash("Email is taken!", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match! ", "register")
            is_valid = False
        if len(user['password']) < 5:
            flash("Password must be at least 5 characters ", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("Please enter your first name ", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Please enter your last name ", "register")
            is_valid = False

        return is_valid


    @staticmethod
    def validate_login(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipe_schema').query_db(query,user)
        if len(results) == 0:
            flash("Account does not exist", "login")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Please enter an email", "login")
            is_valid = False
        return is_valid