from celery import Celery
from datetime import timedelta

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0"
)

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False
)

from main import app
from controllers.models import User, Application
from mail import send_email


@celery.task()
def example_task():

    time.sleep(5)
    print("Example task completed!")


@celery.task()
def generate_csv():

    with app.app_context():

        applications = Application.query.all()

        csv_content = "student_id,drive_id,status,application_date\n"

        for a in applications:
            csv_content += f"{a.student_id},{a.drive_id},{a.status},{a.application_date}\n"

        with open("data.csv", "w") as f:
            f.write(csv_content)

        print("CSV generated successfully!")

        send_email(
            "admin@gmail.com",
            "CSV Generation Complete",
            "The CSV file has been generated successfully."
        )


@celery.task()
def send_daily_reminder():

    with app.app_context():

        subject = "Placement Portal Reminder"
        body = "Check placement drives and application deadlines."

        users = User.query.all()

        for user in users:
            send_email(user.email, subject, body)

        print("Reminder emails sent!")


from celery.schedules import crontab

celery.conf.beat_schedule = {

    "daily-reminder": {
        "task": "celery_app.send_daily_reminder",
        "schedule": timedelta(minutes=3),
    }

}