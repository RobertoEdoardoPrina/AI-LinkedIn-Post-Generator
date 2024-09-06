import openai
import datetime
import os
import glob

# Configure your OpenAI API key
openai.api_key = 'YOUR_API_KEY'  # Insert your OpenAI API key here

# Function to determine and create the path to save results based on the current date
def get_save_path():
    try:
        today = datetime.datetime.now()  # Get the current date and time
        year = today.strftime('%y')  # Extract the current year in two-digit format
        month = today.strftime('%m')  # Extract the current month
        week_number = (today.day - 1) // 7 + 1  # Calculate the week number of the month
        save_path = os.path.join('Results', year, month, f'Week {week_number}')  # Construct the save path
        os.makedirs(save_path, exist_ok=True)  # Create the directories if they don't exist
        return save_path
    except Exception as e:
        print(f"Error determining save path: {e}")  # Print an error message if there's an exception
        return None

# Function to get the date of the previous day
def get_previous_day_date():
    try:
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)  # Get yesterday's date
        return yesterday.strftime('%d %B')  # Format it as 'day month'
    except Exception as e:
        print(f"Error getting previous day's date: {e}")  # Print an error message if there's an exception
        return None

# Function to get the dates of the last Saturday and Sunday
def get_weekend_dates():
    try:
        today = datetime.datetime.now()  # Get the current date
        saturday = today - datetime.timedelta(days=today.weekday() + 2)  # Calculate last Saturday
        sunday = today - datetime.timedelta(days=today.weekday() + 1)  # Calculate last Sunday
        return saturday.strftime('%d %B'), sunday.strftime('%d %B')  # Format as 'day month'
    except Exception as e:
        print(f"Error getting weekend dates: {e}")  # Print an error message if there's an exception
        return None, None

# Function to generate a prompt for a Monday LinkedIn post
def get_monday_prompt():
    saturday, sunday = get_weekend_dates()  # Get last weekend's dates
    if not saturday or not sunday:
        return "Error: Unable to retrieve weekend dates."  # Return error if dates are not found
    # Generate prompt to summarize AI/Tech news from the past weekend
    return (
        f"Act as a social media manager. Search for the latest news and updates that happened during {saturday} and {sunday} in the AI/Tech world from reliable sources such as official news websites, "
        f"company announcements, or reputable tech blogs. Create a LinkedIn post with a recap of what happened during the weekend. If nothing major happened, provide a relevant tip about AI, "
        f"like a new software release or an interesting fact, citing the information found. The post should have an optimistic and forward-looking tone, be easy to understand for everyone, "
        f"and include the source link and company tag (e.g., use @company - the tag should be available) where relevant. Make sure to credit the sources by mentioning the website or platform "
        f"from which the information was gathered. The post should be between 160 and 180 words. After writing the post, count the words and ensure it meets the requirement. If it does not, adjust the length accordingly to fit the range."
    )

# Function to generate a prompt for a LinkedIn post summarizing the previous day's news
def get_previous_day_prompt():
    previous_day = get_previous_day_date()  # Get yesterday's date
    if not previous_day:
        return "Error: Unable to retrieve previous day's date."  # Return error if date is not found
    # Generate prompt to summarize AI/Tech news from the previous day
    return (
        f"Act as a social media manager. Search for the latest news and updates that happened on {previous_day} in the AI/Tech world from reliable sources such as official news websites, "
        f"company announcements, or reputable tech blogs. Create a LinkedIn post with a recap of what happened during the day. If nothing major happened, provide a relevant tip about AI, "
        f"like a new software release or an interesting fact, citing the information found. The post should have an optimistic and forward-looking tone, be easy to understand for everyone, "
        f"and include the source link and company tag (e.g., use @company - the tag should be available) where relevant. Make sure to credit the sources by mentioning the website or platform "
        f"from which the information was gathered. The post should be between 160 and 180 words. After writing the post, count the words and ensure it meets the requirement. If it does not, adjust the length accordingly to fit the range."
    )

# Function to read and summarize files created during the week
def read_weekly_files():
    try:
        summary = ""
        save_path = get_save_path()  # Get the save path for the current week
        if not save_path:
            return "Error: Save path not found."  # Return error if save path is not found
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday']  # List of weekdays to read from
        for day in days:
            files = glob.glob(os.path.join(save_path, f"{day}_*.txt"))  # Find all text files for the day
            for file_name in files:
                try:
                    with open(file_name, 'r', encoding='utf-8') as file:  # Open and read each file
                        content = file.read()
                        summary += f"{file_name}:\n{content}\n\n"  # Append content to the summary
                except Exception as e:
                    print(f"Error reading file {file_name}: {e}")  # Print an error message if there's an exception
        return summary
    except Exception as e:
        print(f"Error reading weekly files: {e}")  # Print an error message if there's an exception
        return ""

# Function to create a prompt for a Friday LinkedIn post summarizing the week
def create_friday_prompt():
    summary = read_weekly_files()  # Read the week's summaries
    if not summary:
        return "Act as a social media manager. Create a LinkedIn post with a recap of the week in AI/Tech, but no specific information was found from the previous days."
    # Generate a prompt based on the week's summaries
    return (
        "Act as a social media manager. Based on the following summaries of AI/Tech news shared during the week, create a LinkedIn post with a recap of the week. "
        "Highlight the most important news or tips, keep an optimistic and forward-looking tone, and ensure the post is easy to understand for everyone. "
        "Include source links and company tags where relevant.\n\n"
        f"Summaries:\n{summary}"
    )

# Function to get the current day of the week
def get_current_day():
    try:
        return datetime.datetime.now().strftime('%A')  # Return the current day of the week
    except Exception as e:
        print(f"Error getting the current day: {e}")  # Print an error message if there's an exception
        return None

# Function to get the current date formatted as 'day_month_year'
def get_current_date():
    try:
        return datetime.datetime.now().strftime('%d_%m_%y')  # Return the current date in a specific format
    except Exception as e:
        print(f"Error getting the current date: {e}")  # Print an error message if there's an exception
        return None

# Function to send a prompt to OpenAI and get a response
def send_prompt(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the GPT-3.5 Turbo model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},  # System message to define assistant role
                {"role": "user", "content": prompt}  # User message with the prompt content
            ]
        )
        response_content = completion.choices[0].message.content  # Extract the assistant's response
        return response_content
    except Exception as e:
        print(f"Error during prompt submission: {e}")  # Print an error message if there's an exception
        return None

# Define prompts to create LinkedIn posts for each day of the week
prompts = {
    'Monday': get_monday_prompt,
    'Tuesday': get_previous_day_prompt,
    'Wednesday': get_previous_day_prompt,
    'Thursday': get_previous_day_prompt,
    'Friday': create_friday_prompt
}
