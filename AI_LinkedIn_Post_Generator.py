import openai
import datetime
import os
import glob

# Configure your OpenAI API key
openai.api_key = 'YOUR_API_KEY' # Insert here your API Key

# Function to determine the save path for files
def get_save_path():
    try:
        today = datetime.datetime.now()
        year = today.strftime('%y')  # Year in YY format
        month = today.strftime('%m')  # Month in MM format
        week_number = (today.day - 1) // 7 + 1  # Calculate the week of the month from 1 to 4
        save_path = os.path.join('Results', year, month, f'Week {week_number}')
        os.makedirs(save_path, exist_ok=True)  # Create directories if they do not exist
        return save_path
    except Exception as e:
        print(f"Error determining save path: {e}")
        return None

# Function to get the date of the previous day
def get_previous_day_date():
    try:
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        return yesterday.strftime('%d %B')
    except Exception as e:
        print(f"Error getting previous day's date: {e}")
        return None

# Function to get the previous weekend's dates (Saturday and Sunday)
def get_weekend_dates():
    try:
        today = datetime.datetime.now()
        saturday = today - datetime.timedelta(days=today.weekday() + 2)  # Previous Saturday
        sunday = today - datetime.timedelta(days=today.weekday() + 1)    # Previous Sunday
        return saturday.strftime('%d %B'), sunday.strftime('%d %B')
    except Exception as e:
        print(f"Error getting weekend dates: {e}")
        return None, None

# Prompt to create Monday LinkedIn posts with dynamic weekend dates
def get_monday_prompt():
    saturday, sunday = get_weekend_dates()
    if not saturday or not sunday:
        return "Error: Unable to retrieve weekend dates."
    return (
        f"Act as a social media manager. Search for the latest news and updates that happened during {saturday} and {sunday} in the AI/Tech world from reliable sources such as official news websites, "
        f"company announcements, or reputable tech blogs. Create a LinkedIn post with a recap of what happened during the weekend. If nothing major happened, provide a relevant tip about AI, "
        f"like a new software release or an interesting fact, citing the information found. The post should have an optimistic and forward-looking tone, be easy to understand for everyone, "
        f"and include the source link and company tag (e.g., use @company - the tag should be available) where relevant. Make sure to credit the sources by mentioning the website or platform "
        f"from which the information was gathered. The post should be between 160 and 180 words. After writing the post, count the words and ensure it meets the requirement. If it does not, adjust the length accordingly to fit the range."
    )

# Prompt for Tuesday, Wednesday, and Thursday based on the previous day
def get_previous_day_prompt():
    previous_day = get_previous_day_date()
    if not previous_day:
        return "Error: Unable to retrieve previous day's date."
    return (
        f"Act as a social media manager. Search for the latest news and updates that happened on {previous_day} in the AI/Tech world from reliable sources such as official news websites, "
        f"company announcements, or reputable tech blogs. Create a LinkedIn post with a recap of what happened during the day. If nothing major happened, provide a relevant tip about AI, "
        f"like a new software release or an interesting fact, citing the information found. The post should have an optimistic and forward-looking tone, be easy to understand for everyone, "
        f"and include the source link and company tag (e.g., use @company - the tag should be available) where relevant. Make sure to credit the sources by mentioning the website or platform "
        f"from which the information was gathered. The post should be between 160 and 180 words. After writing the post, count the words and ensure it meets the requirement. If it does not, adjust the length accordingly to fit the range."
    )

# Function to read files from Monday to Thursday
def read_weekly_files():
    try:
        summary = ""
        save_path = get_save_path()
        if not save_path:
            return "Error: Save path not found."
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday']
        for day in days:
            # Search for all files that start with the day's name in the specified folder
            files = glob.glob(os.path.join(save_path, f"{day}_*.txt"))
            for file_name in files:
                try:
                    with open(file_name, 'r', encoding='utf-8') as file:
                        content = file.read()
                        summary += f"{file_name}:\n{content}\n\n"
                except Exception as e:
                    print(f"Error reading file {file_name}: {e}")
        return summary
    except Exception as e:
        print(f"Error reading weekly files: {e}")
        return ""

# Function to create the Friday prompt based on weekly files
def create_friday_prompt():
    summary = read_weekly_files()
    if not summary:
        return "Act as a social media manager. Create a LinkedIn post with a recap of the week in AI/Tech, but no specific information was found from the previous days."
    return (
        "Act as a social media manager. Based on the following summaries of AI/Tech news shared during the week, create a LinkedIn post with a recap of the week. "
        "Highlight the most important news or tips, keep an optimistic and forward-looking tone, and ensure the post is easy to understand for everyone. "
        "Include source links and company tags where relevant.\n\n"
        f"Summaries:\n{summary}"
    )

# Define prompts to create LinkedIn posts for each day of the week
prompts = {
    'Monday': get_monday_prompt(),  # Dynamic prompt for Monday
    'Tuesday': get_previous_day_prompt(),  # Dynamic prompt for Tuesday
    'Wednesday': get_previous_day_prompt(),  # Dynamic prompt for Wednesday
    'Thursday': get_previous_day_prompt(),  # Dynamic prompt for Thursday
    'Friday': create_friday_prompt()  # Dynamic prompt for Friday
}

# Main function
def main():
    try:
        # Get the current day and date
        current_day = get_current_day()
        current_date = get_current_date()
        save_path = get_save_path()
        
        if not save_path:
            print("Error: Unable to determine the save path.")
            return

        # Generate the correct prompt based on the day
        prompt = prompts.get(current_day, None)
        
        # Check if the prompt is defined
        if prompt:
            # Send the prompt to ChatGPT and get the response
            response = send_prompt(prompt)
            
            if response:
                # Name the text file with the day of the week and date
                file_name = os.path.join(save_path, f'{current_day}_{current_date}.txt')
                
                # Save the response in the file with utf-8 encoding
                try:
                    with open(file_name, 'w', encoding='utf-8') as file:
                        file.write(response)
                    print(f"Response saved in file {file_name}.")
                except Exception as e:
                    print(f"Error saving the response: {e}")
            else:
                print("Unable to obtain a response.")
        else:
            print("No prompt defined for the current day.")
    except Exception as e:
        print(f"Error in the main function: {e}")

# Function to get the name of the current day of the week
def get_current_day():
    try:
        return datetime.datetime.now().strftime('%A')
    except Exception as e:
        print(f"Error getting the current day: {e}")
        return None

# Function to get the current date in the format dd_mm_yy
def get_current_date():
    try:
        return datetime.datetime.now().strftime('%d_%m_%y')
    except Exception as e:
        print(f"Error getting the current date: {e}")
        return None

# Function to send the prompt to ChatGPT
def send_prompt(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        response_content = completion.choices[0].message.content
        return response_content
    except Exception as e:
        print(f"Errore durante l'invio del prompt: {e}")
        return None

# Run the program
if __name__ == "__main__":
    main()
