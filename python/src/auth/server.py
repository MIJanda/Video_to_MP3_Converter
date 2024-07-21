import jwt
import datetime
import os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


@server.route("/login", methods=["POST"])
def login():
    # basic authentication header to extract user credentials, i.e. username and password
    auth = request.authorization
    if not auth:
        return "Missing Credentials!", 401

    # check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid Credentials", 401
        else:
            # return a JWT to be used by the user to make requests to the API
            return create_JWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "Invalid Credentials!", 401


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Missing Credentials!", 401

    # NB. in prod. check for the authentication scheme type: encoded_jwt.split(" ")[0]
    # extract the token
    encoded_token = encoded_jwt.split(" ")[1]

    try:
        decoded_token = jwt.decode(
            encoded_token, os.environ.get("JWT_SECRET"), algorithm=["HS256"]
        )
    except:
        return "Not Authorized!", 403

    return decoded_token, 200


def create_JWT(username, secret, is_admin):
    now = datetime.datetime.utcnow()
    # JWT expires after 1 day
    expiry = now + datetime.timedelta(days=1)
    return jwt.encode(
        {
            "username": username,
            "exp": expiry,
            "iat": now,  # issued at
            "admin": is_admin,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    # listen to requests on all public IPs
    server.run(host="0.0.0.0", port=5000)
