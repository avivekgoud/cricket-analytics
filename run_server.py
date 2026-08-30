"""
CricIntel Pro - Server Launcher
Runs FastAPI backend + Frontend SPA on port 8000
"""
import uvicorn

if __name__ == '__main__':
    print('='*60)
    print('Starting CricIntel Pro Cricket Analytics Platform...')
    print('FastAPI + Modern SPA running at: http://localhost:8000')
    print('Interactive API Docs at: http://localhost:8000/docs')
    print('To run Streamlit UI simultaneously: streamlit run app.py')
    print('='*60)
    uvicorn.run('backend.main:app', host='0.0.0.0', port=8000, reload=False)
