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
        try:
            db.insert("mahasiswa", **new_mhs)
            response = make_response("<h1>Success!!!</h1>")
            response.status_code = 201
        except Exception as e:
            response = make_response(f"<h1>Ada masalah di server!!!</h1>")
            print(f"{e}")
            response.status_code = 500
    else:
        response = ("Bad request", 404)

    return response


if __name__ == "__main__":
    app.run(debug=True)
