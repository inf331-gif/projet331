from fastapi import FastAPI
from shared_libs.utils.config_manager import ConfigManager

config = ConfigManager.get_service_config("users-service")

app = FastAPI(title=config["SERVICE_NAME"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": config["SERVICE_NAME"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config["SERVICE_PORT"])