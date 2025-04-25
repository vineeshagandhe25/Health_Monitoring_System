from twilio.rest import Client

ACCOUNT_SID = 'your_account_sid'
AUTH_TOKEN = 'your_auth_token'
TWILIO_NUMBER = 'your_twilio_number'
TARGET_NUMBER = 'your_verified_number'

heartbeat = 110      # Normal: 60-100 bpm
steps = 1200         # Normal target: 10,000
calories = 900       # Normal daily intake varies

unhealthy = False
alerts = []

if heartbeat > 100 or heartbeat < 60:
    alerts.append(f"Abnormal heartbeat: {heartbeat} bpm")
    unhealthy = True

if steps < 3000:
    alerts.append(f"Low activity: {steps} steps")
    unhealthy = True

if calories < 1000 or calories > 3000:
    alerts.append(f"Unusual calorie burn: {calories} cal")
    unhealthy = True

if unhealthy:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message_body = "⚠️ Health Alert:\n" + "\n".join(alerts)
    message = client.messages.create(
        body=message_body,
        from_=TWILIO_NUMBER,
        to=TARGET_NUMBER
    )
    print("SMS sent:", message.sid)
else:
    print("✅ All vitals normal. No alert sent.")
