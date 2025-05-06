from fastapi import FastAPI, HTTPException

def fake_answer_to_everthing_ml_module(x: float):
    return x*42

ml_models = {}

# Startup command example
async def lifespan(app: FastAPI):
    # Load module
    ml_models['answer_to_everything'] =fake_answer_to_everthing_ml_module
    yield

    # Clean up
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}

