from config import settings
import uvicorn


def main():
    uvicorn.run(
        app="server.server:app",
        host=settings.app_host,
        port=settings.port,
        reload=settings.reload,
        workers=settings.workers,
    )


if __name__ == "__main__":
    main()
