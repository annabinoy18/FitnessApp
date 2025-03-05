from apscheduler.schedulers.blocking import BlockingScheduler
from send_email import send_email
from database_service import get_all_users, get_workout_today

scheduler = BlockingScheduler()

def send_daily_workouts():
    """Fetch workout & send emails to all users."""
    workout = get_workout_today()
    if not workout:
        print("No workout found for today.")
        return

    users = get_all_users()
    subject = "Your Daily Workout"
    body = f"Today's Workout: {workout[0]['title']} - https://youtu.be/{workout[0]['video_id']}"

    for user in users:
        send_email(user, subject, body)
        print(f"📧 Sent to {user}")

# Schedule the job to run at 1:00 AM daily
scheduler.add_job(send_daily_workouts, 'cron', hour=1, minute=55)

if __name__ == "__main__":
    print("📅 Daily Email Scheduler Started...")
    scheduler.start()
