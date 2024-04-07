import time
import bot_function
import json
from action_recorder import recorder
from action_recorder import playback
from multiprocessing import Process

templet = """\n
1. Mine in one direction
2. Mine in the corner
3. Record action
4. Play action

"""

# Load JSON data from file
with open("config.json", "r") as file:
    json_data = json.load(file)

# Extract details
player_level = int(json_data["player_level"])
rocks_to_mine = int(json_data["rocks_to_mine"])
time_for_one_rock = int(json_data["time_for_one_rock"])
position_of_wall = json_data["position_of_wall"]
move_1 = json_data["move_1"]
move_2 = json_data["move_2"]
mine_btn = json_data["mine_btn"]
corner_1 = json_data["corner_1"]
corner_2 = json_data["corner_2"]
print("*"*100)
print("Config details....")
print("*"*100)
print(f"Player Level: {player_level}")
print(f"Rocks to Mine: {rocks_to_mine}")
print(f"Time for One Rock: {time_for_one_rock}")
print(f"Position of Wall: {position_of_wall}")
print(f"Move 1: {move_1}")
print(f"Move 2: {move_2}")
print(f"Mine Button: {mine_btn}")
print(f"Corner one: {corner_1}")
print(f"Corner two: {corner_2}")
print("*"*100)
print()


def countdownTimer():
    # Countdown timer
    print("Starting", end="", flush=True)
    for i in range(0, 5):
        print(".", end="", flush=True)
        time.sleep(1)
    print("Go")
def get_scan_code(direction):
    scan_codes = {
        "Up": 0x48,
        "Down": 0x50,
        "Left": 0x4b,
        "Right": 0x4d,
        "S": 0x1f,
        "Space": 0x39
    }
    return scan_codes.get(direction, None)

int_mine_btn = get_scan_code(mine_btn)
int_wall_position = get_scan_code(position_of_wall)
int_move1 = get_scan_code(move_1)
int_move2 = get_scan_code(move_2)
int_corner_1 = get_scan_code(corner_1)
int_corner_2 = get_scan_code(corner_2)

def mine_dir_1(call):
    count = 0
    while count <= call:
        try:
            bot_function.drill(trigger=int(int_mine_btn), total_time=time_for_one_rock)
            bot_function.move(int(int_move1), wall_side=int(int_wall_position))
        except KeyboardInterrupt as e:
            return

def mine_dir_2(call):
    count = 0
    while count <= call:
        try:
            bot_function.drill(trigger=int(int_mine_btn), total_time=time_for_one_rock)
            bot_function.move(int(int_move2), wall_side=int(int_wall_position))
        except:
            print("Mining interrupted.")
            return
def mine_in_direction():
    rock_mined = 0
    countdownTimer()
    while rock_mined <= rocks_to_mine:
        try:
            mine_dir_1(round(rocks_to_mine/2))
            rock_mined += 1
            print(rock_mined)
            mine_dir_1(round(rocks_to_mine / 2))
            rock_mined += 1
            print(rock_mined)
        except KeyboardInterrupt as e:
            print(e)
            print("Mining interrupted.")
            return
def mine_in_corner(side_1=int_corner_1, side_2=int_corner_2):
    rock_mined = 0
    countdownTimer()
    while rock_mined <= rocks_to_mine:
        try:
            bot_function.drill(trigger=int(int_mine_btn), total_time=time_for_one_rock)
            bot_function.switch_corner(int(side_2))
            rock_mined += 1
            print(rock_mined)
            bot_function.drill(trigger=int(int_mine_btn), total_time=time_for_one_rock)
            bot_function.switch_corner(int(side_1))
            rock_mined += 1
            print(rock_mined)
        except KeyboardInterrupt as e:
            print(e)
            print("Mining interrupted.")

            return

# def check_ok_button():
#     global ok_btn
#     try:
#         ok_button_location = pyautogui.locateOnScreen('button.png', confidence=0.7)
#         time.sleep(1)
#         if ok_button_location:
#             ok_button_center = pyautogui.center(ok_button_location)
#             pyautogui.click(ok_button_center)
#             print("Pop up message detected.... OK pressed, exiting....")
#             ok_btn = True  # Set ok_btn to True before exiting
#             exit()
#     except pyautogui.ImageNotFoundException:
#         pass  # Continue with the program if the image is not found
#


def switch_case(user_in):
    match user_in:
        case "1":
            mine_in_direction()
        case "2":
            mine_in_corner()
        case "3":
            recorder.Record_main()
        case "4":
            playback.Play_main()

def main():
    print("Make sure data in config is right..... Starting the bot...\n")
    time.sleep(2)
    while True:
        try:
            print(templet)
            user_input = input("Your choice: ")
            switch_case(user_input)
        except KeyboardInterrupt as e:
            print(e)
            return


if __name__ == "__main__":
    main()