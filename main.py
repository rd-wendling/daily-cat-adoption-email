#%% Import Dependencies
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import functions.utils as fu
import os


#%% Boulder Human Society Cat Adoption Homepage
url = 'https://boulderhumane.org/cats'

# Run the web scraper
results = fu.run_get_cat_data(url)
cat_df = pd.DataFrame(results)

# Get weight as int from the scraped weight string
cat_df['weight lbs'] = cat_df['weight'].str.split('pounds').str[0].str.strip().astype(int)

# Order the cat_df by weight
cat_df_sorted = cat_df.sort_values(by='weight lbs')

# Get the row with the lightest cat (first row after sorting)
lightest_cat_row = cat_df_sorted.iloc[0]

# Get the row with the heaviest cat (last row after sorting)
heaviest_cat_row = cat_df_sorted.iloc[-1]



#%% Send the Email
# Your Gmail credentials
sender_email = os.environ.get('sender_email')
sender_password = os.environ.get('gmail_app_pwd')

# List of recipient email addresses
recipient_emails = os.environ.get('distro_list')
recipient_emails = recipient_emails.split(',')

# Create a connection to the Gmail SMTP server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, sender_password)

# Create the email message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ', '.join(recipient_emails)
msg['Subject'] = 'Daily Cat Adoption Update'

# Message content
fat_cat_widget = fu.html_widget_generator(heaviest_cat_row, 'Fattest Cat')
small_cat_widget = fu.html_widget_generator(lightest_cat_row, 'Smallest Cat')
message_text = fat_cat_widget + small_cat_widget
msg.attach(MIMEText(message_text, 'html'))

# Send the email
server.sendmail(sender_email, recipient_emails, msg.as_string())

# Close the server connection
server.quit()

# %%
