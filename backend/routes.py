from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture is None:
        return "Picture with id {id} not found", 404
    return jsonify(picture), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()

    if not picture or "id" not in picture or "pic_url" not in picture:
        return jsonify({"message": "Invalid picture data"}), 400

    if any(item["id"] == picture["id"] for item in data):
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture = request.get_json()
	
    if not updated_picture or "pic_url" not in updated_picture:
        return jsonify({"message": "Invalid picture data"}), 400

    for picture in data:
        if picture["id"] == id:
            picture.update(updated_picture)
            return jsonify({"message": "Picture updated successfully", "picture": picture}), 200

    return jsonify({"message": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = next((item for item in data if item['id'] == id), None)
    if picture:
        data.remove(picture)
        return '', 204
    else:
        return jsonify({"message": "picture not found"}), 404
