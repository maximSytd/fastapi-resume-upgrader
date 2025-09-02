from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

view_router = APIRouter()


@view_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Redirect on login page or resumes list."""
    return templates.TemplateResponse("base.html", {"request": request})


@view_router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Render the registration page."""
    return templates.TemplateResponse("register.html", {"request": request})


@view_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render the login page for user authentication."""
    return templates.TemplateResponse("login.html", {"request": request})


@view_router.get("/resumes", response_class=HTMLResponse)
async def resumes_page(request: Request):
    """Render the resumes list page."""
    return templates.TemplateResponse("resumes.html", {"request": request})


@view_router.get("/resumes/{resume_id}", response_class=HTMLResponse)
async def resume_detail_page(request: Request, resume_id: int):
    """Render the resume details page for a specific resume."""
    return templates.TemplateResponse(
        "resume_detail.html",
        {
            "request": request,
            "resume_id": resume_id,
        },
    )
