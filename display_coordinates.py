import time

def display_coordinates(snake_coordinates, snake_size):
    while True:
        print(f"Snake Head Coordinates: {snake_coordinates}, Snake Size: {snake_size}")
        time.sleep(1)  # Adjust the refresh rate as needed
        input("Press Enter to exit...")  # Add this line to keep the window open
