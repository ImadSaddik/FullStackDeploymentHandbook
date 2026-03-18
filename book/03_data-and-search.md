# Module 3: Data and search

## Self-hosting Meilisearch

### Introduction

With your frontend and backend securely communicating through Nginx, your core application is online. For many basic websites, this setup is enough.

However, modern applications often require fast, typo-tolerant search features. A standard SQL database struggles with this. It is too slow for full-text search and does not handle spelling mistakes well. To solve this, you need a dedicated search engine.

If you are deploying your own project and do not need search, you can technically skip this chapter. But I highly recommend following along. You will learn an important server skill: how to securely deploy an internal database or background service that is completely hidden from the internet.

If you are using my reference repository to practice, we need this engine to make the website fully functional. For this guide, we use [Meilisearch](https://www.meilisearch.com/). It is an open-source, lightning-fast search engine built in Rust.

Hosting your own search engine on the same server as your backend has massive advantages:

- **Zero network latency:** Your API communicates with the search engine over `localhost`, meaning queries resolve in milliseconds.
- **Cost-effective:** You do not have to pay for an expensive managed search SaaS.
- **Maximum security:** Because Meilisearch runs behind your UFW firewall, it is completely invisible to the public internet.

In this chapter, you will export your local search data, install the Meilisearch binary on your server, isolate it using a highly secure "system user," and import your data dumps.
