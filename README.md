FindIt AI 🤖✨

FindIt AI is a full-stack, AI-powered lost and found web application designed to replace the inefficient traditional "lost and found" box. It uses a smart matching system to proactively connect users who have lost an item with users who have found one, and facilitates a secure exchange using a unique QR code verification system.

This project is a complete, end-to-end solution, including a responsive React frontend and a secure Django REST Framework backend.

(Note: You should replace the URL above with a link to a screenshot of your project. I recommend a collage of the Dashboard, Chat Page, and AI Match carousels.)

1. The Problem

Traditional lost and found systems (like a physical box or a logbook) are:

Disorganized: There is no way to search or filter items.

Passive: The person who lost an item must do all the work of manually checking, often with no success.

Insecure: Anyone can claim a valuable item, as there is no way to verify the real owner.

2. The Solution: FindIt AI

FindIt AI solves these problems by providing:

An Intelligent Platform: A central, searchable database for all lost and found items.

Proactive AI Matching: A backend system that automatically compares new reports and notifies users of potential matches.

Secure Communication: A private, real-time chat room for the finder and claimant to coordinate.

Secure Verification: A unique QR code exchange system to prove the item was returned to the correct owner, preventing fraud.

3. Key Features

Full User Authentication: Secure user registration, login, and token-based sessions.

Responsive PWA: Built as a Progressive Web App (PWA), so it's installable on a mobile home screen.

Item Reporting: Easy-to-use forms with image uploads for reporting lost or found items.

Browse & Filter: A public "Browse Items" page with search and category filtering.

AI-Powered Dashboard: A personal dashboard showing:

Your reported items (lost & found).

Your active claims.

Potential AI Matches for your lost items.

Pending claims from others on items you found.

Real-Time Chat: A private chat room (using Firebase) is created for every "accepted" claim.

Secure QR Code Exchange: A unique QR code is generated for the Finder, and the Claimant must scan it with their phone to confirm the exchange, resolving the claim.

Dynamic Landing Page: Features auto-scrolling carousels to showcase successful AI matches and recent reunions.

4. Technology Stack

Backend (The "Engine")

Python 3.12

Django 5

Django REST Framework (DRF): For building all the secure REST APIs.

DRF Token Authentication: For handling user login and sessions.

Django Signals: For the automatic AI matching logic.

Django Filter: For the search and filter functionality.

Frontend (The "User Interface")

React 19

Vite: As the high-speed build tool.

React Router: For all page navigation.

Tailwind CSS: For all styling and responsiveness.

qrcode.react: To generate and display QR codes for the Finder.

html5-qrcode: To use the phone's camera to scan QR codes.

Databases

SQLite 3: The primary database for users, items, and claims.

Firebase Realtime Database: Used exclusively for the real-time chat messages.

5. Getting Started (Installation)

To run this project locally, you will need to run the Backend and Frontend in two separate terminals.

Backend Setup (Django)

Navigate to the backend folder:

cd findit-ai


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # On Windows: .\venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Set up your .env file:
Create a file named .env in the findit-ai (backend) folder and add your credentials:

SECRET_KEY=your-django-secret-key
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-16-digit-google-app-password


Run database migrations:

python manage.py makemigrations
python manage.py migrate


Create a superuser (for admin access):

python manage.py createsuperuser


Run the server:

# Run this to allow mobile testing
python manage.py runserver 0.0.0.0:8000


Your backend is now running at http://127.0.0.1:8000/

Frontend Setup (React)

Navigate to the frontend folder (in a new terminal):

cd frontend


Install dependencies:

npm install


Set up Firebase:

Go to the Firebase Console and create a new project.

Create a Realtime Database.

Find your Firebase config credentials.

In the src folder, create a file named firebaseConfig.js and paste your credentials into it.

Set up your development environment file:
Create a file named .env.development in the frontend folder and add the IP address of your computer (so your mobile phone can connect to the backend):

VITE_API_URL=[http://192.168.1.10:8000](http://192.168.1.10:8000) 
# (Replace with your computer's actual IP address)


Run the server:

npm run dev


Your frontend is now running at http://localhost:5173/
