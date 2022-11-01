mkdir -p ~/.streamlit/

PORT=8000
echo "\
  [server]\n\
  headless = true\n\
  port = $PORT\n\
  enableCORS = false\n\
  \n\
  " > ~/.streamlit/config.toml
