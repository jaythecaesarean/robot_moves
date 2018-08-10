#!/usr/bin/python
# Filename: robot_moves.py

"""
This script  simulates a robot moving on a 5 by 5 units tabletop
    with the following commands:

PLACE X,Y,F    --> Placing the robot to the  location (x,y) and direction (f)
MOVE           --> Moves the robot 1 unit forward unless if it's out of bounds
LEFT           --> Turns the robot to the left
RIGHT          --> Turns the robot to the right
REPORT         --> Shows the current location and direction (e.g.: 5,0,NORTH)
STOP           --> Stop the script gracefully as alternative to to use CTRL+C


There are two ways to use this script
1. Use a text file (e.g.: 'data.txt') with commands inside
2. Use manual mode for flexibility (without using data.txt).
        The user needs to enter each command (one command at a time).

"""

import sys

available_commands = [
                        "PLACE", "MOVE", "LEFT", "RIGHT",
                        "MOVE", "REPORT", "STOP"
                     ]
robot_location = [0, 0, "NORTH"]
directions = ["NORTH", "EAST", "SOUTH", "WEST"]


# ask the user if has some file to simlulate
def does_file_exist():
    """
    This function only asks the user if the file to automate the robot exists.
    """
    check = str(input("Do you want to use a"
                      " text file? (y/n): ")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return does_file_exist()
    except Exception as error:
        print("Please enter  a valid file")
        print(error)
        return does_file_exist()


def process_file():
    """
    This function does the following
    1. Check if the file exists
    2. Check if all the commands inside the file are correct
    3. execute the each command
    """
    filename = str(input("What is the the filename "
                         "[default: data.txt]?")) or "data.txt"
    commands = []

    # check if the file exists then read the text and save it to a list
    try:
        with open(filename) as data_file:
            commands = data_file.read().splitlines()
    except Exception as error:
        error_str = "file does not exists. Make sure that this file exists."
        print("\'%s\' " + error_str % (filename))
        print(error)

    # check all the commands if valid
    invalid_lines = [commands.index(command) + 1 for command in commands
                     if command.split()[0] not in available_commands]
    if invalid_lines:
        print("Invalid commands found on "
              "following line/s of %s: %s" % (filename, invalid_lines))
        sys.exit(0)

    # execute the commands
    for command in commands:
        execute_command(command)

    sys.exit(0)


def place_robot(x, y, face_direction):
    """
    Place the robot on the desired location and direction

    Usage:
    place_robot(x,y,f)

    x,y   --> robot's position in x and y axes. (0,0) in the
                SOUTHWEST most corner of the table where 0 <= x,y <= 5
    f     --> what direction should the robot face
                (i.e. NORTH, EAST, SOUTH, or WEST)
    """
    new_x = int(x)
    new_y = int(y)
    if 0 <= new_x <= 5 and 0 <= new_y <= 5 and face_direction in directions:
        robot_location[0] = new_x
        robot_location[1] = new_y
        robot_location[2] = face_direction
    else:
        print("PLACE argument/s are invalid. %s" % (place_robot.__doc__))


def move():
    """
    Move the robot forward
    """
    # if facing north increment y but must not over 5 after increment
    if robot_location[2] == "NORTH" and robot_location[1] < 5:
        robot_location[1] += 1
    # if facing east increment x but must not be over 5 after increment
    elif robot_location[2] == "EAST" and robot_location[0] < 5:
        robot_location[0] += 1

    # if facing south decrement y but must not be less than 0 after decrement
    elif robot_location[2] == "SOUTH" and robot_location[1] > 0:
        robot_location[1] -= 1
    # if facing south decrement x but must not be less than 0 after decrement
    elif robot_location[2] == "WEST" and robot_location[0] > 0:
        robot_location[0] -= 1


def left():
    """
    Turns the robot to the left
    """
    current_face_index = directions.index(robot_location[2])
    robot_location[2] = directions[current_face_index - 1] \
        if current_face_index > 0 else directions[3]


def right():
    """
    Turns the robot to the right
    """
    current_face_index = directions.index(robot_location[2])
    robot_location[2] = directions[current_face_index + 1] \
        if current_face_index < 3 else directions[0]


def report():
    """
    Show the current location of the robot
    """
    print("Output: %s" % ','.join(map(str, robot_location)))


def execute_command(command):
    """
    This function sorts out the commands and execute them

    command --> one of the commands available
                (i.e.
                    "PLACE", "MOVE", "LEFT", "RIGHT",
                    "MOVE", "REPORT", or "STOP")
    """
    new_command = command.split()
    # check if the command is in the list of available commands then execute
    if new_command[0] in available_commands:
        if new_command[0] == "PLACE":
            try:
                place_args = new_command[1].split(',')
                place_robot(*place_args)
            except Exception as error:
                print(error)
                print("Please be sure to user the command "
                      "with arguments: PLACE X,Y,F")
        elif new_command[0] == "MOVE":
            move()

        elif new_command[0] == "LEFT":
            left()
        elif new_command[0] == "RIGHT":
            right()
        elif new_command[0] == "REPORT":
            report()
        else:
            sys.exit(0)

    else:
        print("\'%s\' is not on the our command list. Try Again." % (command))


def main():
    """
    Call this function to start
    """
    # check if the file exist or not?
    has_file = does_file_exist()
    if has_file:
        # if the file exist, process the file
        process_file()
    else:
        # if the user opts not to use a text file
        print("Enter Commands Below:")
        accepting_commands = True
        command_line_count = 0
        while accepting_commands:
            # show the commands line number to the user for references
            command_line_count += 1
            command = input("["+str(command_line_count) + "]: ")
            execute_command(command.upper())


if __name__ == '__main__':
    # tell the user what to do
    print(__doc__)
    main()
