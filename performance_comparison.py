import time
import os
from kerberos_auth import main
from oauth2_auth import fetch_protected_resource, get_access_token
import matplotlib.pyplot as plt
from jinja2 import Template

# Create results directory if it doesn't exist
os.makedirs('results', exist_ok=True)

# Measure Kerberos performance
start_time = time.time()
main()
kerberos_time = time.time() - start_time

# Measure OAuth performance
start_time = time.time()
token = get_access_token()
user_info = fetch_protected_resource(token)
oauth_time = time.time() - start_time

# Format user info: If it's a dictionary, join the key-value pairs into a string
if isinstance(user_info, dict):
    formatted_user_info = '\n'.join([f"{key}: {value}" for key, value in user_info.items()])
else:
    # Handle case where user_info is not a dictionary (fallback)
    formatted_user_info = user_info

# Log results
with open("results/results.txt", "w") as f:
    f.write(f"Kerberos Time: {kerberos_time:.2f}s\n")
    f.write(f"OAuth Time: {oauth_time:.2f}s\n")
    f.write(f"OAuth User Info:\n{formatted_user_info}\n")

# Data for chart
protocols = ['Kerberos', 'OAuth 2.0']
times = [kerberos_time, oauth_time]

# Create bar chart
plt.bar(protocols, times, color=['blue', 'green'])
plt.title("Authentication Performance Comparison")
plt.xlabel("Protocols")
plt.ylabel("Time (seconds)")
plt.savefig("results/performance_chart.png")
plt.close()

# Report Template
report_template = """
# Cryptographic and Authentication Protocol Comparison

## Results
- **Kerberos Authentication Time**: {{ kerberos_time }} seconds
- **OAuth 2.0 Authentication Time**: {{ oauth_time }} seconds

## User Info from OAuth
```
  {{ formatted_user_info }}
```
## Performance Chart
![Performance Chart](performance_chart.png)
"""

# Data for the report
data = {
    "kerberos_time": kerberos_time,
    "oauth_time": oauth_time,
    "formatted_user_info": formatted_user_info,
}

# Render the report
template = Template(report_template)
report_content = template.render(data)

# Save the report
with open("results/report.md", "w") as f:
    f.write(report_content)

print("Performance comparison completed and archived.")
