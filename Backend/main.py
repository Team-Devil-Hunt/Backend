from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware





from router import auth, user, role, admissions, awards, event, equipment, faculty, exams, home, lab
from router import home_quicklinks, contact, projects, events, announcements, lab_bookings, assignments, courses
from router.program import program_router, course_router
from router.project import project_router
from router.schedule import router as schedule_router


app = FastAPI()


@app.get("/ping")
def read_root():
    return {"v": "1"}


origins = [
    "http://localhost:5173",  # Frontend development server
    "http://127.0.0.1:5173",  # Alternative local address
    "http://localhost:3000",  # Another common development port
    "http://localhost:4173",  # Vite preview server
    "http://127.0.0.1:4173",  # Alternative Vite preview address
    # Remove wildcard when using allow_credentials=True
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specific origins only
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"],  # Expose all headers to the browser
)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(role.router)
app.include_router(event.router)
app.include_router(admissions.router)
app.include_router(awards.router)
app.include_router(faculty.router)
app.include_router(exams.router)
app.include_router(equipment.router)
app.include_router(home.router)
app.include_router(home_quicklinks.router)
app.include_router(contact.router)
app.include_router(program_router)
app.include_router(course_router)
app.include_router(courses.router)
app.include_router(project_router)
app.include_router(projects.router)
app.include_router(events.router)
app.include_router(announcements.router)
app.include_router(lab.router)
app.include_router(lab_bookings.router)
app.include_router(schedule_router)
app.include_router(assignments.router)
