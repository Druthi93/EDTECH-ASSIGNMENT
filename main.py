from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers import users, assignments, submissions
from database import Base, engine

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("static/index.html")

@app.get("/teacher")
async def teacher_dashboard():
    return FileResponse("static/view.html") 

@app.get("/student", response_class=FileResponse)
async def student_page():
    return FileResponse("static/submit.html")

@app.get("/create-assignment", response_class=FileResponse)
async def create_assignment_page():
    return FileResponse("static/create.html")


app.include_router(users.router, prefix="/users")
app.include_router(assignments.router)
app.include_router(submissions.router)


Base.metadata.create_all(bind=engine)
