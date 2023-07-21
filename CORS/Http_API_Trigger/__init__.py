import logging
import azure.functions as func
import requests
import json
import io
import azure.functions as func
from datetime import datetime as dt
import base64
from ZAUBER import API,ENDPOINT

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')



    body = req.form.get("data") # is always a json object
    data=json.loads(body)
    input_image = base64.b64decode(req.form['input_image'].replace("data:image/png;base64,","")) if req.form.get('input_image') else req.files['input_image'].filename if req.files.get('input_image') else None

    conditioning_image = base64.b64decode(req.form['conditioning_image'].replace("data:image/png;base64,","")) if req.form.get('conditioning_image') else req.files['conditioning_image'].filename if req.files.get('conditioning_image') else None


    logging.info(data)
    # return func.HttpResponse("multi form data collected!", status_code=200)


    logging.info(f"Sent files are : {len(req.files)}")

    # if len(req.files) > 0:
    #     # try:
    #     #     input_image =req.files.get('input_image').filename   if req.files.get('input_image').filename != '' else None
    #     #     conditioning_image =req.files.get('conditioning_image').filename  if req.files.get('conditioning_image').filename != '' else None
            
    #     #     logging.info(f"input file is :{input_image}")
    #     #     logging.info(f"conditioning_image file is :{conditioning_image}")

    #     # except Exception as e:
    #     #     logging.info(f"Error for fecthing files : {e.args}")
    # else:
    #     pass
    #     # logging.info("0 files where recieved ")

    if not data:
        try:
            req_body = req.get_json()
            
        except ValueError:
            pass
        else:
            data = req_body.get('data')

    if data:
        
        endpoint_url = ENDPOINT 
        api_key      = API


        try:
            # logging.info("Got the info for the request:")
            # logging.info(data)
            # logging.info(type(data))
            output_bytes,status_code = perform_request(data=data, 
                                                       endpoint_url=endpoint_url,
                                                       input_image= input_image, 
                                                       conditioning_image=conditioning_image, 
                                                       api_key=api_key)

            # Return response with CORS headers
            headers = {
                "Access-Control-Allow-Origin": "http://localhost:3000", # or specific origin,
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Origin, Content-Type, Accept" ,
                "Content-Type": "image/png"   
                }
            
            logging.info(status_code)
            
            # png_data is the binary data
            base64_img = base64.b64encode(output_bytes).decode('utf-8')
            return func.HttpResponse(base64_img, status_code=status_code, headers=headers)



        except Exception as e:
            return func.HttpResponse(str(e), status_code=500)

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a query string or in the request body for a personalized response.",
             status_code=200
        )



def clean_data(data:dict)->dict:
  cleaned = {}
  for key,value in data.items():
    if value is not None and value != "" and value != "undefined":
      cleaned[key] = value

  return cleaned



def perform_request(
    data: dict, 
    endpoint_url: str,
    input_image: str = None,
    conditioning_image: str = None,
    deployment_name: str = "blue",
    api_key: str = None,
    save_png:bool=True
) -> None:

    """
    Read request json, perform the call to the endpoint, and return the result

    Parameters
    ----------
    data : dict
        The request parameters
        
    endpoint_url : str
        The url endpoint
        
    input_image : str, optional
        The path to the input image, used in `image to image` requests
        Defaults to None

    conditioning_image : str, optional 
        The path to conditioning image, used in `controlnet` requests
        Defaults to None

    deployment_name : str, optional
        The name of the deployment. Only necessary with remote deployment.
        Defaults to "blue".

    api_key : str
        The API key used to connect to a remote endpoint. If this method is used with 
        a local endpoint, it can be omitted.
        Defaults to None.
    """
    
    clean_base_url = endpoint_url.replace("score", "")
    url = f"{clean_base_url}/score"

    # set headers
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        headers["azureml-model-deployment"] = deployment_name


    logging.info(f"Data before clearning :\n {data}")

    #Clearning the data before parse it as json 
    data = clean_data(data)

    logging.info(f"Data after clearning :\n {data}")



    # set request files
    files = {
        "data": json.dumps(data),
        "input_image": open(input_image, "rb").read() if isinstance(input_image, str) else input_image if isinstance(input_image, bytes) else None,
        "conditioning_image": open(conditioning_image, "rb").read() if isinstance(conditioning_image, str) else conditioning_image if isinstance(conditioning_image, bytes) else None,

    }

    logging.info(type(files["input_image"]))
    # perform request
    result = requests.post(
        url,
        files=files,
        headers=headers,
        verify=False, # noqa: S501
        timeout=60,
    )
    


    if result.status_code == 200:
        print("Response status code ",result.status_code)


        if save_png:
            output_bytes = io.BytesIO(result.content).getvalue()


            logging.info(files["data"])
            image_type =json.loads(files["data"])["type"]
            image_name = str(dt.strftime(dt.now(),"%Y-%m-%d %H-%M-%S"))
            output_image = f"{image_type}_{image_name}.png"
            

            with open(output_image, "wb") as output_file:
                output_file.write(output_bytes)
            

    
        
    else:
        print(f"Error: {result.reason} - {result.text}")
        output_bytes=0
        output_image = ''
    
    
    

    print(
        f"Endpoint processing time: {result.headers.get('processing-time-ms')} ms",
    )
    
    return output_bytes,result.status_code

