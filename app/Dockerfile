FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY priors.py investability_v2.py streamlit_app.py fkin_lookup.npz ./
ENV PORT=8080
EXPOSE 8080
CMD streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
