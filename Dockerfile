# ---------- Frontend Build Stage ----------
FROM node:18 AS frontend-build
WORKDIR /app/frontend
    
# Copy only package files first (for caching)
COPY frontend/package*.json ./
RUN npm install
    
# Copy rest of frontend and build
COPY frontend/ .
RUN npm run build
    
# ---------- Backend Stage ----------
FROM python:3.10-slim
WORKDIR /app
    
# Copy and install backend dependencies first
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
    
# Copy backend code and data
COPY backend/ ./backend
COPY student_performance.csv ./
    
# Copy built frontend to backend's static folder
COPY --from=frontend-build /app/frontend/dist ./backend/static

EXPOSE 5000
WORKDIR /app/backend

CMD ["python", "app.py"]
    