# Backend

## Simple API for Image Analysis.

Basically, the API allows uploads of images, then calls OpenAI's 
Vision Preview API, and sends responses to the frontend. 
The API validates and stores images for training, alongside 
OpenAI's responses. Images are processed into 128x128 
thumbnails (aspect ratio preserved) and 512x512 square images 
(non-square images have black-filled backgrounds). 
Original images are compressed into zip files for local storage 
and then deleted from the server. Thumbnails reference the 
external API response; 512x512 images aid in model training.


*Any further technical details can be found in the code.*


## Installation

```bash

# Install dependencies
$ pip3  install -r requirements.txt
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver

```

# Developer Notes 

## API Key

The API Key is stored in Dockerfile environment variable. There are
two keys, the one marked 'OPENAI_API_KEY_1' is the correct one. The other one is for 
testing purposes. In the zip file the api keys are still there,
but they are not present in the GitHub repo.

## Endpoints


### /api/thumbnails/{file_name}
#### (GET)
returns a thumbnail image || 404
```
/api/thumbnails/thumbnail_aiv_aaa_sample.png - (Sample Image) 
```
----

### /api/health/status 
#### (GET)
returns a 200 status code if the server is running

----
### /api/images/analyze-image 
#### (POST)
```
params: uploaded_file (file)
```

Developer Note :
This endpoint can return various status codes.
The status codes are as follows:
- 200 - Success
- 400 - Bad Request (Invalid File)
- 401 - Unauthorized (Invalid API Key)
- 500 - Internal Server Error (OpenAI API Error)



*If openai returns an error code, the error
returned to front end may be 200 due to the fact the
image was uploaded successfully... on this case
the error will be present and handled in the front end.*

Success Upload and OpenAI Success
```
response = {
   "message": "Image uploaded successfully",
  "thumbnail": "/uploads/thumbnails/thumbnail_aiv_aaa_sample.png",
  "openai_response": {SEE SAMPLE IN CODE BACKEND/API/CONSTANTS.PY}
}
```
Success Upload but OpenAI Error
```
  response = {
  "message": "Image uploaded successfully",
  "thumbnail": "/uploads/thumbnails/thumbnail_aiv_aaa_sample.png",
    "openai_response":
      {"error":
          {"message": "Incorrect API key provided: .....",
            "type": "invalid_request_error", // this is the error type
            "param": null,
            "code":
              "invalid_api_key"
          }
      }
  }
```

----



