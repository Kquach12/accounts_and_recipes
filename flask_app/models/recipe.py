# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models import user 
# model the class after the friend table from our database


class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_30_minutes = data['under_30_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.users = []
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipe_schema').query_db(query)
        # Create an empty list to append our instances of friends
        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes

    @classmethod   
    def get_all_with_users(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL('recipe_schema').query_db(query)
        recipes = []
        # for row in results:
        for i in range(len(results)):
            recipes.append( cls(results[i]) )
            u = {
                "id": results[i]['users.id'],
                "first_name": results[i]['first_name'],
                "last_name": results[i]['last_name'],
                "email": results[i]['email'],
                "password": results[i]['password'],
                "created_at": results[i]['created_at'],
                "updated_at": results[i]['updated_at']
            }
            recipes[i].users.append(user.User(u))
        return recipes

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instruction, under_30_minutes, created_at, updated_at, user_id ) VALUES (%(name)s, %(description)s, %(instruction)s, %(under_30_minutes)s , %(created_at)s , NOW(), %(user_id)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipe_schema').query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipe_schema').query_db(query, data)
        return cls(results[0])
    
        
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, under_30_minutes = %(under_30_minutes)s, created_at = %(created_at)s,  updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL('recipe_schema').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL('recipe_schema').query_db(query, data)

    @classmethod 
    def get_one_with_user(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipe_schema').query_db(query, data)
        recipe = cls(results[0])
        for row in results:
            u = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            recipe.users.append(user.User(u))
        return recipe

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        # test whether a field matches the pattern
        query = "SELECT * FROM recipes WHERE name = %(name)s;"
        results = connectToMySQL('recipe_schema').query_db(query,recipe)
        if 'under_30_minutes' not in recipe:
            flash("Please indicate the length of time! ", "recipe")
            is_valid = False
        if len(recipe['name']) < 3:
            flash("Name needs to be at least 3 characters", "recipe")
            is_valid = False
        if len(recipe['description']) < 5:
            flash("Description must be at least 5 characters ", "recipe")
            is_valid = False
        if len(recipe['instruction']) < 5:
            flash("Instruction must be at least 5 characters", "recipe")
            is_valid = False
        if len(recipe['created_at']) < 1:
            flash("Please enter a date", "recipe")
            is_valid = False

        return is_valid

