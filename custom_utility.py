from flask import jsonify

### Programmer defined utility functions
def utility_pythonify(user):
    """
        Utility function to convert object in database into python dictionary.
    """
    _id,name,email,password = str(user["_id"]),user["name"],user["email"],user["password"]
    u = {"id":_id, "name":name, "email":email, "password":password}
    return u

def success_200(response):
    """
        Returns the response on success and code 200.
    """
    return jsonify(response),200

def error_404_not_found():
    """
        Returns an error not found message and code 404.
    """
    return jsonify({"error":"User with that ID does not exist!"}),404

def error_400_bad_request(msg):
    """
        Returns a custom error message and code 400.
    """
    return jsonify({"error":msg}),400

def error_409_conflict(msg):
    """
        Returns a custom error message and code 409.
    """
    return jsonify({"error":msg}),409

