# Module 6: Optimization & maintenance

## Observability

### Introduction

Your deployment pipeline is running smoothly, your application is live, and traffic is flowing through Cloudflare. But running a server without visibility is like driving a car with a blacked-out windshield. You might be moving forward, but you cannot see the obstacles until you crash.

In this subchapter, you will transition from a blind deployment to a fully observed system. You will learn how to monitor your traffic natively without using heavy, privacy-invasive scripts like Google Analytics. You will install a terminal-based system monitor to track your resource limits in real time, and you will learn how to read your access logs to identify, isolate, and permanently ban web bots and malicious actors at the network edge.

### Server-side analytics with GoAccess

You naturally want to know how many people are using your website, which content is popular, and where your visitors come from. However, loading client-side JavaScript tracking scripts hurts frontend rendering speeds and forces you to show intrusive cookie consent banners to protect user privacy.

Since you are running Nginx, you already have a perfect data source: your access logs. Every single request for a web page, an API endpoint, or a static asset is recorded automatically by Nginx. You can parse these raw logs in real time using [GoAccess](https://github.com/allinurl/goaccess), a fast, open-source terminal log analyzer.

Install GoAccess on your server:

```bash
sudo apt install goaccess -y
```

To view a live analysis directly inside your active SSH session, point GoAccess to your production Nginx access log file and specify the combined log format:

```bash
sudo goaccess /var/log/nginx/<your_domain>-access.log --log-format=COMBINED
```

The terminal will instantly switch to an interactive, graphical dashboard layout.

![GoAccess terminal dashboard showing web server statistics for imadsaddik.com on December 7, 2025, displaying total requests, unique visitors, requested URLs, and static requests.](./images/6_1_1_go_access_dashboard.png)
_The GoAccess interactive terminal dashboard displays web server statistics directly inside your SSH session._

You can navigate this dashboard using your arrow keys, press `Tab` to shift between data panels, or press `q` to exit back to your standard shell. The tool breaks your raw log lines down into important metrics, including:

* **Unique visitors:** Tracks actual daily visitor trends separate from total page views.
* **Requested files:** Shows exactly which URL endpoints are drawing traffic.
* **Static assets:** Isolates image, CSS, and JS file requests from application logic.
* **HTTP status codes:** Highlights server anomalies, such as tracking how often users hit 404 or 500 errors.

### Build a secure web dashboard

While a terminal interface is highly efficient for quick checks over SSH, you might prefer a visual dashboard accessible from a web browser. GoAccess can generate a clean, standalone HTML dashboard. However, since this dashboard displays internal server traffic patterns, you must protect it so the public cannot access it.

You will use HTTP basic authentication to lock down the file. First, install the utility suite containing the password generation tools:

```bash
sudo apt install apache2-utils -y
```

Now, generate an encrypted password file. You will place it inside the secure Nginx configuration directory:

```bash
sudo htpasswd -c /etc/nginx/.htpasswd admin
```

The system will prompt you to enter and verify a strong password for your `admin` user.

Next, open your primary Nginx server configuration file to create a routing rule for your analytics file:

```bash
sudo nano /etc/nginx/sites-available/<your_domain>.com
```

Locate your secure, port 443 `server` block. Paste this location directive right above your general SPA fallback routes:

```nginx
location = /analytics.html {
    root /web_app/frontend/dist;
    auth_basic "Restricted Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

Save the file and exit the editor. Test the configuration structure and reload the server to apply the authentication block:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Now, manually trigger GoAccess to compile your current access log data into a static HTML report placed inside your frontend distribution folder:

```bash
sudo goaccess /var/log/nginx/<your_domain>-access.log -o /web_app/frontend/dist/analytics.html --log-format=COMBINED
```

Open your browser and navigate to `https://<your_domain>.com/analytics.html`. The browser will instantly pause and prompt you for your username and password. Enter your credentials to access the full graphical dashboard interface.

![GoAccess HTML report dashboard showing web traffic analysis from July 5 to July 11, 2026, featuring overview metrics, a unique visitors per day line chart, and an Autonomous System Numbers (ASN) bar chart.](./images/6_1_2_go_access_html_page.png)
_The secure GoAccess HTML dashboard displaying interactive charts and detailed request metrics._

### Log rotation and automation

The HTML report you just generated is static. It only shows data captured up to the exact second you ran the command. To keep it accurate, you need to automate the compilation process.

Furthermore, Linux systems use a mechanism called log rotation ([logrotate](https://linux.die.net/man/8/logrotate)) to prevent files from growing indefinitely. Every night, the system compresses yesterday's Nginx logs into a separate file ending in `.gz`. If your script only reads the active text log, your web dashboard will reset to zero every morning.

To fix both issues, you will create an automated cron job that pipes your active and compressed logs directly into GoAccess:

```bash
sudo crontab -e
```

Go to the bottom of the cron file and add this entry to rebuild the dashboard every hour on the hour:

```text
0 * * * * zgrep -h . /var/log/nginx/<your_domain>-access.log* | goaccess - -o /web_app/frontend/dist/analytics.html --log-format=COMBINED
```

Here is exactly what this command is doing:

* `zgrep -h .`: The `zgrep` utility allows Linux to search inside compressed files without wasting time decompressing them to disk first. The `*` wildcard tells it to look at both your current log file and your old `.gz` backups.
* `|` (Pipe): Passes the entire historical data stream directly into GoAccess.
* `-` (Dash): Tells GoAccess to read the incoming log data from standard input instead of opening a physical file path.

### Monitor system resources with Btop

With your traffic analytics active, you now need to monitor the resource performance of your server. Running a full stack of Nginx, FastAPI, and Meilisearch inside a low-RAM environment leaves very little room for error.

Ubuntu includes a classic monitor called `top`, but it is text-heavy and difficult to read at a glance. You will install [Btop](https://github.com/aristocratos/btop), a modern, terminal-based resource monitor that visualizes your processes, memory trees, and CPU states cleanly.

Download the standalone precompiled binary directly from the official repository:

```bash
wget https://github.com/aristocratos/btop/releases/download/v1.4.0/btop-x86_64-linux-musl.tbz
```

> [!NOTE]
> The command downloads Btop version 1.4.0 for 64-bit Linux systems. Check the [Btop releases page](https://github.com/aristocratos/btop/releases) to find the latest version or packages for other hardware architectures.

Extract the compressed file:

```bash
tar -xjf btop-x86_64-linux-musl.tbz
```

Move into the extracted directory and install the tool globally:

```bash
cd btop
sudo make install
```

By default, standard Linux security boundaries prevent non-root processes from reading low-level hardware sensors like power usage or detailed CPU core metrics. Grant Btop direct sensor access by setting system capabilities on the binary:

```bash
sudo make setcap
```

Now, return to your main directory, clean up the installer files, and launch Btop:

```bash
cd ..
rm -rf btop btop-x86_64-linux-musl.tbz
btop
```

The terminal will switch into a dynamic dashboard displaying your server's performance metrics.

![btop terminal system monitor showing low resource usage, displaying CPU activity, memory consumption at 52%, disk utilization, network traffic graphs, and a running process tree layout.](./images/6_1_3_btop_dashboard.png)
_The Btop interface visualizes CPU load, memory utilization, and active process hierarchies simultaneously._

When running a full stack on a small VM with only 512MB or 1GB of RAM, you should closely watch these specific indicators:

* **The memory map (Left):** If your RAM fills up with active processes, the Linux kernel will start moving inactive, cold memory pages into your slower swap file to protect the system from running out of memory.
* **The process tree (Right):** This panel displays your active applications sorted by resource footprint. You can easily watch your `meilisearch` instance and clustered Python `gunicorn` worker processes to check for abnormal memory growth or CPU spikes.

### Identify and ban persistent outliers

Now that you have full observability over your traffic and system resources, you can use these tools together to defend your infrastructure.

If you look closely at your GoAccess dashboard under the **Requested files (URLs)** panel, you will often spot continuous requests for paths like `/wp-login.php`, `/admin/config.php`, or `/new.php`. Because your application is built on FastAPI and Vue, these files do not exist on your file system. These requests are sent by automated malicious bots scanning the open internet for known security flaws.

While your Nginx configuration safely drops these scans with a 404 response, these bots still consume memory, compete for network sockets, and clutter your logs. When a persistent scraper targets your application, you should step in and block it completely at the network edge.

#### Pinpoint the top offenders

Finding a single malicious IP address out of thousands of log lines can be difficult. You can automate this process by writing a short Python script that parses your GoAccess JSON records to highlight extreme traffic anomalies.

First, export your current dashboard statistics into a raw data file:

```bash
sudo goaccess /var/log/nginx/<your_domain>-access.log -o /web_app/goaccess.json --log-format=COMBINED
```

Create a diagnostic script inside your project root:

```bash
nano /web_app/find_bad_actors.py
```

Paste the following code:

```python
import json
import sys

try:
    with open('/web_app/goaccess.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: Could not find goaccess.json file.")
    sys.exit(1)

hosts = data.get('hosts', {}).get('data', [])

print(f"{'IP Address':<20} {'Total Hits':<15} {'Traffic Share':<15}")
print("-" * 50)

for host in hosts[:10]:
    ip = host.get('data')
    hits = host.get('hits', {}).get('count', 0)
    percent = host.get('hits', {}).get('percent', "0.00%")
    print(f"{ip:<20} {hits:<15} {percent:<15}")

print("-" * 50)
print("Review Checklist:")
print("Look for severe traffic imbalances (outliers). If the top IP has")
print("thousands of hits while others have fewer than 50, block it.")
```

Run the parser script:

```bash
python3 /web_app/find_bad_actors.py
```

The script will parse the log data and output a clean list of your top traffic sources:

```text
IP Address           Total Hits      Traffic Share  
--------------------------------------------------
45.148.10.246        5542            35.84%         
4.230.26.9           370             2.39%          
4.189.112.79         252             1.63%          
--------------------------------------------------
```

> [!WARNING]
> Do not ban entries blindly. Analyze your data carefully for extreme **outliers**. In the diagnostic report above, the top IP address accounts for over 35% of all server traffic, while the second entry drops down to a normal baseline. The top address is clearly an automated scanner, whereas the lower entries represent legitimate human activity.

#### Block attackers at the firewall level

Once you isolate a clear outlier IP address, you can use **UFW** to drop the traffic immediately. This action blocks the attacker at the network layer, preventing their packets from reaching Nginx or consuming your application's resources.

Run the firewall block command:

```bash
sudo ufw deny from 45.148.10.246 to any
```

Verify that the new network barrier is active:

```bash
sudo ufw status
```

Your system firewall rule table will update to confirm the block:

```text
Status: active

To                         Action      From
--                         ------      ----
Nginx Full                 ALLOW       Anywhere                  
OpenSSH                    ALLOW       Anywhere                  
Anywhere                   DENY        45.148.10.246             
Nginx Full (v6)            ALLOW       Anywhere (v6)             
OpenSSH (v6)               ALLOW       Anywhere (v6)             
```

The server will now actively drop all connection attempts from that specific source on sight.

### What is next?

Your server infrastructure is fully secure, automated, and observable. You can track user traffic natively, monitor hardware limits in real time, and block network attackers cleanly.

In the upcoming subchapter, **Chapter 6.2: Reliability**, you will put your server under stress to see how it performs under load. You will learn how to simulate real user traffic using Locust, optimize your Nginx log rotation configurations for long-term data collection, and write an automated cleanup script to prevent system logs and caches from filling up your disk space.
