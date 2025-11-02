# ---------- Frontend Build Stage ----------
    FROM node:18 AS frontend-build
    WORKDIR /app/frontend
    COPY frontend/package*.json ./
    RUN npm install
    COPY frontend/ .
    RUN npm run build
    
    # ---------- Backend Stage ----------
    FROM python:3.10-slim
    WORKDIR /app
    
    # Copy backend files
    COPY backend/ ./backend
    COPY student_performance.csv ./
    
    # Install Python dependencies
    RUN pip install --no-cache-dir -r backend/requirements.txt
    
    # Copy built frontend into backend's static folder
    COPY --from=frontend-build /app/frontend/dist ./backend/static
    
    EXPOSE 5000
    WORKDIR /app/backend
    
    CMD ["python", "app.py"]
    