# Module 4: Global delivery & Security

## Domains and SSL

### Introduction

Up until now, your application has been accessible via a raw IP address. While this proves your server works, it is not user-friendly, and more importantly, it is not secure. Browsers will flag your website as "Not Secure" because traffic is sent in plain text using [HTTP](https://en.wikipedia.org/wiki/HTTP).

In this chapter, you will purchase a custom domain name, connect it to your DigitalOcean droplet using [DNS records](https://www.cloudflare.com/learning/dns/dns-records/), and secure all traffic with free, auto-renewing [SSL certificates](https://www.cloudflare.com/learning/ssl/what-is-an-ssl-certificate/) via [Let's Encrypt](https://letsencrypt.org/).
