import dearpygui.dearpygui as dpg
import logging
import paramiko
from datetime import datetime
from fabric import Connection
import hashlib
import os

# ot2
# /data/fragmax/visitors/<proposal>/2-soak
# maxiv
# /data/staff/biomax/tobias/workflow_test/20211214/workflow/2-soak

ot_dir = "/data/fragmax/visitors"
maxiv_dir = "/data/staff/biomax/tobias/workflow_test"
local_dir = ""
default_host = "offline-fe1.maxiv.lu.se"
ssh_client = None
ssh_ot = None
ot_keyfile = "C:/Users/tobkro/ot2_ssh_key"


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
#    with Connection(host=remote_host, user=remote_user, connect_kwargs=connect_kwargs) as c:
#        # Execute the rsync command locally since we're using sshpass to handle password input
#        c.local(rsync_cmd)


# Example usage
# sync_remote_folders_secure('/path/to/local/dir', '/path/to/remote/dir', 'remote_host_address', 'remote_user', 'your_ssh_password')

def transfer_file(local_path, remote_path, hostname, port, username, password):
    try:
        # Create an SSH client instance
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server
        ssh.connect(hostname, port, username, password)

        # Create an SFTP session
        sftp = ssh.open_sftp()

        # Transfer the file
        sftp.put(local_path, remote_path)
        print(f"Successfully transferred {local_path} to {remote_path} on {hostname}")

        # Close the SFTP session and SSH connection
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"Failed to transfer file: {e}")

def backup_files(remote_host, folder_path, ssh_client):
    logger.info(f"host: {remote_host} - making backups of all files in {folder_path}")
    logger.info(f"ssh_client: {ssh_client}")
    try:
        # Get the current date and time for file naming
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Ensure the backup folder exists
        backup_folder = f"{folder_path}/backup"
        stdin, stdout, stderr = ssh_client.exec_command(f'mkdir -p {backup_folder}')
        stdout.read()

        # List all files in the specified folder
        stdin, stdout, stderr = ssh_client.exec_command(f'ls -1 {folder_path}')
        files = stdout.read().decode('utf-8').strip().split('\n')
        logger.info(files)

        # Copy and move each file to the backup folder
        for file in files:
            original_file_path = f"{folder_path}/{file}"
            backup_file_path = f"{backup_folder}/{file}.{current_datetime}"
            # Copy and rename the file
            command = f'cp {original_file_path} {backup_file_path}'
            logger.info(command)
            stdin, stdout, stderr = ssh_client.exec_command(command)
            stdout.read()

        logger.info("Backup completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        ssh_client.close()


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
    logger.info(f'trying to connect to {host_input}...')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    logger.info(f"count dots in {host_input} -> {host_input.count('.')}")
    try:
        if str(host_input).count('.') > 2:
            logger.info(f'run: ssh -i {ot_keyfile} root@{host_input}')
            print(f'run: ssh -i {ot_keyfile} root@{host_input}')
            client.connect(str(host_input), username=username_input, password=password_input, key_filename=ot_keyfile)
        else:
            client.connect(host_input, username=username_input, password=password_input)
    except paramiko.ssh_exception.AuthenticationException:
        client = None
        logger.error(f'connection to {host_input} failed')
        if str(host_input).count('.') > 2:
            logger.info(f'run: ssh -i {ot_keyfile} root@{host_input}')
        else:
            logger.info(f'run: ssh {username_input}@{host_input}')
    if client:
        logger.info(f'connection {host_input} established')   # takes several seconds before exception appears
    return client

# Callback function for the button
def login_maxiv_callback(sender, app_data, user_data):
    username_input = str(dpg.get_value(user_data["username_field"])).replace("\r", "").replace("\n", "")
    password_input = str(dpg.get_value(user_data["password_field"])).replace("\r", "").replace("\n", "")
    hashed_password = hashlib.sha256(password_input.encode('utf-8')).hexdigest()
    host_input = dpg.get_value(user_data["host_field"])
    global ssh_client
    ssh_client = host_login(host_input, username_input, password_input)
    # Log the action
    logger.info(f"user: {username_input}, pass: {hashed_password}, ssh: {ssh_client}")

def login_ot_callback(sender, app_data, user_data):
    username_input = "root"
    password_input = str(dpg.get_value(user_data["otpw_field"])).replace("\r", "").replace("\n", "")
    hashed_password = hashlib.sha256(password_input.encode('utf-8')).hexdigest()
    host_input = dpg.get_value(user_data["otip_field"])
    global ssh_ot
    ssh_ot = host_login(host_input, username_input, password_input)
    # Log the action
    logger.info(f"user: {username_input}, pass: {hashed_password}, ssh: {ssh_client}")

def sync_button_callback(sender, app_data, user_data):
    username_input = str(dpg.get_value(user_data["username_field"])).replace("\r", "").replace("\n", "")
    password_input = str(dpg.get_value(user_data["password_field"])).replace("\r", "").replace("\n", "")
    hashed_password = hashlib.sha256(password_input.encode()).hexdigest()
    proposal_input = dpg.get_value(user_data["proposal_field"])
    proposal_type = dpg.get_value(user_data["combo_box"])
    remote_host = dpg.get_value(user_data["host_field"])
    otip_input = dpg.get_value(user_data["otip_field"])
    folder_path = os.path.join(maxiv_dir, proposal_input, "workflow", "2-soak")
    if not ssh_client:
        logger.error('log into maxiv host computer first')
    else:
        # Log the action
        # /data/staff/biomax/tobias/workflow_test/20211214/workflow/2-soak
        logger.info(f"folder_path: {folder_path}, ssh: {ssh_client}")
        backup_files(remote_host, folder_path, ssh_client)


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


with dpg.window(label="input", width=1000, height=600):

    # Group for the text input
    with dpg.group(horizontal=False):
        dpg.add_text("MAXIV username:")
        username_field = dpg.add_input_text()
        dpg.add_text("MAXIV password:")
        password_field = dpg.add_input_text(password=True)
        dpg.add_text("MAXIV host:")
        host_field = dpg.add_input_text(default_value="offline-fe1")
        dpg.add_text("OT-2 password:")
        otpw_field = dpg.add_input_text(password=True)
        dpg.add_text("OT-2 IP address:")
        otip_field = dpg.add_input_text(default_value="192.252")
        dpg.add_text("proposal:")
        proposal_field = dpg.add_input_text()

    # Group for the combo box
    with dpg.group(horizontal=True):
        dpg.add_text("type:")
        combo_box = dpg.add_combo(items=["academic", "proprietary"])

    with dpg.group(horizontal=True):
        login_maxiv_button = dpg.add_button(label="login MAXIV", callback=login_maxiv_callback,
                                        user_data={"username_field": username_field,
                                                   "password_field": password_field,
                                                   "host_field": host_field})

        login_ot_button = dpg.add_button(label="login OT-2", callback=login_ot_callback,
                                        user_data={"otpw_field": otpw_field,
                                                   "otip_field": otip_field})

        sync_button = dpg.add_button(label="synchronize", callback=sync_button_callback,
                                    user_data={"username_field": username_field,
                                               "password_field": password_field,
                                               "proposal_field": proposal_field,
                                               "host_field": host_field,
                                               "otip_field": otip_field,
                                               "combo_box": combo_box,})

    # Window for logging
    with dpg.child_window(label="Logs", height=100, autosize_x=True):
        dpg.add_text(default_value="", tag="log_display")

logger = setup_logger()

dpg.create_viewport(title='MAXIV <-> OT-2', width=1000, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()