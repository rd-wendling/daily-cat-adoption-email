# Daily Cat Adoption Email

I built this project for my wife. She wanted a cat and would frequently visit the Boulder Humane Society cat rescue website, showing me various cats and trying to convince me to adopt one. To streamline her search, I created this daily email update. It highlights the chunkiest and tiniest cats available for adoption near us. Eventually, we adopted a cat, which was a great decision, but we both enjoy receiving these updates, so the email remains active.

## Overview
This project web scrapes the Boulder Humane Society's cat adoption website to gather relevant data on each cat up for adoption (e.g., name, age, weight, image). It filters the data to identify the largest and smallest cats and generates a responsive HTML block to display the information in an email that renders well on both desktop and mobile devices.

### Key Steps
1. **Get Animal IDs**
   - Extract all Animal IDs from the cat adoption homepage's source code. This step ensures we have a complete list of available cats and can adjust the data collection if any cats are adopted or new ones are added.
   - These IDs are used in the URLs for each specific cat, allowing us to access detailed information without manual navigation.
   - Since some data only becomes visible after JavaScript execution, we use Selenium to render the webpage and retrieve the source code, as opposed to using libraries like `requests`.

2. **Collect Individual Cat Data**
   - With the Animal IDs, we open each cat's webpage using concurrent requests through `ThreadPoolExecutor` to speed up the data collection process.
   - Scrape the necessary data from the source code.

3. **Generate HTML**
   - Extract the two cats of interest and build the HTML to embed in the email.
   - Ensure long descriptions are scrollable to maintain visual appeal, especially on mobile devices.

4. **Build and Send Email**
   - Embed the HTML into an email and send it to the recipients on the distribution list.

## Example Output
Here is what one of the updates looks like on Gmail desktop:
![screenshot](assets/screenshots/example_output.png)

## Installation
To run this yourself, follow these steps:

1. **Clone the Repository**
    ```sh
    git clone https://github.com/rd-wendling/daily-cat-adoption-email.git
    cd daily-cat-adoption-email
    ```
2. **Install Dependencies**
    Ensure you have Python installed (this was created using version 3.11). Then, install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```
3. **Set Up Environmental Variables**
    - **gmail_app_pwd:** Set up an app password for the Gmail account you will use to send the email and assign this value to the variable.
    - **sender_email:** The email address you want the email to be sent from.
    - **distro_list:** A comma-separated string of email addresses to send this email to.

You can now edit the code to work with your local Humane Society website and send email updates to you and your loved ones!
