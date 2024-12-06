import subprocess
import kerberos
from dotenv import load_dotenv
import os

load_dotenv()

def register_service_principal():
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
