from fastapi import FastAPI
import os

app = FastAPI()

@app.get('/debug/source')
def debug():
    return {
        'file': __file__,
        'cwd': os.getcwd()
    }
