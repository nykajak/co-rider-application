from flask import Flask,request
from custom_utility import utility_pythonify, success_200, error_404_not_found, error_400_bad_request, error_409_conflict
from flask_pymongo import PyMongo,ObjectId
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY",'temp_secret')
app.config["MONGO_URI"] = "mongodb://db:27017/testdb"
client = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route("/users",methods=["GET"])
def all_users():
    """
        Used for: Getting all the users in the users collection.
        Usage: GET /users
        Return: 
            If no users: [<list-of-ids-of-all-users>], 200
            If empty: [], 200
    """
    l = []
    for user in client.db.users.find():
        l.append(str(user["_id"]))

    return success_200(l)


@app.route("/users/<uid>",methods=["GET"])
def see_user(uid):
    """
        Used for: Getting the details of a specific user given user id. uid - alphanumeric string of length 24.
        Usage: GET /users/<uid>
        Return: 
            If found: {_id:<_id>, name:<name>, email:<email>, password:<password>}, 200
            If not found: {"error":"User with that ID does not exist!"}, 404
    """

    if len(uid) != 24:
        return error_404_not_found()

    user = client.db.users.find_one({"_id": ObjectId(uid)})
    if user is not None:
        user = utility_pythonify(user)
        return success_200(user)

    else:
        return error_404_not_found()

@app.route("/users",methods=["POST"])
def create_user():
    """
        Used for: Creating a new user.
        Usage: POST /users
               REQUIRED form body: name, email and password
        Return: 
            If successful: {_id:<_id>, name:<name>, email:<email>, password:<password>}, 200
            If required params not given: {"error": "Missing one or more required parameters - name, email and password"}, 400
            If username already taken: {"error": "User with that username already exists!"}, 409
            If email already taken: {"error": "User with that email already exists!"}, 409
            If both email and username taken: {"error": ""Both email and username already in use!""}, 409
    """
    params = {k:v for k,v in request.form.items() if k in ["name","email","password"]}

    if len(params) < 3:
        return error_400_bad_request("Missing one or more required parameters - name, email and password")

    name = params["name"]
    email = params["email"]
    password = params["password"]

    username_taken = True if client.db.users.find_one({"name": name}) else False
    email_taken = True if client.db.users.find_one({"email": email}) else False

    if username_taken and not email_taken:
        return error_409_conflict("User with that username already exists!")
    
    elif email_taken and not username_taken:
        return error_409_conflict("User with that email already exists!")
    
    elif email_taken and username_taken:
        return error_409_conflict("Both email and username already in use!")

    _id = client.db.users.insert_one({
        "name": name,
        "email": email,
        "password": str(bcrypt.generate_password_hash(password))
    }).inserted_id

    user = client.db.users.find_one({"_id": ObjectId(_id)})
    user = utility_pythonify(user)

    return success_200(user)

@app.route("/users/<uid>",methods=["DELETE"])
def delete_user(uid):
    """
        Used for: Deleting a specific user with given uid as id.  uid - alphanumeric string of length 24.
        Usage: DELETE /users/<uid>
        Return:
            If successful: {_id:<_id>, name:<name>, email:<email>, password:<password>}, 200
            If not found: {"error":"User with that ID does not exist!"}, 404
    """

    if len(uid) != 24:
        return error_404_not_found()

    user = client.db.users.find_one({"_id": ObjectId(uid)})
    if user is not None:
        client.db.users.delete_one({"_id": ObjectId(uid)})
        user = utility_pythonify(user)
        return success_200(user)

    else:
        return error_404_not_found()

@app.route("/users/<uid>",methods=["PUT"])
def edit_user(uid):
    """
        Used for: Editing details of a specific user.
        Usage: PUT /users/<uid>
               REQUIRED: At least one of name,email and password
        Return: 
            If successful: {_id:<_id>, name:<name>, email:<email>, password:<password>}, 200
            If not found: {"error":"User with that ID does not exist!"}, 404
            If required params not given: {"error": "At least one parameter among name, password,email required."}, 400
    """

    if len(uid) != 24:
        return error_404_not_found()

    params = {k:v for k,v in request.form.items() if k in ["name","password","email"]}

    if "password" in params:
        params["password"] = bcrypt.generate_password_hash(params["password"])

    if not 0 < len(params):
        return error_400_bad_request("At least one parameter among name, password,email required.")

    user = client.db.users.find_one({"_id": ObjectId(uid)})
    if user is not None:
        client.db.users.update_one({"_id": ObjectId(uid)},{
            "$set": params
        })

        user = client.db.users.find_one({"_id": ObjectId(uid)})
        user = utility_pythonify(user)
        return success_200(user)

    else:
        return error_404_not_found()

if __name__ == "__main__":
    app.run('0.0.0.0',port=5000,debug=True)