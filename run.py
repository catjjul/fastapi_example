import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "src.app.app:app"
        , reload=True
        , port=8080
        , host='127.0.0.1'
    )
