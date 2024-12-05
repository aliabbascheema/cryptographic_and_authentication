import subprocess
import kerberos
from dotenv import load_dotenv
import os

load_dotenv()

def register_service_principal():
    """
    Register a service principal for Kerberos authentication and create a corresponding keytab file. This function automates the process of adding a service principal and generating a keytab, which is essential for secure service authentication.

    It uses system commands to interact with the Kerberos administration tool, ensuring that the service principal is registered and the keytab is created at the specified path. The function handles potential errors during the registration process and provides feedback on the success or failure of the operations.

    Args:
        None

    Returns:
        None

    Raises:
        subprocess.CalledProcessError: If the registration or keytab creation fails.
    """
    principal = os.getenv('KRB5_SERVICE_PRINCIPAL', 'HTTP/localhost')
    keytab_path = os.getenv('KRB5_KEYTAB_PATH', '/etc/krb5.keytab')

    try:
        print("Registering service principal...")
        subprocess.run(["sudo", "kadmin.local", "-q", f"addprinc -randkey {principal}"], check=True)
        print(f"Service principal {principal} registered successfully.")
        
        # Generate the keytab for the service principal
        subprocess.run(["sudo", "kadmin.local", "-q", f"ktadd -k {keytab_path} {principal}"], check=True)
        print(f"Keytab created at {keytab_path}.")

    except subprocess.CalledProcessError as e:
        print(f"Error while registering principal or creating keytab: {e}")

# Function to authenticate using Kerberos
def authenticate_with_kerberos():
    """
    Authenticate a user with Kerberos using a specified service principal. This function initializes a Kerberos authentication context and generates a ticket token for the user.

    It handles the authentication process by setting up the necessary context and steps to obtain a valid ticket token. If an error occurs during the authentication process, it captures and reports the error.

    Args:
        None

    Returns:
        None

    Raises:
        kerberos.GSSError: If there is an error during the Kerberos authentication process.
    """
    service = "HTTP/localhost"

    try:
        _, krb_context = kerberos.authGSSClientInit(service)
        kerberos.authGSSClientStep(krb_context, "")
        token = kerberos.authGSSClientResponse(krb_context)
        
        print(f"Generated Ticket Token: {token}")
        
    except kerberos.GSSError as e:
        print(f"Kerberos Error: {e}")

def main():
    register_service_principal()
    authenticate_with_kerberos()

if __name__ == "__main__":
    main()
