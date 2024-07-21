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
    # basic authentication header to extract user credentials
    auth = request.authorization
    if not auth:
        return "Missing Credentials", 401

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
            return create_JWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "Invalid Credentials", 401


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
