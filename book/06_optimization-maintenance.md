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
