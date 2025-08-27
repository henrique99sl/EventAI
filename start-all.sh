#!/bin/bash

# Arranca o backend Flask em background
cd backend
flask run &
BACKEND_PID=$!

# Arranca o frontend Angular em background
cd ../frontend
ng serve &
FRONTEND_PID=$!

# Mensagem de estado
echo "Backend (Flask) a correr com PID $BACKEND_PID"
echo "Frontend (Angular) a correr com PID $FRONTEND_PID"

# Opcional: Espera até Ctrl+C
wait