
def get_threat_actor_group_from_file(filename):

    # Open the file and read line by line
    with open(filename, 'r') as file:
        lines_list = [line.strip() for line in file]

    return lines_list