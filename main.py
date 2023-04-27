import numpy as np
import cv2
import pyautogui
import time
import mouse

# Function to calculate Mean Squared Error (MSE) between two images
def mse(imageA, imageB):
    # Find the sum of squared difference between the images
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    # Normalize the squared error by dividing it by the total number of pixels
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err

def main():
    print('Welcome to Valorant InstaLocker!')
    flag = True
    a = 0
    example_image = cv2.imread('example.png', cv2.IMREAD_GRAYSCALE) # Load the image that we want to find on screen
    threshold = 5 # Set the maximum allowable MSE between the target and the current screen region
    x_lock = 960 # Set the X coordinate for the lock button position
    y_lock = 816 # Set the Y coordinate for the lock button position
    
    while True:
        i = 0
        if flag:
            while True:
                try:
                    a = int(input('Enter number of desired agent (from 1 to 21): ')) - 1 # Get the desired agent from the user
                    if not (0 <= a <= 20): # Check if the input is valid
                        raise Exception()
                    break
                except Exception:
                    print("Oops! That was no valid number.  Try again...")
            x_agent = 543 + 84 * (a % 11) # Calculate the X coordinate for the selected agent's icon
            y_agent = 927 + 84 * (a // 11) # Calculate the Y coordinate for the selected agent's icon
        flag = False
        
        while True:
            screenshot = np.array(pyautogui.screenshot(region = (839, 782, 243, 67))) # Take a screenshot of the current screen region
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY) # Convert the screenshot to grayscale for easier comparison
            
            if (mse(screenshot, example_image)) < threshold: # If the MSE between the target and the current screen region is less than the threshold,
                time.sleep(0.1) # Wait for a bit to make sure that the screen has updated
                screenshot = np.array(pyautogui.screenshot(region = (839, 782, 243, 67))) # Take another screenshot of the updated screen region
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY) # Convert the updated screenshot to grayscale

                if (mse(screenshot, example_image)) < threshold: # If the updated screenshot still matches the target image,
                    print('Success error: ', round(mse(screenshot, example_image)))
                    mouse.move(x_agent, y_agent, absolute=True, duration=0.01) # Move the mouse to the desired agent's icon
                    mouse.click('left') # Click on the agent's icon
                    time.sleep(0.01)
                    mouse.move(x_lock, y_lock, absolute=True, duration=0.01) # Move the mouse to the lock button position
                    mouse.click('left') # Click on the lock button
                    time.sleep(0.01)
                    break # Break out of the loop
                
            i = (i + 1) % 10 # Increment i to display current error every 10 iterations
            if i == 0:
                print('Current error: ', round(mse(screenshot, example_image))) # Print the current error every 10 iterations
            time.sleep(0.05) # Wait for a short while before taking another screenshot
        
        print('Success!')
        answer = input("ENTER to restart / 'h' to change agent / 'q' to exit: ")
        if answer == 'Q' or answer == 'q':
            break
        if answer == 'H' or answer == 'h':
            flag = True
        
        
if __name__ == '__main__':
    main()
