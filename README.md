# Co-rider assignment

## To run the files
- Ensure Docker is installed on the target system.
- Clone this repo and navigate to it.
- Run `docker compose up --build` to run the program
- Navigate to localhost:5000/users to explore the API

## API Endpoints

### GET /users
- Used for: Getting all the users in the users collection.
- Return: 
    - If no users: [list-of-ids-of-all-users], 200
    - If empty: [], 200

### GET /users/"uid"
- Used for: Getting the details of a specific user given user id. uid - alphanumeric string of length 24.
- Return: 
    - If found: {_id:_id, name:name, email:email, password:password}, 200
    - If not found: {"error":"User with that ID does not exist!"}, 404

### POST /users?name=A&email=B&password=C
- REQUIRED params: name, email and password
- Used for: Creating a new user. Note that passwords are hashed at the server before storing.
- Return: 
    - If successful: {_id:_id, name:name, email:email, password:password}, 200
    - If required params not given: {"error": "Missing one or more required parameters - name, email and password"}, 400
    - If username already taken: {"error": "User with that username already exists!"}, 409
    - If email already taken: {"error": "User with that email already exists!"}, 409
    - If both email and username taken: {"error": ""Both email and username already in use!""}, 409


### DELETE /users/"uid"
- Used for: Deleting a specific user with given uid as id.  uid - alphanumeric string of length 24.
- Return:
    - If successful: {_id:_id, name:name, email:email, password:password}, 200
    - If not found: {"error":"User with that ID does not exist!"}, 404

### PUT /users/"uid"
- REQUIRED params: At least one of name, email and password
- Used for: Editing details of a specific user.
- Return: 
    - If successful: {_id:_id, name:name, email:email, password:password}, 200
    - If not found: {"error":"User with that ID does not exist!"}, 404
    - If required params not given: {"error": "At least one parameter among name, password,email required."}, 400