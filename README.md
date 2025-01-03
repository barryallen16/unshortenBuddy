# **Unshorten Buddy** 🚀

Unshorten Buddy is your friendly Telegram bot that effortlessly unshortens URLs, bypassing ads and timers to reveal direct links. Whether you're dealing with `tnshort`, `krownlinks`, or other similar services, 
Unshorten Buddy is here to simplify your online experience. Fast, secure, and user-friendly, it’s the perfect tool for anyone tired of clicking through endless redirects.
Built with Python, Selenium, and PostgreSQL.

## **Demo video**
https://github.com/user-attachments/assets/d7c88ff9-a4d6-4cfb-a2f9-a3b9bd0aae7a


---

## **Features** ✨

- **Unshorten Links Instantly**: Get direct links in seconds.
- **Bypass Ads and Timers**: No more waiting or clicking through ads.
- **Admin Controls**: Easily manage user access with admin commands.
- **Secure and Private**: Your privacy is our priority.
- **Open-Source**: Fully transparent and customizable.

---

## **Setup Instructions** 🛠️

### **Prerequisites**
- A Linux-based system (e.g., Ubuntu).
- Python 3.8 or higher.
- A Telegram bot token (get it from [@BotFather](https://core.telegram.org/bots#botfather)).
- A PostgreSQL database (optional, for logging unshortened links).

---

### **Installation**

1. **Update System Packages**
   ```bash
   sudo apt update
   ```

2. **Install Google Chrome**
   ```bash
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo dpkg -i google-chrome-stable_current_amd64.deb
   sudo apt install -y -f
   ```

3. **Install ChromeDriver**
   ```bash
   wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.204/linux64/chromedriver-linux64.zip
   unzip chromedriver-linux64.zip
   sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
   ```

4. **Verify Installations**
   ```bash
   google-chrome --version
   chromedriver --version
   ```

5. **Install Python, pip, and Git**
   ```bash
   sudo apt install python3-pip
   sudo apt install git
   ```

6. **Clone the Repository**
   ```bash
   git clone https://github.com/barryallen16/unshortenBuddy.git
   cd unshortenBuddy
   ```

7. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

### **Configuration**


1. **Edit the `.env` file and add your credentials**
     ```plaintext
     DATABASE_URL="postgresql://username:password@host:port/database_name"
     TELEGRAM_BOT_TOKEN="your_telegram_bot_token_here"
     ADMIN_TELEGRAM_USERID=your_admin_user_id_here
     ```

2. **Run the Bot**
   ```bash
   python main.py
   ```

---

## **Usage** 🤖

1. Start the bot by sending `/start` in Telegram.
2. Send a shortened URL (e.g., `https://tnshort.com/xyz`).
3. Receive the unshortened link instantly.

---

## **Admin Commands** 🔒

- **Grant Access**: Use `/givebotaccess` to add a user to the access list.
- **Revoke Access**: Manually remove the user from the database.

---
## **License** 📜

This project is licensed under the **GNU General Public License (GPL)**. See the [LICENSE](LICENSE) file for details.
---

### **Changelog**
- **v1.0.0**: Initial release with support for `tnshort` and `krownlinks`.
- **v1.1.0**: Added admin controls and database logging.

---

### **FAQ**
**Q: How do I get my Telegram user ID?**  
A: Send `/start` to [@userinfobot](https://t.me/userinfobot) on Telegram.

**Q: Can I use this bot commercially?**  
A: No, this project is licensed under the GPL, which restricts commercial use.

**Q: How do I report a bug?**  
A: Open an issue on the [GitHub repository](https://github.com/yourusername/unshorten-buddy/issues).

---

**Unshorten Buddy** – Because every link deserves to be free! 🌐✨
