# app
import os
import tempfile
import zipfile
from pathlib import Path

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from controller import load_controller

app = FastAPI(
    title='TradingView Scraper',
    version='1.0.0',
    redoc_url='/127.0.0.1:8000/docs'
)

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post("/api/v1/scrap-scripts/{rul}")
async def scrap_scripts(url: str):
    try:
        print("in try block")
        status = load_controller(url)
        if status:
            data_files = get_files()
            if not data_files:
                return {
                    "status": 400,
                    "message": "data directory is not found"
                }
            return {
                "status": 200,
                "message": "Operation Success",
                "scripted-data": data_files
            }
    except Exception as e:
        data_files = get_files()
        if not data_files:
            return {
                "status": 400,
                "message": "data directory is not found"
            }

        return {
            "status": 500,
            "message": str(e),
            "scripted-data": data_files
        }


def get_files():
    data_directory = 'data'
    dist_path = os.path.join(os.getcwd(), data_directory)
    if not os.path.exists(dist_path):
        return False

    # List all files in the directory and filter PDF files
    data_files = [filename for filename in os.listdir(data_directory) if filename.endswith('.txt')]
    return data_files


# Helper function to create a zip file containing multiple files
def create_zip_archive(file_paths, zip_filename):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                zipf.write(file_path, arcname=os.path.basename(file_path))
    return zip_filename


@app.get("/api/v1/get-extracted-files")
async def get_multiple_files():
    data_files = get_files()
    files_to_return = []
    for file in data_files:
        files_to_return.append(f"data/"+str(file))


    # Create a temporary zip archive containing multiple files
    zip_filename = "multiple_files.zip"
    create_zip_archive(files_to_return, zip_filename)

    # Return the zip archive as a response
    if os.path.exists(zip_filename):
        return FileResponse(zip_filename, headers={"Content-Disposition": f"attachment; filename={zip_filename}"})
    else:
        raise HTTPException(status_code=404, detail="Files not found")
