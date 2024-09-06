from utils import (
    get_save_path, get_current_day, get_current_date,
    send_prompt, prompts
)
import os

def main():
    try:
        current_day = get_current_day()
        current_date = get_current_date()
        save_path = get_save_path()
        
        if not save_path:
            print("Error: Unable to determine the save path.")
            return

        prompt_func = prompts.get(current_day)
        
        if prompt_func:
            prompt = prompt_func()
            response = send_prompt(prompt)
            
            if response:
                file_name = os.path.join(save_path, f'{current_day}_{current_date}.txt')
                
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

if __name__ == "__main__":
    main()
