from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/create/recipe')
def create_page():
    if 'user_id' in session:
        data = {
            "id": session['user_id']
        }
        user = User.get_one(data)
        return render_template('create_recipe.html', user = user)

@app.route('/create', methods = ["POST"])
def add_to_db():
    if not Recipe.validate_recipe(request.form):
        return redirect('/')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "under_30_minutes": request.form['under_30_minutes'],
        "created_at": request.form['created_at'],
        "user_id": session['user_id']
    }
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/view/<int:id>')
def view_recipe(id):
    data = {
        "id": id
    }
    recipe = Recipe.get_one_with_user(data)
    return render_template("view_recipe.html", recipe = recipe)
