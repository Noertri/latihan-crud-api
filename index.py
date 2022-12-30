from flask import Flask, request, make_response
from models import DatabaseMahasiswa

app = Flask(__name__)
TABLE = "mahasiswa"


@app.route("/mahasiswa", methods=["GET", "POST", "DELETE", "PUT"])
def get_mahasiswa():
    db = DatabaseMahasiswa(database="database_mahasiswa.db")
    args = request.args
    method = request.method
    # response = make_response()
    if method == "GET" and len(args) == 0:
        try:
            all_mhs = db.query_all(tablename=TABLE)
            response = make_response(all_mhs)
            response.status_code = 200
        except Exception as e:
            response = make_response({
                "pesan"      : "Ada masalah di server!!!",
                "kode status": 500,
                "parameter"  : args
            })
            app.logger.error(f"{e}", exc_info=True)
            response.status_code = 500
    elif method == "POST" and all(key.strip() in ("nama", "nim", "jurusan") for key in args.keys()):
        try:
            db.insert(tablename=TABLE, record=args)
            response = make_response({
                "pesan"      : "Sukses!!!",
                "kode status": 201
            })
            response.status_code = 201
        except Exception as e:
            db.cursor.close()
            response = make_response({
                "pesan"      : f"Ada masalah di server!!!. {e}",
                "kode status": 500,
                "parameter"  : args
            })
            # app.logger.error(f"{e}", exc_info=True)
            response.status_code = 500
    elif method == "PUT" and any(key.strip() in ("id", "nama", "nim", "jurusan") for key in args.keys()):
        try:
            _id = args["id"]
            new_records = dict([(k.strip(), v) for k, v in args.items() if k != "id"])
            db.update(tablename=TABLE, new_records=new_records, _id=int(_id))
            response = make_response({
                "pesan"      : "Sukses!!!",
                "kode status": 200
            })
            response.status_code = 200
        except Exception as e:
            response = make_response({
                "pesan"      : f"Ada masalah di server!!!. {e}",
                "kode status": 500,
                "parameter"  : args
            })
            # app.logger.error(f"{e}", exc_info=True)
            response.status_code = 500
    elif method == "DELETE" and all(key.strip() in ("id",) for key in args.keys()):
        try:
            db.delete_by_id(tablename=TABLE, _id=int(args["id"].strip()))
            response = make_response({
                "pesan"      : "Sukses!!!",
                "kode status": 200
            })
            response.status_code = 200
        except Exception as e:
            response = make_response({
                "pesan"      : f"Ada masalah di server!!!. {e}",
                "kode status": 500,
                "parameter"  : args
            })
            # app.logger.error(f"{e}", exc_info=True)
            response.status_code = 500
    else:
        response = make_response({
            "pesan"      : "Bad requests!!!",
            "kode status": 404,
            "parameter"  : args
        })
        response.status_code = 404

    return response


if __name__ == "__main__":
    app.run(debug=True)
