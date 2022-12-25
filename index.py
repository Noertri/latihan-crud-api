from flask import Flask, request, make_response
from CRUD import SqliteDB

app = Flask(__name__)


@app.route("/mahasiswa", methods=["GET", "POST"])
def get_mahasiswa():
    db = SqliteDB(database="database_mahasiswa.db")
    if request.method == "GET":
        all_mhs = db.query_all(tablename="mahasiswa")
        response = make_response(all_mhs)
        response.status_code = 200
    elif request.method == "POST":
        new_mhs = request.get_json()
        response = "Succes!!!"
    else:
        response = ("Bad request", 404)

    return response


if __name__ == "__main__":
    app.run(debug=True)
