mkdir -p ~/.streamlit/

PORT=8000
echo "\
  [server]\n\
  headless = true\n\
  port = $PORT\n\
  enableCORS = false\n\
  \n\
  " > ~/.streamlit/config.toml

gunicorn -w 3 -k uvicorn.workers.UvicornWorker app:app
