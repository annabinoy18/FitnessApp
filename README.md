*The Fitness App is a web-based platform that helps users stay consistent with their workouts by sending them daily workout video recommendations via email. Users can sign up, add workout videos, manage their workout list, and receive a new workout video every day in their inbox.*

*Tech Stack*:
Frontend & UI: Streamlit (Python-based web framework)
Backend & Database: Python, MongoDB (NoSQL)
Email Service: Gmail SMTP (for sending daily workout emails)
API Integration: YouTube API (to fetch video details from user-input URLs)

*Key Features*
1️⃣ User Authentication (Signup & Login)
Users can sign up using their email and password.
Registered users can log in using their credentials instead of signing up every time.
This authentication system ensures user-specific workout tracking.
2️⃣ Workout Management
Users can add workouts by pasting a YouTube video URL.
The app automatically extracts the video title, duration, and channel name using the YouTube API.
Users can view all stored workouts in a structured format.
The app allows users to delete workouts they no longer need.
3️⃣ Daily Workout Recommendation
Every day, the app selects a random workout from the stored database.
Users have the option to change the recommended workout manually.
The selected workout is stored as "Today's Workout" in the database.
4️⃣ Automated Email System (Using Gmail SMTP, Not SendGrid)
The app sends a daily email containing the selected workout video link.
This ensures users receive a new workout reminder every day.
Gmail SMTP is used instead of SendGrid for handling email delivery.
The system can handle multiple users, sending personalized emails to each registered user.
Database Structure (MongoDB Collections)
The database is designed to efficiently store users and workout data:

*Collection Name	Purpose*
-users_collection	Stores user emails & passwords for authentication.
-workouts_collection	Stores workout details (title, duration, video ID, etc.).
-workout_today_collection	Stores the currently selected workout of the day.

*Why This Project is Valuable?*
✅ Encourages fitness consistency by providing daily reminders.
✅ Personalized experience by allowing users to manage workouts.
✅ Automation saves time by reducing manual tracking of workouts.
✅ Practical implementation of Python, APIs, MongoDB, and SMTP services.
