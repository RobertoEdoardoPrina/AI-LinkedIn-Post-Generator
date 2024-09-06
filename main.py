from utils import (
    get_save_path, get_current_day, get_current_date,
    send_prompt, prompts
)  # Importing utility functions from the utils module
import os

# Main function to execute the daily prompt generation and saving process
def main():
    try:
        current_day = get_current_day()  # Get the current day of the week (e.g., Monday)
        current_date = get_current_date()  # Get the current date formatted as 'day_month_year'
        save_path = get_save_path()  # Get or create the directory path where results will be saved

        if not save_path:  # Check if the save path was determined successfully
            print("Error: Unable to determine the save path.")
            return  # Exit the function if the save path is not found

        # Retrieve the appropriate prompt function based on the current day
        prompt_func = prompts.get(current_day)
        
        if prompt_func:  # Check if a prompt function is defined for the current day
            prompt = prompt_func()  # Generate the prompt using the function
            response = send_prompt(prompt)  # Send the prompt to OpenAI and get a response
            
            if response:  # Check if a response was successfully received
                file_name = os.path.join(save_path, f'{current_day}_{current_date}.txt')  # Define the file name based on the current day and date
                
                try:
                    with open(file_name, 'w', encoding='utf-8') as file:  # Open the file in write mode
                        file.write(response)  # Write the response content to the file
                    print(f"Response saved in file {file_name}.")  # Notify that the response was saved
                except Exception as e:
                    print(f"Error saving the response: {e}")  # Print an error message if saving fails
            else:
                print("Unable to obtain a response.")  # Print a message if the response is empty or None
        else:
            print("No prompt defined for the current day.")  # Print a message if no prompt function is defined
    except Exception as e:
        print(f"Error in the main function: {e}")  # Print an error message if an exception occurs in the main function

# Execute the main function when the script is run directly
if __name__ == "__main__":
    main() 
