# Cryptographic and Authentication Protocols Project

This project demonstrates cryptographic techniques (AES encryption) and compares authentication protocols (Kerberos and OAuth 2.0) in a Python-based environment. It evaluates the performance of these protocols and generates automated reports.



## Project Structure

```plaintext
cryptographic_and_authentication/
├── aes_encryption.py           # AES encryption and decryption script
├── kerberos_auth.py            # Kerberos authentication script
├── oauth2_auth.py              # OAuth 2.0 authentication script
├── performance_comparison.py   # Script to compare Kerberos and OAuth
├── results/
│   ├── results.txt             # Log file for results
│   ├── performance_chart.png   # Visualization chart
│   └── report.md               # Automated report
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```


## Features

- **AES Encryption**: Demonstrates symmetric encryption for securing data.
- **Kerberos Authentication**: Automates ticket-based authentication using MIT Kerberos.
- **OAuth 2.0 Authentication**: Implements token-based delegated access for secure API usage.
- **Performance Comparison**: Measures and compares the time taken for Kerberos and OAuth 2.0 flows.
- **Visualization**: Generates a bar chart to illustrate protocol performance.
- **Automated Documentation**: Creates logs and a report summarizing the results.

## Prerequisites

### 1. Python 3.8 or higher installed on your system.
### 2. Required Python libraries:
   - `cryptography`
   - `requests`
   - `requests-oauthlib`
   - `matplotlib`
   - `jinja2`
   - `pykerberos`

## Installation

### 1. Clone the repository:
   ```bash
   git clone https://github.com/aliabbascheema/cryptographic_and_authentication.git
   cd cryptographic_and_authentication
  ```
### 2. Python Environment
- **Python 3.8+**
- Create a virtual environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate   # On Windows: venv\Scripts\activate
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### 3. Kerberos Setup
- **Install Kerberos utilities**:
```bash
sudo apt update
sudo apt install krb5-kdc krb5-admin-server krb5-user
```

During installation, you’ll be prompted to set up the Kerberos realm. If you skip this, you can configure it manually.

#### **Step 2: Configure Kerberos Realm**

1. **Edit `/etc/krb5.conf`**:
   Open the Kerberos configuration file:

   ```bash
   sudo nano /etc/krb5.conf
   ```

   Example configuration:

   ```ini
   [libdefaults]
       default_realm = EXAMPLE.COM
       dns_lookup_realm = false
       dns_lookup_kdc = false

   [realms]
       EXAMPLE.COM = {
           kdc = localhost
           admin_server = localhost
       }

   [domain_realm]
       .example.com = EXAMPLE.COM
       example.com = EXAMPLE.COM
   ```

   Replace `EXAMPLE.COM` with your desired realm.

2. **Edit `/etc/krb5kdc/kdc.conf`**:
   Configure the KDC-specific settings:

   ```bash
   sudo nano /etc/krb5kdc/kdc.conf
   ```

   Example configuration:

   ```ini
   [kdcdefaults]
       kdc_ports = 88
       kdc_tcp_ports = 88

   [realms]
       EXAMPLE.COM = {
           master_key_type = aes256-cts
           max_life = 1d
           max_renewable_life = 7d
           acl_file = /etc/krb5kdc/kadm5.acl
           database_name = /var/lib/krb5kdc/principal
           key_stash_file = /etc/krb5kdc/stash
           default_principal_flags = +preauth
       }
   ```

3. **Edit `/etc/krb5kdc/kadm5.acl`**:
   Define access control rules for administrative operations:

   ```bash
   sudo nano /etc/krb5kdc/kadm5.acl
   ```

   Example content:

   ```
   */admin@EXAMPLE.COM *
   ```

   This allows all admin principals to have full access.



#### **Step 3: Create the Kerberos Database**

Initialize the KDC database:

```bash
sudo kdb5_util create -s
```

You will be prompted to set a master password for the database.



#### **Step 4: Add Kerberos Principals**

1. Add an admin principal:

   ```bash
   sudo kadmin.local
   ```

   Inside the `kadmin.local` shell:

   ```bash
   addprinc admin/admin
   ```

   Set a password for the `admin/admin` principal.

2. Add a regular user principal for testing:

   ```bash
   addprinc testuser
   ```

   Set a password for `testuser`.

3. Exit the admin shell:

   ```bash
   exit
   ```



#### **Step 5: Start the Kerberos Services**

Start and enable the KDC and admin services:

```bash
sudo systemctl start krb5-kdc
sudo systemctl start krb5-admin-server
sudo systemctl enable krb5-kdc
sudo systemctl enable krb5-admin-server
```



#### **Step 6: Configure as a Kerberos Client**

1. Ensure `/etc/krb5.conf` matches the server configuration. It should already be configured if you followed the earlier steps.

2. Test the client by obtaining a Kerberos ticket:

   ```bash
   kinit admin/admin
   ```

   Enter the password you set earlier. If successful, you can view your ticket using:

   ```bash
   klist
   ```

   Output should look like:

   ```
   Ticket cache: FILE:/tmp/krb5cc_1000
   Default principal: admin/admin@EXAMPLE.COM

   Valid starting       Expires              Service principal
   12/05/2024  19:45    12/06/2024  19:45    krbtgt/EXAMPLE.COM@EXAMPLE.COM
   ```



#### **Step 7: Test Kerberos Authentication**

1. Add a service principal for testing:

   ```bash
   sudo kadmin.local
   ```

   Inside the `kadmin.local` shell:

   ```bash
   addprinc -randkey host/localhost
   ```

   Export the keytab file for the service:

   ```bash
   ktadd host/localhost
   ```

   Exit the admin shell:

   ```bash
   exit
   ```

2. Test a service authentication using:

   ```bash
   kinit testuser
   kvno host/localhost
   ```

   The `kvno` command fetches a service ticket, indicating successful Kerberos authentication.



#### **Step 8: Debugging**

- Check logs for any issues:
  - `/var/log/krb5kdc.log`
  - `/var/log/krb5lib.log`
- Restart services if needed:

  ```bash
  sudo systemctl restart krb5-kdc
  sudo systemctl restart krb5-admin-server
  ```


### 4. OAuth Setup
- **OAuth Application Registration**:
  - Register your app with a provider like GitHub.
  - Add these variables to `.env`:
    ```plaintext
    CLIENT_ID=<your_client_id>
    CLIENT_SECRET=<your_client_secret>
    AUTHORIZATION_URL=https://github.com/login/oauth/authorize
    TOKEN_URL=https://github.com/login/oauth/access_token
    REDIRECT_URL=<your_redirect_url>
    ```



## Scripts Overview

### 1. **AES Encryption (`aes_encryption.py`)**
   - Encrypts and decrypts a message using AES with CBC mode.
   - Generates a random key and initialization vector (IV).
   - Demonstrates encryption, padding, and decryption.

### 2. **Kerberos Authentication (`kerberos_auth.py`)**
   - Automates the setup of a Kerberos service principal.
   - Authenticates using Kerberos tickets and retrieves a service token.

### 3. **OAuth 2.0 Authentication (`oauth2_auth.py`)**
   - Implements the OAuth 2.0 flow to authenticate and fetch user data.
   - Retrieves an access token and uses it to access a protected resource.

### 4. **Performance Comparison (`performance_comparison.py`)**
   - Compares Kerberos and OAuth 2.0 authentication based on execution time.
   - Outputs a performance chart and a summary report.



## Outputs

1. **`results/results.txt`**: 
   - Execution times for Kerberos and OAuth.
   - OAuth user details (retrieved from the API).

2. **`results/performance_chart.png`**: 
   - A bar chart comparing authentication performance.

3. **`results/report.md`**: 
   - A markdown report summarizing the results and including the performance chart.



## Usage Guide

### 1. Run AES Encryption
```bash
python aes_encryption.py
```

### 2. Run Kerberos Authentication
```bash
python kerberos_auth.py
```

### 3. Run OAuth 2.0 Authentication
```bash
python oauth2_auth.py
```

### 4. Compare Protocols
```bash
python performance_comparison.py
```



## Example Workflow

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Run individual scripts to observe functionality.
3. Execute `performance_comparison.py` to measure and compare protocol performance.



## Dependencies

All dependencies are listed in `requirements.txt`. Install them with:
```bash
pip install -r requirements.txt
```



## Key Notes

1. **Kerberos**:
   - Ensure `/etc/krb5.conf` is correctly configured for your realm.
   - Use a valid service principal (`HTTP/localhost`).

2. **OAuth**:
   - Replace placeholders in `.env` with valid credentials from your OAuth provider.

3. **Virtual Environment**:
   - Always activate the virtual environment before running scripts.



## Future Enhancements

- Extend comparison to additional encryption and authentication protocols (e.g., RSA, JWT).
- Add real-world use cases, such as API integration.
- Automate environment setup using Docker or Ansible.
- Add support for decentralized identity solutions like DIDs.
- Extend the performance evaluation to include scalability tests with multiple concurrent users.


## Author
- **Ali Abbas**

