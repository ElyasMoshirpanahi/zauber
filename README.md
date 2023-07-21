# Generative AI Frontend and Backend for [Zauber](https://zauber.com) 

Goddess of Ice and Water   |  Peacful Land
:-------------------------:|:-------------------------:
![alt text](Q1.jpg)  |  ![alt text](Q2.jpg)
-------------------------------------------------------


This project involved developing a frontend interface and backend API for interacting with generative AI models. The main challenges included:

- Implementing a user-friendly interface for composing image generation prompts
- Integrating with backend API endpoints for submitting requests 
- Handling pre-processing and validation of request data
- Enabling cross-origin requests between frontend and backend
- Parsing and encoding request data properly for the ML models
- Displaying API response images and handling errors 


## Getting Started

To run the project locally:

### Frontend

The frontend is built with Nuxt.js. To install dependencies and start the dev server:

```
cd  nuxt.js
npm install
npm run dev
```

The app will start by default on http://localhost:3000.

### Backend

The backend exposes API endpoints built with Azure functions. To install:

```
cd  CORS
bash deploy.sh
```

This will start the Function runtime  by default  on http://localhost:7071.

## Frontend Architecture

The frontend allows users to compose image generation with 4 different pipelines such as :

- Text/Image to Image
- Controlnet Text/Image  to Image


Along with various options such as :

- Text prompt
- Negative prompt
- Image size
- Number of inference steps
- Guidance scale


Technoliges that were used here:

- Nuxt.js for UI and routing
- Vuetify component library
- Axios for API calls
- Form handling and validation
- Bootstrap for styling 

The image generation options are submitted to the backend API. The response image is displayed back to the user.

## Backend Architecture

The backend handles requests from the frontend and routes them to the actual ML model endpoints. It uses:

- Azure functions with Python runtime
- CORS enabled on all endpoints
- Validation and sanitization of request data
- Python requests module for outgoing API calls
- Multipart form data parsing
- Input data encoding to base64 when needed


## Key Challenges

- **CORS errors** - CORS had to be enabled on backend to allow cross-origin requests from frontend along with many testings for the right parameters.

- **Data encoding** - Some model endpoints required base64 encoding and decoding data. This was handled in the backend before forwarding requests and handeled before rendering.

- **Multipart forms** - Request data, images etc were sent as multipart form data. The backend parses these requests before reading the fields.

- **Validation and sanitization** - User data is validated and cleaned to prevent errors and issues before sending requests to ML endpoints.

## Next Steps

Some possible improvements for the future :

TODO:
- Containerization with Docker          [✓] 
- Additional models and features        []
- User authentication  	       		    []
- Deploy to production servers          []
- CI/CD pipelines and automated testing []


## Deployment and CI/CD

The backend API has been configured to be easily deployable using Docker containers. A Dockerfile is provided that packages the Azure functions and dependencies into a container image.

Containerized deployment improves portability, allows scaling using orchestrators like Kubernetes, and standardizes environments across dev/test/prod.

For later CI/CD, GitHub Actions workflows can be added in the future to enable:

- Running automated tests on code changes
- Building backend and frontend artifacts
- Pushing Docker images to a container registry  
- Deploying updates automatically

These best practices enable quick and reliable delivery of changes through standardized pipelines. Test coverage provides confidence in releases.


Please note that , this project requires endpoint and api key to be up and running which is currently provided and restriced access to staff only, Good luck!



## Contributing

Contributions to improve the project are welcome! Please open issues or pull requests on GitHub with any enhancements.

Some areas that could be improved:

- Adding more generative AI models
- Increasing test coverage
- Optimizing backend performance
- Implementing lightweight user accounts

## License

This project is released under the [MIT license](https://choosealicense.com/licenses/mit/). Feel free to use and modify the code for your own projects.
