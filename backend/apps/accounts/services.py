from django.conf import settings

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailService:

    @staticmethod
    def send_verification_email(user):

        verification_url = (
            f"http://localhost:8000/api/auth/verify-email/"
            f"{user.email_verification_token}/"
        )

        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=user.email,
            subject="Verify your RepoLens account",
            html_content=f"""
            <h2>Welcome to RepoLens</h2>

            <p>
                Click the link below to verify your email:
            </p>

            <a href="{verification_url}">
                Verify Email
            </a>
            """,
        )

        try:
            sg = SendGridAPIClient(
                settings.SENDGRID_API_KEY
            )

            response = sg.send(message)

            print(
                f"Email sent successfully. "
                f"Status: {response.status_code}"
            )

        except Exception as error:
            print(
                f"Failed to send email: {error}"
            )