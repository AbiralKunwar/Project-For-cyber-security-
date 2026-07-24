import random
import string


def check_password_strength(password):
    # function to check the strength of a password
    if len(password) < 8:                                                        # check if the password is at least 8 characters long
        return "Password is Weak: Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):                             # check if the password contains at least one digit
        return "Password is Weak: Password must contain at least one digit."
    if not any(char.isupper() for char in password):                             # check if the password contains at least one uppercase letter
        return "Password is Weak: Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):                             # check if the password contains at least one lowercase letter
        return "Password is Weak: Password must contain at least one lowercase letter."
    if not any(char in "!@#$%^&*(),.?\":{}|<>" for char in password):            # check if the password contains at least one special character
        return "Password is Weak: Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)."       
    
    return "Congratulations! Your password is Strong and secure." # if password passes all checks, return that it is strong

# Creating a function to generate a strong password based on user input
def generate_password(word): 
    # Make the first letter uppercase
    password = word.capitalize()

    #  Randomly add numbers
    password += str(random.randint(100, 999))

    # Randomly add special characters
    symbols = "!@#$%^&*"
    password += random.choice(symbols)
    password += random.choice(symbols)

    return password

def password_stren_checker():
    # function to take user input and check the strength of the password
    weak_count = 0
  
    print ("==========================Weclcome to Password Strength Checker==========================")
    while True: # loop to continuously ask for user input until they choose to exit
        password = input("\n Enter your password (or type 'exit' to quit): ")
        if password.lower() == 'exit':
            print("Exiting... Thank you for using the Password Strength Checker! Have a good day!")
            break

        result = check_password_strength(password)
        print(result)

        if "Weak" in result:  # if the password is weak, increment the weak count and check if it exceeds 3 attempts
            weak_count += 1 
            print(f"Password attempts: {weak_count}/3") 

            if weak_count >= 3:
                print("You have exceeded the maximum number of attempts. Please try again later or use auto generate password.")
                
                choice = input("Do you want to generate a strong password from your input? (y/n): ")

                if choice.lower() == "y":   
                    new_password = generate_password(password)
                    print("Suggested Strong Password:", new_password)

                # Reset the weak count after suggesting a new password
                weak_count = 0  
        else:
            # Reset the weak count if the password is strong
            weak_count = 0  

if __name__ == "__main__":
    password_stren_checker()  # call the main function to start the password strength checker
    







