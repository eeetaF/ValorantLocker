import numpy as np
import cv2
import pyautogui
import time
import mouse

def mse(imageA, imageB):
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err

def main():
    print('Welcome to Valorant InstaLocker!')
    
    flag = True
    a = 0
    
    example_image = cv2.imread('example.png')
    example_image = cv2.cvtColor(example_image, cv2.COLOR_BGR2GRAY)
    threshold = 5
    x_lock = 960
    y_lock = 816
    
    while True:
        i = 0
        if flag:
            while True:
                try:
                    a = int(input('Enter number of desired agent (from 1 to 21): '))
                    if a < 1 or a > 21:
                        raise Exception()
                    break
                except Exception:
                    print("Oops! That was no valid number.  Try again...")
            a-=1
            x_agent = 543 + 84 * (a % 11)
            y_agent = 927 + 84 * (a // 11)
        flag = False
        
        while True:
            screenshot = pyautogui.screenshot(region = (839, 782, 243, 67))
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            if (mse(screenshot, example_image)) < threshold:
                time.sleep(0.1)
                screenshot = pyautogui.screenshot(region = (839, 782, 243, 67))
                screenshot = np.array(screenshot)
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

                if (mse(screenshot, example_image)) < threshold:
                    print('Success error: ', round(mse(screenshot, example_image)))
                    mouse.move(x_agent, y_agent, absolute=True, duration=0.01)
                    time.sleep(0.01)
                    mouse.click('left')
                    time.sleep(0.01)
                    mouse.move(x_lock, y_lock, absolute=True, duration=0.01)
                    time.sleep(0.01)
                    mouse.click('left')
                    time.sleep(0.01)
                    break
            
            i = i + 1
            if i % 10 == 0:
                print('Current error: ', round(mse(screenshot, example_image)))
            time.sleep(0.05)
        
    
        print('Success!')
        answer = input("Press ENTER to restart / Type 'h' to change agent /Type 'q' to exit: ")
        if answer == 'Q' or answer == 'q':
            break
        if answer == 'H' or answer == 'h':
            flag = True
        
        
if __name__ == '__main__':
    main()
