from fastapi import FastAPI

from app.api.routes import auth, parser, projects, search, skills, teams

app = FastAPI(
    title="Team Finder API",
    description="Платформа для поиска людей в команду (ЛР3 — Docker + Celery).",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(skills.router)
app.include_router(projects.router)
app.include_router(teams.router)
app.include_router(search.router)
app.include_router(parser.router)


@app.get("/", tags=["Служебные"])
def root() -> dict:
    return {"app": "Team Finder API", "status": "ok", "docs": "/docs"}
