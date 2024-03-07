import dearpygui.dearpygui as dpg
import logging
import paramiko
from datetime import datetime
from fabric import Connection


def sync_remote_folders_secure(local_dir, remote_dir, remote_host, remote_user, ssh_password):
    """
    Synchronizes a local directory with a remote directory using rsync via Fabric, with password authentication,
    and improves security handling for SSH connections.

    Parameters:
    - local_dir (str): The local directory path to sync from.
    - remote_dir (str): The remote directory path to sync to.
    - remote_host (str): The hostname or IP address of the remote server.
    - remote_user (str): The username to use for the SSH connection.
    - ssh_password (str): The password for SSH authentication.

    Returns:
    None
    """
    # Define SSH connection options with improved security
    connect_kwargs = {"password": ssh_password}

    # Setup SSH options for better security, assuming known_hosts are managed properly.
    ssh_options = "-o UserKnownHostsFile=/path/to/your/known_hosts -o StrictHostKeyChecking=yes"

    # Rsync command using sshpass for password injection, with improved SSH security options
    rsync_cmd = f"sshpass -p '{ssh_password}' rsync -avz -e 'ssh {ssh_options}' {local_dir} {remote_user}@{remote_host}:{remote_dir}"

    # Establish an SSH connection to the remote server
    with Connection(host=remote_host, user=remote_user, connect_kwargs=connect_kwargs) as c:
        # Execute the rsync command locally since we're using sshpass to handle password input
        c.local(rsync_cmd)


# Example usage
# sync_remote_folders_secure('/path/to/local/dir', '/path/to/remote/dir', 'remote_host_address', 'remote_user', 'your_ssh_password')


def backup_files(remote_host, port, username, password, folder_path):
    logger.info(f"making backups of all files in {folder_path}")
    # Create an SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote host
        client.connect(hostname=remote_host, port=port, username=username, password=password)

        # Get the current date and time for file naming
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Ensure the backup folder exists
        backup_folder = f"{folder_path}/backup"
        stdin, stdout, stderr = client.exec_command(f'mkdir -p {backup_folder}')
        stdout.read()

        # List all files in the specified folder
        stdin, stdout, stderr = client.exec_command(f'ls -1 {folder_path}')
        files = stdout.read().decode('utf-8').strip().split('\n')

        # Copy and move each file to the backup folder
        for file in files:
            original_file_path = f"{folder_path}/{file}"
            backup_file_path = f"{backup_folder}/{file}.{current_datetime}"
            # Copy and rename the file
            command = f'cp {original_file_path} {backup_file_path}'
            logger.info(command)
            stdin, stdout, stderr = client.exec_command(command)
            stdout.read()

        print("Backup completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()


# Replace the following variables with your actual details
# backup_files(remote_host="your_remote_host", port=22, username="your_username", password="your_password", folder_path="/path/to/your/folder


# Custom logging handler to redirect log messages to a Dear PyGui text widget
class DPGLogHandler(logging.Handler):
    def __init__(self, widget_id):
        super().__init__()
        self.widget_id = widget_id

    def emit(self, record):
        msg = self.format(record)
        # Get current text from the widget
        current_text = dpg.get_value(self.widget_id)
        # Append the new log message to the current text
        new_text = current_text + msg + '\n'
        # Set the new text value to the widget
        dpg.set_value(self.widget_id, new_text)

def host_login(host_input, username_input, password_input):
    logger.info('trying to connect to {0!s}'.format(host_input))
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(host_input, username=username_input, password=password_input)
    except paramiko.ssh_exception.AuthenticationException:
        logger.error('connection failed')
        ssh_client = None
    if ssh_client:
        logger.info('connection established')   # takes several seconds before exception appears
    return ssh_client

# Callback function for the button
def login_button_callback(sender, app_data, user_data):
    username_input = dpg.get_value(user_data["username_field"])
    password_input = dpg.get_value(user_data["password_field"])
    host_input = dpg.get_value(user_data["host_field"])
    ssh_client = host_login(host_input, username_input, password_input)
    combo_selection = dpg.get_value(user_data["combo_box"])

    # Log the action
    logger.info(f"user: {username_input}, pass: {password_input}, Combo Selection: {combo_selection}")

def sync_button_callback(sender, app_data, user_data):
    username_input = dpg.get_value(user_data["username_field"])
    password_input = dpg.get_value(user_data["password_field"])
    combo_selection = dpg.get_value(user_data["combo_box"])

    # Log the action
    logger.info(f"user: {username_input}, pass: {password_input}, Combo Selection: {combo_selection}")


def setup_logger():
    logger = logging.getLogger("ExampleLogger")
    logger.setLevel(logging.INFO)
    log_widget = "log_display"
    handler = DPGLogHandler(log_widget)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# Initialize Dear PyGui context
dpg.create_context()

#
# rsync
# 1. make backups in maxiv fs
# 2. make backups in ot2 fs
# 3. rsync ot2 -> local fs -> maxiv (csv files are always last edited on ot2
# 4. rsync maxiv -> local fs -> ot-2 (now new backups and edited versions of csv files are synched)
#


with dpg.window(label="input", width=600, height=400):

    default_host = "offline-fe1"
    ssh_client = None

    # Group for the text input
    with dpg.group(horizontal=False):
        dpg.add_text("username:")
        username_field = dpg.add_input_text()
        dpg.add_text("password:")
        password_field = dpg.add_input_text(password=True)
        dpg.add_text("MAXIV host:")
        host_field = dpg.add_input_text(default_value="offline-fe1")
        dpg.add_text("OT-2 IP address:")
        otip_field = dpg.add_input_text(default_value="192.252")
        dpg.add_text("proposal:")
        proposal_field = dpg.add_input_text()

    # Group for the combo box
    with dpg.group(horizontal=True):
        dpg.add_text("type:")
        combo_box = dpg.add_combo(items=["academic", "proprietary"])

    with dpg.group(horizontal=True):
        login_button = dpg.add_button(label="login", callback=login_button_callback,
                                    user_data={"username_field": username_field,
                                               "password_field": password_field,
                                               "proposal_field": proposal_field,
                                               "combo_box": combo_box,})

        sync_button = dpg.add_button(label="synchronize", callback=sync_button_callback,
                                    user_data={"username_field": username_field,
                                               "password_field": password_field,
                                               "proposal_field": proposal_field,
                                               "combo_box": combo_box,})

    # Window for logging
    with dpg.child_window(label="Logs", height=100, autosize_x=True):
        dpg.add_text(default_value="", tag="log_display")

logger = setup_logger()

dpg.create_viewport(title='MAXIV <-> OT-2', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()