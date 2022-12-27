from flask import Flask, request, make_response, g
from models import DatabaseMahasiswa

app = Flask(__name__)
TABLE = "mahasiswa"


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def are_args_valid(args):
    keys = [key.strip() for key in args.keys()]
    if "nama" in keys and "nim" in keys and "jurusan" in keys:
        return True


@app.route("/mahasiswa", methods=["GET", "POST"])
def get_mahasiswa():
    db = DatabaseMahasiswa(database="database_mahasiswa.db", logger=app.logger)
    args = request.args
    method = request.method
    if method == "GET" and len(args) == 0:
        try:
            all_mhs = db.query_all(tablename=TABLE)
            response = make_response(all_mhs)
            response.status_code = 200
        except Exception as e:
            response = make_response("Ada masalah di server!!!")
            app.logger.error(f"{e}")
            response.status_code = 500
            db.close()
    elif method == "POST" and are_args_valid(args):
        try:
            db.insert(tablename=TABLE, record=args)
            response = make_response("Success!!!")
            response.status_code = 201
        except Exception as e:
            response = make_response("Ada masalah di server!!!")
            app.logger.error(f"{e}")
            response.status_code = 500
            db.close()
    else:
        response = ("Bad request", 404)
        db.close()

    return response


if __name__ == "__main__":
    app.run(debug=True)
