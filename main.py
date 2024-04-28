import subprocess
import json


def load_config():
    """ Load configuration from JSON file. """
    with open('config.json', 'r') as config_file:
        return json.load(config_file)


config = load_config()


def build_base_command():
    """ Build the base command for restic operations using SSH configuration. """
    return f"restic -o rclone.program=\"ssh -p 23 {config['ssh_address']} -i {config['ssh_key']} forced-command\" -r rclone:"


def execute_command(command):
    """ Execute a shell command using subprocess. """
    subprocess.run(command, shell=True, check=True)


def get_repo_location():
    """ Prompt the user to enter the repository location. """
    return input('Enter the name of the repo:\n')


def op_init_repo(base_command):
    """ Initialize a new repository. """
    location = get_repo_location()
    command = f'{base_command}{location} init'
    execute_command(command)


def op_backup(base_command):
    """ Backup a folder to a specified repository. """
    location = get_repo_location()
    client_folder_location = input(
        'Enter the location of the client folder to backup e.g. ~/Home\n')
    command = f'{base_command}{location} backup {client_folder_location}'
    execute_command(command)


def op_list_snapshots(base_command):
    """ List all snapshots in a repository. """
    location = get_repo_location()
    command = f'{base_command}{location} snapshots'
    execute_command(command)


def op_list_files_in_snapshot(base_command):
    """ List files in a specific snapshot. """
    location = get_repo_location()
    snapshot_id = input('Enter the id of the snapshot:\n')
    command = f'{base_command}{location} ls --long {snapshot_id}'
    execute_command(command)


def op_restore_file(base_command):
    """ Restore a file from a snapshot. """
    location = get_repo_location()
    snapshot_id = input('Enter the id of the snapshot:\n')
    restore_target_location = input(
        'Enter the folder path to restore the file to:\n')
    path_to_file_in_snapshot = input(
        'Enter the path to the file in the snapshot (Acquired from list files in snapshot):\n')
    command = f'{base_command}{location} restore {snapshot_id} --target={restore_target_location} --include={path_to_file_in_snapshot}'
    execute_command(command)


def op_forget_snapshot(base_command):
    """ Forget a specific snapshot. """
    location = get_repo_location()
    snapshot_id = input('Enter the id of the snapshot to delete:\n')
    command = f'{base_command}{location} forget {snapshot_id}'
    execute_command(command)


def op_prune_repo(base_command):
    """ Prune the repository. """
    location = get_repo_location()
    command = f'{base_command}{location} prune'
    execute_command(command)


def display_menu():
    """ Display the menu options to the user. """
    menu_options = [
        "1. Init a new repo (Initialize a new backup location)",
        "2. Backup",
        "3. List snapshots",
        "4. List files in a snapshot",
        "5. Restore a file from the snapshot",
        "6. Forget a snapshot",
        "7. Prune the repo",
        "8. Exit"
    ]
    print("\nMENU:")
    for option in menu_options:
        print(option)


def main():
    """ Main function to run the backup tool. """
    print("\nMake sure the SSH key is placed in .ssh and the restic version supports compression.")
    print("\nAssumed using restic on client with rclone restic serve on the server.")
    base_command = build_base_command()
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ")
        operations = {
            '1': op_init_repo,
            '2': op_backup,
            '3': op_list_snapshots,
            '4': op_list_files_in_snapshot,
            '5': op_restore_file,
            '6': op_forget_snapshot,
            '7': op_prune_repo,
            '8': lambda _: exit("Exiting the program.")
        }
        operation = operations.get(choice)
        if operation:
            operation(base_command)
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
