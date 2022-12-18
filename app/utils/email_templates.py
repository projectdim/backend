from app.core.config import settings


def return_template(template_type: str, *, link: str = None) -> dict:

    templates = {
        "invite": {
            "subject": "Invitation to the platform.",
            "html":
                """
                <html>
                    <head></head>
                    <h1>Project DIM invitation.</h1>
                    <p>Someone has invited you to join the <a href='{}'> DIM platform. </a></p>
                    <p>To complete the registration, please follow this <a href='{}'> link </a></p>
                    <p>It will expire in 24 hours.</p>
                </html>    
                """.format(settings.DOMAIN_ADDRESS, link),
            "text": "Project dim invitation."
        },
        "password-renewal": {
            "subject": "Password renewal.",
            "html":
                """
                <html>
                    <head></head>
                    <h1>Project DIM password renewal.</h1>
                    <p>Someone has requested a password renewal for your account at <a href='{}'> DIM platform. </a></p>
                    <p>If it was not you, please ignore this message.</p>
                    <p>To reset your password, please follow this <a href='{}'> link </a></p>
                    <p>It will expire in 24 hours.</p>
                </html>    
                """.format(settings.DOMAIN_ADDRESS, link),
            "text": "Project dim password renewal"
        }
    }

    return templates[template_type]
