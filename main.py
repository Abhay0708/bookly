from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
# this code is for only for restFox Ui
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins for development/testing
    allow_credentials=True,     # Allow cookies and authentication headers
    allow_methods=["*"],        # Allow all HTTP methods including OPTIONS
    allow_headers=["*"],        # Allow all headers
)
@app.get("/")
async def read_root():
    return {"Hello": "World"}

#path parameter
@app.get("/great/{name}")
async def read(name:str):
    return {"name":f"hello {name}"}

#Query parameter

@app.get("/great")
async def read_query(name:str) ->dict:
    return {"name":f"hello {name}"}

#both para and query
@app.get("/greet/{name}")
async def read_para_query(name:str,age:int) -> dict:
    return {"message":f"hello my name is {name} I am {age} year old"}

