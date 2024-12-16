from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.analysis import analyze_text
from app.suggestions import generate_suggestions  # Import generate_suggestions function
from app.models import TextAnalysisRequest, AnalysisResult

app = FastAPI()

# Jinja2 template rendering
templates = Jinja2Templates(directory="templates")

# Serve static files (optional, remove if not used)
app.mount("/static", StaticFiles(directory="static"), name="static")
# Route to serve the HTML form (GET)
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to analyze the text (POST)
@app.post("/analyze/", response_model=AnalysisResult)
async def analyze(request: TextAnalysisRequest):
    try:
        analysis_results = analyze_text(request.text)
        suggestions_result = generate_suggestions(analysis_results)  # Generate suggestions
        # Combine both the analysis and suggestions into the final response
        final_result = {
            **analysis_results,  # Analysis results
            **suggestions_result  # Suggestions and confidence
        }
        return final_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
