import os
from dotenv import load_dotenv
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import time
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
import re
import psycopg2
from selenium.common.exceptions import TimeoutException

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_USERID = int(os.getenv("ADMIN_TELEGRAM_USERID"))

async def is_element_present(driver, by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        return False

def wait_for_timer(driver, timer_id):
    WebDriverWait(driver, 30).until(
        lambda d: d.find_element(By.ID, timer_id).text == "0"
    )

async def tnshort_bypass(url):
    chrome_options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Mobile Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    c_url = None
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        driver.implicitly_wait(30)
        for page_no in range(1, 4):
            pageNoText = driver.find_element(By.ID, 'stick').text
            if f"{page_no}/3" in pageNoText:
                driver.execute_script(""" 
                const btn1 = document.getElementById('btn7');
                btn1.style.display = 'block';
                btn1.click();
                """)
            else:
                print(f"Unexpected page number: {pageNoText}")
        try:
            wait_for_timer(driver, "timer")
            timer = driver.find_element(By.ID, 'timer')
            if timer:
                time.sleep(3)
                ip = driver.execute_script('return window.location.hostname')
                driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-success.btn-lg.get-link').click()
                c_url = driver.current_url
                driver.quit()
        except:
            pass
    except Exception as e:
        error_message = str(e)
        print(error_message)
    finally:
        if c_url:
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO unshortenbuddy (shortlink,directlink) VALUES {url,c_url}")
            connection.commit()
            cursor.close()
            connection.close()
            return c_url
        else:
            print('c_url is none')

async def krownlinks_bypass(url):
    chrome_options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Mobile Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    fdlink = None
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.execute_script("javascript:openSite()")
    wait = WebDriverWait(driver, 60)
    element = wait.until(
        EC.presence_of_element_located((By.ID, "gotolink")))
    if element:
        driver.execute_script("""var gotoLinkButton = document.getElementById("gotolink");
gotoLinkButton.disabled = false;
gotoLinkButton.click();
""")
        wait = WebDriverWait(driver, 60)
        element = wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, "Get Link")))
        if element:
            fdlink = driver.find_element(By.CSS_SELECTOR, "a.btn").get_attribute("href")
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO unshortenbuddy (shortlink,directlink) VALUES {url, fdlink}")
            connection.commit()
            cursor.close()
            connection.close()
            return fdlink

async def process_tnshort_urls(urls):
    tasks = [tnshort_bypass(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def process_krownlinks_urls(urls):
    tasks = [krownlinks_bypass(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(f"SELECT username FROM accesscontrol")
    rows = cursor.fetchall()
    connection.close()
    usernames = [row[0] for row in rows]
    print(usernames)
    userid = update.message.from_user.id
    userid = str(userid)
    if userid not in usernames and userid !=str(ADMIN_USERID):
        keyboard = [[InlineKeyboardButton("Get User Id", callback_data='getuserid')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        response = f"""🔒 *Access Denied!* 🚫\n\nHey there! It looks like you don’t have access to this bot yet. No worries! Tap *Get User Id* to fetch your user ID and forward it to the admin for access. Once approved, you’ll be all set to start unshortening links like a pro! 😊"""
        response = response.replace('.', r'\.')
        response = response.replace('!', r'\!')
        
        await update.message.reply_text(text=response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
                                        reply_markup=reply_markup)
    elif userid in usernames or userid ==str(ADMIN_USERID):
        formatted_message = r"""
🎉 *Welcome to UnshortenBuddy Bot!* 🚀

Hey there, Explorer! 🕵️‍♂️ Ready to dive into the world of unshortened links? I’m *UnshortenBuddy*, your trusty sidekick for bypassing those pesky short URLs and revealing their true destinations. 🌐✨

Here’s how I can help:
1. **Unshorten Links**: Just send me a short link, and I’ll work my magic to reveal the full URL.
2. **Fast & Reliable**: No more waiting around—get direct links in seconds.
3. **Easy to Use**: Simply send a link, and I’ll handle the rest.

Use the /help command if you need a quick guide on how to use me. Let’s get started and unshorten some links! 🚀

🚨 *Note*: Please send only one short link at a time for bypass. Sending multiple links may result in longer processing times. Thank you! 😊
        """
        formatted_message = formatted_message.replace('!', r'\!')
        formatted_message = formatted_message.replace('.', r'\.')
        await update.message.reply_text(text=formatted_message, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(f"SELECT username FROM accesscontrol")
    rows = cursor.fetchall()
    connection.close()
    usernames = [row[0] for row in rows]
    userid = update.message.from_user.id
    userid = str(userid)
    if userid in usernames or userid ==str(ADMIN_USERID):
        formatted_message =r"""
🌟 *Unlock the Magic with Unshorten Buddy Bot!* 🌟

Hey there, link explorers! 🕵️‍♂️ Ready to unleash the magic? Your Unshorten Buddy can effortlessly handle these tricky links:
1. 🧙‍♂️ **tnshort** 
2. 👑 **krownlinks** 
No more link guessing games. Let Unshorten Buddy guide you through the link wonderland! 🚀✨ #LinkMagic #UnshortenBuddy

🚀 **Start sending those links and let the magic unfold!** 🌐✉️

🚨 *Note:* Please send only one short link at a time for bypass. Sending multiple links may result in longer processing times. Thank you!
        """
        formatted_message = formatted_message.replace('.', r'\.')
        formatted_message = formatted_message.replace('!', r'\!')
        formatted_message = formatted_message.replace('#', r'\#')
        formatted_message = formatted_message.replace('**', '*')
        await update.message.reply_text(text=formatted_message, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
    if userid not in usernames and userid !=str(ADMIN_USERID):
        formatted_message = r"""
🌟 *Unlock the Magic with Unshorten Buddy Bot!* 🌟

Hey there, link explorers! 🕵️‍♂️ Ready to unleash the magic? Your Unshorten Buddy can effortlessly handle these tricky links:
1. 🧙‍♂️ **tnshort** 
2. 👑 **krownlinks** 
No more link guessing games. Let Unshorten Buddy guide you through the link wonderland! 🚀✨ #LinkMagic #UnshortenBuddy

🚀 **Before you start sending those links, get your Bot Access from the admin by using /start command** 🌐✉️

🚨 *Note:* Please send only one short link at a time for bypass. Sending multiple links may result in longer processing times. Thank you!
        """
        formatted_message = formatted_message.replace('.', r'\.')
        formatted_message = formatted_message.replace('!', r'\!')
        formatted_message = formatted_message.replace('#', r'\#')
        formatted_message = formatted_message.replace('**', '*')
        await update.message.reply_text(text=formatted_message, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
async def process_urls(input, url_pattern, process_function, update: Update):
    processing_message = await update.message.reply_text(r"🔍 *Processing your link\.\.\.* Hang tight\! I'm working my magic to unshorten it for you\. ✨", 
                                                         parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

    listi = re.split(r'(\S+|\s)', input)
    shortlink_positions = [i for i, word in enumerate(listi) if word.startswith(url_pattern)]
    all_links = [listi[i] for i in shortlink_positions]
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(f"SELECT shortlink,directlink FROM unshortenbuddy")
    rows = cursor.fetchall()
    connection.close()
    index = 0
    results = []
    for row in rows:
        slink, dlink = row
        if 0 <= index < len(all_links) and all_links[index] == slink:
            results.append(dlink)
            index += 1
    if results:
        start_time = time.time()
        for i, position in enumerate(shortlink_positions):
            listi[position] = results[i]
        final_link = ''.join(listi)
        print(final_link)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total time taken: {total_time} seconds")
        await processing_message.delete()  
        return final_link
    elif not results:
        start_time = time.time()
        results = await process_function(all_links)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total time taken: {total_time} seconds")
        print(results)
        for i, position in enumerate(shortlink_positions):
            listi[position] = results[i]
        final_link = ''.join(listi)
        print(final_link)
        await processing_message.delete() 
        return final_link

async def process_input(update, context):
    if "waiting_for_input" in context.user_data and context.user_data["waiting_for_input"]:
        user_input = update.message.text
        if user_input.isdigit():
            context.user_data["user_input"] = user_input
            context.user_data["waiting_for_input"] = False
            connection = psycopg2.connect(DATABASE_URL)
            cursor = connection.cursor()
            userid = update.message.from_user.id
            admin = ADMIN_USERID
            if userid == admin:
                idtestquery=""
                cursor.execute(f"SELECT username FROM accesscontrol")
                rows = cursor.fetchall()
                usernames = [row[0] for row in rows]
                user_input=str(user_input)
                if user_input in usernames or user_input ==str(ADMIN_USERID):
                    print('in here')
                    response = f"*The user already has access.*"
                    response = response.replace('.', r'\.')
                    await update.message.reply_text(text=response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
                else:
                    query = "INSERT INTO accesscontrol (username) VALUES (%s)"
                    cursor.execute(query, (user_input,))
                    connection.commit()
                    response = f"✅ *Access Granted!* The user has been added to the bot's access list."
                    response = response.replace('.', r'\.')
                    response = response.replace('!', r'\!')
                    await update.message.reply_text(text=response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
                    # Notify the user that access has been granted
                    response=f"""🎉 *Welcome aboard!* 🚀\n\nYour access to *UnshortenBuddy Bot* has been granted by the admin. You can now start using the bot to unshorten links effortlessly. Just send me a short link, and I'll do the rest! ✨\n\nHappy unshortening! 😊"""
                    response = response.replace('!', r'\!')
                    response = response.replace('.', r'\.')
                    await context.bot.send_message(
                        chat_id=user_input,
                        text=response,
                        parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
                    )
            elif userid != admin:
                response = r"❌ *Oops!* This command is exclusive to the admin. Only the admin can grant bot access."
                await update.message.reply_text(text=response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
            cursor.close()
            connection.close()
        else:
            context.user_data["waiting_for_input"] = False
    else:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        cursor.execute(f"SELECT username FROM accesscontrol")
        rows = cursor.fetchall()
        connection.close()
        usernames = [row[0] for row in rows]
        userid = update.message.from_user.id
        userid = str(userid)
        if userid not in usernames and userid !=str(ADMIN_USERID):
            keyboard = [[InlineKeyboardButton("Get User Id", callback_data='getuserid')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            response = f"🔒 *Access Denied!*\n\nApologies, you don't have access to this bot yet. Tap *Get User Id* to fetch your user ID and forward it to the admin for access."
            response = response.replace('.', r'\.')
            response = response.replace('!', r'\!')
            await update.message.reply_text(text=response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
                                            reply_markup=reply_markup)
        elif userid in usernames or userid ==str(ADMIN_USERID):
            input_text = update.message.text
            tnshort_pattern = re.compile(r'https://tnseries.com/\w+')
            krownlinks_pattern = re.compile(r'https://krownlinks.me/\S+')
            if re.search(tnshort_pattern, input_text):
                final_link = await process_urls(input_text, "https://tnseries.com/", process_tnshort_urls, update)
            elif re.search(krownlinks_pattern, input_text):
                print("found krownlinks")
                final_link = await process_urls(input_text, "https://krownlinks.me/", process_krownlinks_urls, update)
            else:
                final_link = None
                response= f"""❌ *Oops!* It seems I've hit a roadblock with this particular website. 🚧\n\nI can't unshorten links from here. Feel free to try another link, and I'll do my best to assist you! 😊"""
                response = response.replace('!', r'\!')
                response = response.replace('.', r'\.')
                await update.message.reply_text(
                response,
                    parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
                )
            if final_link:
                await update.message.reply_text(final_link)

async def photo_caption_handler(update, context):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute(f"SELECT username FROM accesscontrol")
    rows = cursor.fetchall()
    connection.close()
    usernames = [row[0] for row in rows]
    userid = update.message.from_user.id
    userid = str(userid)
    if userid not in usernames and userid !=str(ADMIN_USERID):
        keyboard = [[InlineKeyboardButton("Get User Id", callback_data='getuserid')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        response = f"🔒 *Access Denied!*\n\nApologies, you don't have access to this bot yet. Tap *Get User Id* to fetch your user ID and forward it to the admin for access."
        response = response.replace('.', r'\.')
        response = response.replace('!', r'\!')
        await update.message.reply_text(text=response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
                                        reply_markup=reply_markup)
    elif userid in usernames or userid ==str(ADMIN_USERID):
        message = update.message
        caption_text = None
        if message.photo and message.caption:
            caption_text = message.caption
        elif message.video and message.caption:
            caption_text = message.caption
        input_text = caption_text
        tnshort_pattern = re.compile(r'https://tnseries.com/\w+')
        krownlinks_pattern = re.compile(r'https://krownlinks.me/\S+')
        if re.search(tnshort_pattern, input_text):
            final_link = await process_urls(input_text, "https://tnseries.com/", process_tnshort_urls, update)
        elif re.search(krownlinks_pattern, input_text):
            print("found krownlinks")
            final_link = await process_urls(input_text, "https://krownlinks.me/", process_krownlinks_urls, update)
        else:
            final_link = None
            response= f"""❌ *Oops!* It seems I've hit a roadblock with this particular website. 🚧\n\nI can't unshorten links from here. Feel free to try another link, and I'll do my best to assist you! 😊"""
            response = response.replace('!', r'\!')
            response = response.replace('.', r'\.')
            await update.message.reply_text(response,
                parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
            )
        if final_link:
            await update.message.reply_text(final_link)

async def botaccess(update: Update, context):
    userid = update.message.from_user.id
    admin = ADMIN_USERID
    if userid == admin:
        response = f"👑 *Admin Command* 👑\n\nPlease enter the user ID to grant bot access:"
        await update.message.reply_text(text=response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
        context.user_data["waiting_for_input"] = True
    elif userid != admin:
        response = "❌ *Oops!* This command is exclusive to the admin. Only the admin can grant bot access."
        response = response.replace('.', r'\.')
        response = response.replace('!', r'\!')
        await update.message.reply_text(text=response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

async def button_click(update, context):
    query = update.callback_query
    button_clicked = query.data
    message = update.message or query.message
    if button_clicked == 'getuserid':
        user_id = update.effective_user.id
        user_name = update.effective_user.name
        response = f"🆔 *Your User ID:* `{user_id}`\n👤 *Your Name:* {user_name}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
        response = f"📤 *Next Steps:*\n\nSend your user ID to the admin to get access to the bot. Once approved, you’ll be all set to start unshortening links! 🚀"
        response = response.replace('!', r'\!')
        response = response.replace('.', r'\.')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_input))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO & filters.CAPTION, photo_caption_handler))
    app.add_handler(CommandHandler("givebotaccess", botaccess))
    app.add_handler(CallbackQueryHandler(button_click))
    app.run_polling()
