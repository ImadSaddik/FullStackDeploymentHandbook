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
> Throughout this chapter, you will see placeholders inside angle brackets like `<YOUR_LOCAL_MASTER_KEY>`, `<YOUR_STRONG_MASTER_KEY>`, or `<YOUR_DUMP_FILE.dump>`. You must replace these with your actual keys and remove the brackets when running the commands.

### Export your local data

You have two options for getting data into your production search engine.

**Option 1: Export existing data.** If you built your application on your computer, I assume you have a local Meilisearch instance running with your test data. You need to export this data so you can migrate it to the new server.

**Option 2: Seed from scratch.** If you are using my reference repository and do not have a local database running, you can skip this entire section! I have included a Python script ([backend/scripts/seed_meilisearch.py](https://github.com/ImadSaddik/ImadSaddikWebsite/blob/master/backend/scripts/seed_meilisearch.py)) in the codebase that will automatically configure the settings and inject sample documents into your production server later.

> [!TIP]
> If you chose **Option 2**, jump straight to the next section: **Install Meilisearch on the server**.

If you chose **Option 1**, continue reading. Meilisearch offers two ways to back up data: [Snapshots](https://www.meilisearch.com/docs/learn/data_backup/snapshots_vs_dumps#snapshots) and [Dumps](https://www.meilisearch.com/docs/learn/data_backup/snapshots_vs_dumps#dumps).

- Snapshots are exact copies of the database files, meant for quick backups on the exact same Meilisearch version.
- Dumps are essentially a set of instructions used to recreate the database from scratch. Dumps are the safest way to migrate data across different machines or versions.

Because your local computer and your production server might not have the exact same setup, you must use a dump.

Run this command on your **local machine** (while your local Meilisearch instance is running):

```bash
curl -X POST 'http://localhost:7700/dumps' \
  -H 'Authorization: Bearer <YOUR_LOCAL_MASTER_KEY>'
```

You will get a JSON response back that looks like this:

```json
{
  "taskUid": 1,
  "indexUid": null,
  "status": "enqueued",
  "type": "dumpCreation",
  "enqueuedAt": "2026-03-18T10:00:00.000000Z"
}
```

Take note of the `taskUid` number. Creating a dump is an asynchronous operation, which means Meilisearch does it in the background. You can check the status to see when it finishes by using that ID:

```bash
curl -X GET 'http://localhost:7700/tasks/<YOUR_TASK_UID>' \
  -H 'Authorization: Bearer <YOUR_LOCAL_MASTER_KEY>'
```

Once the status in the response says `succeeded`, your dump file (which looks something like `20260318-100000.dump`) will appear in your local `dumps/` directory.

If you prefer using Python instead of the terminal, you can use the official SDK to do all of this automatically.

First, install the SDK:

> [!IMPORTANT]
> Make sure your local Python virtual environment is active before running the install command. The exact command depends on your local setup (e.g., `source venv/bin/activate`, `conda activate`, or `uv venv`).

```bash
pip install meilisearch
```

Then, run this Python code to create the dump and wait for it to finish:

```python
import meilisearch

meilisearch_client = meilisearch.Client("http://localhost:7700", "<YOUR_LOCAL_MASTER_KEY>")
task = meilisearch_client.create_dump()

meilisearch_client.wait_for_task(task.task_uid)
print("Dump created successfully!")
```

### Install Meilisearch on the server

Now, it is time to set up the engine on your production VM.

SSH into your server using your shortcut:

```bash
ssh my-website
```

Download the latest stable Meilisearch binary using their official installation script.

```bash
curl -L https://install.meilisearch.com | sh
```

This script downloads a single, compiled file named `meilisearch` into your current directory. It is completely self-contained, meaning you don't need to install Rust or any other dependencies.

Make the binary executable and move it to the global `/usr/local/bin/` directory. This ensures the command can be run from anywhere on the system, which is required when we turn it into a background service later.

```bash
chmod +x ./meilisearch
sudo mv ./meilisearch /usr/local/bin/
```

Verify the installation was successful by checking the version:

```bash
meilisearch --version
```

If it prints the version number, you are ready to proceed.

### Create a dedicated system user

In [Chapter 1](./01_foundation.md), you learned that running applications as `root` is a massive security risk. You created a standard user for yourself. Now, you are going to take security one step further by creating a [system user](https://wiki.archlinux.org/title/Users_and_groups#Example_adding_a_system_user) specifically for Meilisearch.

System users are "dummy" accounts. They exist purely to own files and run specific background processes. They have no password and cannot accept login attempts, making them immune to SSH brute-force attacks.

Run this command to create the user:

```bash
sudo useradd -d /var/lib/meilisearch -s /bin/false -m -r meilisearch
```

This command looks complex, so let's break down exactly what each flag does:

- `sudo useradd`: This is the command to add a user. It's different from `adduser` (which you used in Chapter 1), as it does not prompt you for a password or full name.
- `-d /var/lib/meilisearch`: This flag sets the user's **home directory**. Instead of the default `/home/meilisearch`, you set it to `/var/lib/meilisearch`, which is the standard Linux directory path for a background service's data.
- `-s /bin/false`: This flag sets the user's **shell**. `/bin/false` is a dummy shell that immediately exits and does nothing. This is what makes it **impossible for anyone to log in** as this user.
- `-m`: This flag tells `useradd` to physically **create the home directory** you specified with the `-d` flag.
- `-r`: This flag creates the **system user**.

Next, create a specific folder inside that home directory for the actual database files, and ensure the new system user owns everything inside its home directory.

```bash
sudo mkdir -p /var/lib/meilisearch/data
sudo chown -R meilisearch:meilisearch /var/lib/meilisearch
```

### Transfer and import the dump

> [!NOTE]
> If you chose **Option 2** (seeding from scratch), you do not have a dump file to transfer. You can skip this section and go straight to **Run Meilisearch as a service**.

You need to get the dump file from your computer over to the server.

First, log out of your active SSH session by typing `exit` or pressing `Ctrl+D`. Once you are back in your local terminal, use the `scp` command to upload the file.

You are going to send it to the `/tmp/` directory for now. We do this because `/tmp/` is openly writable by any user, whereas our final destination (`/var/lib/meilisearch`) is strictly locked down.

```bash
scp /path/to/your/local/dumps/<YOUR_DUMP_FILE.dump> my-website:/tmp/
```

**SSH back in** to the machine.

```bash
ssh my-website
```

Move the dump file from the temporary folder to the Meilisearch directory, and immediately transfer the file ownership to the `meilisearch` user. If you skip the `chown` command, the Meilisearch service will crash because it won't have permission to read the file uploaded by your user account.

```bash
sudo mv /tmp/<YOUR_DUMP_FILE.dump> /var/lib/meilisearch/
sudo chown meilisearch:meilisearch /var/lib/meilisearch/<YOUR_DUMP_FILE.dump>
```
