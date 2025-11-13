# Development Team Project: Coding Output

# Prerequisite

The following software required.
- Docker

# Docker
Deploy containers
```
docker compose up --build -d
```
Remove
```
docker-compose down
```
# Program

publisher.py: Publish random currency data to topic every 1 sec  
subscriber.py: Subscribe topic and display on flask, page refresh every 1 sec

# Console page
Solace: http://localhost:8080/  
<img width="2541" height="720" alt="Image" src="https://github.com/user-attachments/assets/95eac72c-625b-4c30-95ff-2b24893e5d89" />
Solace-exporter: http://localhost:9628/  
<img width="866" height="812" alt="Image" src="https://github.com/user-attachments/assets/0f1eb076-75ed-44e8-89a2-9accd608ed3b" />
Prometheus: http://localhost:9628/  
<img width="936" height="478" alt="Image" src="https://github.com/user-attachments/assets/e14a1f5a-a3c8-4e47-bc1c-dfbd4b4b007a" />
Grafana: http://localhost:3000/  
<img width="2537" height="854" alt="Image" src="https://github.com/user-attachments/assets/f2c9e657-b265-4ea2-8670-409499671b25" />
Publisher log  
<img width="1934" height="156" alt="Image" src="https://github.com/user-attachments/assets/f92e0137-51df-4447-a458-98aa2a2a1075" />
Subscriber: http://localhost:5000/
<img width="487" height="433" alt="Image" src="https://github.com/user-attachments/assets/e033f6b1-6424-4684-8ba3-3c2f77dc62d5" />