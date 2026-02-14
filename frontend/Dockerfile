# Step 1: Nginx image use karenge jo web files serve karta hai
FROM nginx:alpine

# Step 2: Apni index.html file ko Nginx ke default folder mein copy karenge
COPY index.html /usr/share/nginx/html/index.html

# Step 3: Port 80 open karenge
EXPOSE 80

# Nginx apne aap start ho jata hai, extra command ki zaroorat nahi