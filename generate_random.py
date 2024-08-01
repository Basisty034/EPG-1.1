from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

def generate_random_email(domain="gmail.com"):
    random_letters = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    random_digits = ''.join(random.choice(string.digits) for _ in range(3))
    email_name = random_letters + random_digits
    return f"{email_name}@{domain}"

def generate_random_password(length=12):
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation
    all_characters = letters + digits + symbols
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    command = data.get('command')
    response = process_command(command)
    return jsonify(response)

def process_command(command):
    parts = command.split()
    if command.startswith("generate e!"):
        try:
            count = int(parts[2])
            domain = "gmail.com"
            if len(parts) > 3:
                domain = parts[3].replace("@", "") + ".com"
            emails = [generate_random_email(domain) for _ in range(count)]
            return {"emails": emails}
        except (IndexError, ValueError):
            return {"error": "Invalid command format for generating emails."}
    elif command.startswith("generate p!"):
        try:
            count = int(parts[2])
            length = 12
            if len(parts) > 3:
                length = int(parts[3][1:])
            passwords = [generate_random_password(length) for _ in range(count)]
            return {"passwords": passwords}
        except (IndexError, ValueError):
            return {"error": "Invalid command format for generating passwords."}
    elif command.startswith("Email Fused Password!"):
        try:
            count = int(parts[3])
            emails = [generate_random_email() for _ in range(count)]
            passwords = [generate_random_password() for _ in range(count)]
            return {"emails": emails, "passwords": passwords}
        except (IndexError, ValueError):
            return {"error": "Invalid command format for generating emails and passwords."}
    elif "Fused" in command:
        try:
            email_part = parts[0].replace("Email", "")
            password_part = parts[2].replace("Password", "")
            email_count = int(email_part)
            password_count = int(password_part)
            domain = parts[3].replace("!", "").replace("@", "") + ".com" if len(parts) > 3 else "gmail.com"
            emails = [generate_random_email(domain) for _ in range(email_count)]
            passwords = [generate_random_password() for _ in range(password_count)]
            return {"emails": emails, "passwords": passwords}
        except (IndexError, ValueError):
            return {"error": "Invalid command format for generating emails and passwords."}
    else:
        return {"error": "Unknown command."}

if __name__ == '__main__':
    app.run(debug=True)
