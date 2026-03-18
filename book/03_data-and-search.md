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

> [!IMPORTANT]
> Throughout this chapter, you will see placeholders inside angle brackets like `<YOUR_LOCAL_MASTER_KEY>` or `<YOUR_STRONG_MASTER_KEY>`. You must replace these with your actual keys and remove the brackets when running the commands.

### Export your local data

You have two options for getting data into your production search engine.

**Option 1: Export existing data.** If you built your application on your computer, I assume you have a local Meilisearch instance running with your test data. You need to export this data so you can migrate it to the new server.

**Option 2: Seed from scratch.** If you are using my reference repository and do not have a local database running, you can skip this entire section! I have included a Python script ([backend/scripts/seed_meilisearch.py](https://github.com/ImadSaddik/ImadSaddikWebsite/blob/master/backend/scripts/seed_meilisearch.py)) in the codebase that will automatically configure the settings and inject sample documents into your production server later.

> [!TIP]
> If you chose **Option 2**, jump straight to the next section: **Install Meilisearch on the server**.
