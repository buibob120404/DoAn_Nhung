import cv2
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# ==================== CONFIG (EDIT THESE 3 LINES) ====================
EMAIL_SENDER = "buibob051@gmail.com"
EMAIL_PASSWORD = "your_16_char_app_password"
EMAIL_RECEIVER = "bob.ckcn.k22@gmail.com"

# --- Camera and file settings ---
CAMERA_ID = 0                # Try 0 first; if not, try 1
FOLDER_NAME = "Do_An"        # Folder to save image
IMAGE_NAME = "anh_chup_tu_pi.jpg"
EMAIL_SUBJECT = "Anh chup moi tu Raspberry Pi 5!"
# Build full path, e.g. "Do_An/anh_chup_tu_pi.jpg"
IMAGE_FILE_NAME = os.path.join(FOLDER_NAME, IMAGE_NAME)
# ====================================================================

def capture_image() -> bool:
    """Capture one frame and save it."""
    # Ensure folder exists
    if not os.path.exists(FOLDER_NAME):
        print(f"Folder {FOLDER_NAME} not found. Creating ...")
        os.makedirs(FOLDER_NAME)

    print(f"Start capturing from camera ID {CAMERA_ID} ...")
    cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_V4L2)

    if not cap.isOpened():
        print(f"ERROR: Cannot open camera ID {CAMERA_ID}.")
        return False

    print("Camera connected. Waiting 2 seconds to stabilize ...")
    time.sleep(2)

    ret, frame = cap.read()
    if not ret:
        print("ERROR: Cannot read frame from camera.")
        cap.release()
        return False

    # Save image to specified path (e.g., Do_An/anh_chup_tu_pi.jpg)
    cv2.imwrite(IMAGE_FILE_NAME, frame)
    print(f"Captured OK! Saved to: {IMAGE_FILE_NAME}")

    cap.release()
    print("Camera closed.")
    return True

def send_email():
    """Send an email with the captured image attached."""
    print(f"Preparing to send email from {EMAIL_SENDER} to {EMAIL_RECEIVER} ...")
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = EMAIL_SUBJECT

        body = "This image was sent automatically from Raspberry Pi 5."
        msg.attach(MIMEText(body, "plain"))

        # Attach the image from the correct path
        print(f"Attaching file: {IMAGE_FILE_NAME}")
        with open(IMAGE_FILE_NAME, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        # Use IMAGE_NAME for attachment filename
        part.add_header("Content-Disposition", f"attachment; filename={IMAGE_NAME}")
        msg.attach(part)

        print("Connecting to Gmail SMTP ...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        print("Logging in ...")
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {EMAIL_RECEIVER}!")

    except Exception as e:
        print(f"ERROR while sending email: {e}")

# --- Main ---
if __name__ == "__main__":
    if capture_image():
        send_email()
    else:
        print("Capture failed. Email will not be sent.")
