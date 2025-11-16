from flask import Blueprint, render_template, request, redirect, url_for, current_app
from pathlib import Path

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def index():
    return render_template("upload.html")

@main_bp.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        # No file? Just go back to index.
        return redirect(url_for("main.index"))

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    file_path = upload_folder / uploaded_file.filename
    uploaded_file.save(file_path)

    return f"Uploaded {uploaded_file.filename} to {file_path}"