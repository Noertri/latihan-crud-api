from flask import Flask, request, make_response, g
from CRUD import SqliteDB

app = Flask(__name__)
TABLE = "mahasiswa"


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


@app.route("/mahasiswa", methods=["GET", "POST"])
def get_mahasiswa():
    db = SqliteDB(database="database_mahasiswa.db")
    if request.method == "GET":
        db.cursor.execute("SELECT * FROM {0}".format(TABLE))
        all_mhs = db.cursor.fetchall()
        response = make_response(all_mhs)
        response.status_code = 200
    elif request.method == "POST":
        record = request.args
        sql2 = "INSERT INTO {0} ({1}) VALUES ({2});".format(TABLE, ", ".join(record.keys()), ", ".join(["?" for _ in range(len(record))]))
        try:
            db.cursor.execute(sql2, [v for v in record.values()])
            db.commit()
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
