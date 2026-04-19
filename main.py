from datetime import date

def extract_login_domain(address: str) -> tuple[str, str]:
    return address.split("@")[0], address.split("@")[1]

def clean_body_text(body: str) -> str:
    if not body:
        return ""
    return " ".join(body.split())

def mask_sender_email(login: str, domain: str) -> str:
    return login[:2] + "***@" + domain


def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "body": body,
    }


def add_send_date(email: dict) -> dict:
    email["date"] = date.today().strftime("%Y-%m-%d")
    return email


def add_short_body(body: str) -> str:
    return body[:10] + "..."


def build_sent_text(email: dict) -> str:
    return (
        f"Кому: {email['masked_recipient']}, от {email['masked_sender']}\n"
        f"Тема: {email['subject']}, дата {email['date']}\n"
        f"{email['short_body']}"
    )


def normalize_addresses(value: str) -> str:
    return value.lower().strip()


def check_empty_fields(subject: str, body: str) -> tuple[bool, bool]:
    return subject.strip() == "", body.strip() == ""


def get_correct_email(email_list: list[str]) -> list[str]:
    result = []

    for email in email_list:
        cleaned = email.strip().lower()

        if cleaned.count("@") != 1:
            continue

        login, domain = cleaned.split("@")

        if not login or not domain:
            continue

        if not domain.endswith((".com", ".ru", ".net")):
            continue

        result.append(cleaned)

    return result


def sender_email(
    recipient_list: list[str],
    subject: str,
    message: str,
    *,
    sender="default@study.com"
) -> list[dict]:

    sender = normalize_addresses(sender)
    recipients = get_correct_email(recipient_list)

    recipients = [r for r in recipients if r != sender]

    if not recipients:
        return []

    is_empty_subject, is_empty_body = check_empty_fields(subject, message)
    if is_empty_subject or is_empty_body:
        return []

    cleaned_subject = clean_body_text(subject)
    cleaned_body = clean_body_text(message)

    login, domain = extract_login_domain(sender)
    masked_sender = mask_sender_email(login, domain)

    result = []

    for recipient in recipients:
        login_r, domain_r = extract_login_domain(recipient)
        masked_recipient = mask_sender_email(login_r, domain_r)
        email = create_email(
            masked_sender,
            recipient,
            cleaned_subject,
            cleaned_body
        )

        email = add_send_date(email)

        email["masked_sender"] = masked_sender
        email["masked_recipient"] = masked_recipient
        email["short_body"] = add_short_body(email["body"])
        email["sent_text"] = build_sent_text(email)

        result.append(email)

    return result

result = sender_email(
    ["admin@company.ru", "user@gmail.com"],
    "Hello!",
    "Привет, коллега!"
)

for email in result:
    print(email["sent_text"])
    print("-" * 40)