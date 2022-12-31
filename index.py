from flask import Flask, request, make_response, jsonify
from models import Mahasiswa

app = Flask(__name__)


@app.route("/mahasiswa", methods=("GET",))
def get_mahasiswa():
    mhs = Mahasiswa(database="database_mahasiswa.db", table="mahasiswa")
    args = request.args

    if len(args) == 0:
        try:
            all_mhs = mhs.query_all()
            response = make_response(all_mhs)
            response.status_code = 200
        except Exception as e:
            response = make_response({
                "pesan"      : "Ada masalah di server!!!",
                "parameter"  : args
            })
            app.logger.error(f"{e}", exc_info=True)
            response.status_code = 500
    elif len(args) == 1 and all(key.strip() in ("id",) for key in args.keys()):
        try:
            result = mhs.query_by_id(_id=int(args["id"]))
            response = make_response(result)
            response.status_code = 200
        except Exception as e:
            response = make_response({
                "pesan"      : "Ada masalah di server!!!",
                "parameter"  : args
            })
            app.logger.error(f"{e}", exc_info=True)
            response.status_code = 500
    else:
        response = make_response({
            "pesan"      : "Bad requests!!!",
            "parameter"  : args
        })

        response.status_code = 400

    return response


@app.route("/mahasiswa", methods=("POST",))
def insert_mahasiswa():
    mhs = Mahasiswa(database="database_mahasiswa.db", table="mahasiswa")
    args = request.args

    if all(key.strip() in ("nama", "nim", "jurusan") for key in args.keys()):
        try:
            mhs.insert(record=args)
            response = make_response({
                "pesan"      : "Sukses!!!",
                "kode status": 201
            })
            response.status_code = 201
        except Exception as e:
            mhs.cursor.close()
            response = make_response({
                "pesan"      : f"{e}",
                "parameter"  : args
            })
            # app.logger.error(f"{e}", exc_info=True)
            response.status_code = 400
    else:
        response = make_response({
            "pesan"      : "Bad requests!!!",
            "parameter"  : args
        })

        response.status_code = 400

    return response


@app.route("/mahasiswa", methods=("PUT",))
def update_mahasiswa():
    mhs = Mahasiswa(database="database_mahasiswa.db", table="mahasiswa")
    args = request.args

    if any(key.strip() in ("id", "nama", "nim", "jurusan") for key in args.keys()):
        try:
            _id = args["id"]
            new_records = dict([(k.strip(), v) for k, v in args.items() if k != "id"])
            mhs.update(new_records=new_records, _id=int(_id))
            response = make_response({
                "pesan"      : "Sukses!!!",
                "kode status": 200
            })
            response.status_code = 200
        except Exception as e:
            response = make_response({
                "pesan"      : f"{e}",
                "parameter"  : args
            })
            # app.logger.error(f"{e}", exc_info=True)
            response.status_code = 404
    else:
        response = make_response({
            "pesan"      : "Bad requests!!!",
            "parameter"  : args
        })

        response.status_code = 400

    return response


@app.route("/mahasiswa", methods=("DELETE",))
def delete_mahasiswa_by_id():
    mhs = Mahasiswa(database="database_mahasiswa.db", table="mahasiswa")
    args = request.args

    if all(key.strip() in ("id",) for key in args.keys()):
        try:
            mhs.delete_by_id(_id=int(args["id"].strip()))
            response = make_response({
                "pesan"      : "Sukses!!!"
            })
            response.status_code = 200
        except Exception as e:
            response = make_response({
                "pesan"      : f"{e}",
                "parameter"  : args
            })
            # app.logger.error(f"{e}", exc_info=True)
            response.status_code = 404
    else:
        response = make_response({
            "pesan"      : "Bad requests!!!",
            "parameter"  : args
        })
        response.status_code = 400

    return response


if __name__ == "__main__":
    app.run(debug=True)
