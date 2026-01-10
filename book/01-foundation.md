# Module 1: The foundation

## Cloud setup & access

### Introduction

Before you deploy any code, you need a secure environment. You will use DigitalOcean, but these concepts apply to AWS EC2, Linode, or even a Raspberry Pi.

By the end of this section, you will have a server running Ubuntu 24.04 LTS, accessed securely via SSH keys, with password authentication completely disabled.

### Create the project

In this handbook, you will use DigitalOcean to host your web application. If you don’t have an account, [create one here](https://m.do.co/c/4f9010fc5eb3) to get **$200 in free credit**.

After creating your account, create a project to hold your resources. Click on the **New project** button.

![image](./images/1_1_1_create_new_project_inkscape.png)
_The location of the **+ New Project** button on the DigitalOcean dashboard._

Give your project a name and a description. Choose a **descriptive** name so you can remember the purpose of the project later. I named mine “imad-saddik”. Click on **Create Project** when you are done.

![image](./images/1_1_2_information_about_project_step_1.png)
Give the project a name and a description._

DigitalOcean will ask if you want to move resources to this project. Click **Skip for now** because you are starting from scratch.

![image](./images/1_1_3_information_about_project_step_2.png)
_Skip this step because you don’t have any resources yet._

### Create the droplet

Now, create the virtual machine. In DigitalOcean, these are called “droplets”. Click on **Create** in the top menu, then select **droplets**.

A droplet is a Linux-based virtual machine that runs on virtualized hardware. This machine will host the code for your website.

![image](./images/1_1_4_create_droplet_inkscape.jpg)
_Click **Create**, then select **droplets** to start setting up your server._

Choose a **Region** where your VM will be hosted. Always select a region that is geographically near you or your target users. I live in Morocco, so I chose the Frankfurt (Germany) datacenter.

![image](./images/1_1_5_choose_region.png)
_Select the region where your droplet will be hosted._

Next, choose an **Operating System**. Linux is the standard for servers. Select **Ubuntu 24.04 (LTS)** because it is stable and well-supported.

![image](./images/1_1_6_choose_an_image.png)
_Choose the operating system for your droplet._

Now you need to choose the size of your virtual machine. You can pick between **shared CPU** and **dedicated CPU**. Inside each option, you must decide how much **RAM**, **disk space**, and how many **CPU cores** you want.

Dedicated VMs are more expensive because the resources are **reserved only for you**. Adding more RAM, disk space, or CPU cores will also increase the price.

The good thing is that you can **change the droplet size later** if needed. For now, you will create a droplet with a shared CPU and the lowest resources. This costs **$4 per month**, and I will show you how to upgrade it later.

![image](./images/1_1_7_choose_size.png)
_Select the droplet size that fits your needs._

If you need more storage, click **Add Volume** and enter the size in GB. This feature is not free; it costs **$1 per month for every 10 GB**. You can also enable automatic backups if you need them.

![image](./images/1_1_8_space_and_backup.png)
_Additional storage and backup options._

### Configure authentication

This is a critical security step. You can access your server using a **Password** or an **SSH key**. **Always use an SSH key.** Passwords can be guessed, but SSH keys are much safer.

Select **SSH Key** and click on the **Add SSH Key** button.

![image](./images/1_1_9_authentication.png)
_Select SSH key for better security._

To generate a key, open your terminal on your local computer and run this command:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/<your_key_name> -C "<key_comment>"
```

Here is what the arguments do:

- `-t rsa`: Specifies the type of cryptography ([RSA](https://en.wikipedia.org/wiki/RSA_cryptosystem)).
- `-b 4096`: Generates a strong 4096-bit key.
- `-f ~/.ssh/<your_key_name>`: Saves the key with a specific name so you don’t overwrite your default keys.
- `-C "<key_comment>"`: Adds a comment to help you identify the key.

You will be asked to add a **passphrase**. This is an extra password to protect your private key. If someone steals your private key file, they cannot use it without this passphrase.

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/<your_key_name> -C "<key_comment>"

# Output:
Generating public/private rsa key pair.
Enter passphrase for "/home/<your_username>/.ssh/<your_key_name>" (empty for no passphrase):
```

If you do not want to use a passphrase, press **Enter** twice. If you do add one, remember that you will need to enter it every time you log in to the VM.

This is fine for manual login. However, if you have a **CI workflow** that needs to log in automatically, it is better not to set a passphrase.

You have generated the key pair. Now, copy the public key.

```bash
cat ~/.ssh/<your_key_name>.pub
```

The command displays your public key. Copy the entire text starting with `ssh-rsa`. Paste it into the box, give it a name, and click **Add SSH Key**.

![image](./images/1_1_10_adding_a_public_key.png)
_Add the public SSH key._

You can add more than one SSH key by clicking the **New SSH Key** button. This allows you to add a specific key for your CI without a passphrase, while keeping the one on your computer protected with a passphrase.

![image](./images/1_1_11_add_addtional_ssh_keys.jpg)
_Add multiple SSH keys._

You are almost done. Select **Add improved metrics monitoring and alerting** because it is free.

![image](./images/1_1_12_advanced_options.png)
_Select the free monitoring option._

### Finalize and connect

Give your droplet a name you can recognize, add tags, and assign it to the project you created. You can deploy multiple droplets, but for now, keep the quantity set to **1 droplet**.

![image](./images/1_1_13_final_step_before_creating_droplet.png)
_Fill the finalize details section._

Click on **Create droplet**. You will be redirected to the project page. Under **Resources**, you should see a **green dot** next to your droplet. This means it is running.

![image](./images/1_1_14_droplet_in_project_page.png)
_Ensure that the droplet is running and assigned to the project._

Later, if you find that this VM cannot handle the traffic, you can click on **Upsize** to add more resources.

![image](./images/1_1_15_upsize_droplet.png)
_Increase resources by upsizing._

You are now ready to connect to your VM. Find the **IP address** on the project page.

![image](./images/1_1_16_find_ip_address.png)
_Locate the IP address of the VM._

Use the SSH command to connect to the machine. Pass your private key using the `-i` flag and add your IP address after `root@`.

```bash
ssh -i ~/.ssh/<your_key_name> root@<your_droplet_ip>
```

You will see a security warning about the authenticity of host. Type `yes` and hit **Enter** to continue.

```text
The authenticity of host '<your_droplet_ip> (<your_droplet_ip>)' can't be established.
ED25519 key fingerprint is SHA256:...
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Sometimes, the server is not fully ready even though it says "Running". If you see a **Connection closed** message immediately after typing yes, don’t worry.

If this happens, just wait a few seconds and run the SSH command again. It should work the second time.

```text
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '<your_droplet_ip>' (ED69696) to the list of known hosts.
Connection closed by <your_droplet_ip> port 22
```

Once connected, you will see a welcome message similar to this:

```text
*** System restart required ***

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

root@<your_hostname>:~#
```

Update your VM packages by running the following commands:

```bash
sudo apt update
sudo apt upgrade
```

> [!IMPORTANT]
> If you see a configuration screen during the update, select **keep the local version currently installed**. This option ensures you keep the working SSH configuration that DigitalOcean set up for you.

![image](./images/1_1_17_configure_open_ssh_server_warning.png)
_Handle the configuration conflict._

Reboot the machine to complete the upgrade and start using the new kernel and packages.

```bash
reboot
```

The connection will close, but you can ssh to the server again after it reboots. If you want to exit the VM, type exit and hit `Enter` or hit `Ctrl+D`.

### Create a non-root user and configure SSH access

Running everything as **root** is dangerous. If you make a mistake, it might be unrecoverable. Also, if an attacker finds a vulnerability in your app while it is running as root, they gain full control of your server.

Create a new user to act as a security barrier.

```bash
adduser <your_username>
```

You will be asked to set a password and fill in some details. You can skip the details by pressing **Enter**.

```text
New password:
Retype new password:
passwd: password updated successfully
Changing the user information for <your_username>
Enter the new value, or press ENTER for the default
Full Name []: <your_fullname>
Room Number []:
Work Phone []:
Home Phone []:
Other []:
Is the information correct? [Y/n] y
info: Adding new user `<your_username>' to supplemental / extra groups `users' ...
info: Adding user `<your_username>' to group `users' ...
```

Give the new user administrative privileges ([sudo](https://www.sudo.ws/news/)).

```bash
usermod -aG sudo <your_username>
```

Now, log out of the server (`exit` or `Ctrl+D`) and try to log in as your new user.

```bash
ssh -i ~/.ssh/<private_key_name> <your_username>@<your_droplet_ip>
```

You will get an error. This happens because the SSH key you authorized exists only in the `root` user's list. The new user (`<your_username>`) has an empty list. You need to copy the key from `root` to `<your_username>`.

```text
<your_username>@<your_droplet_ip>: Permission denied (publickey).
```

Log back in as **root**.

```bash
ssh -i ~/.ssh/<private_key_name> root@<your_droplet_ip>
```

Run these commands to copy the authorized keys to the new user. You cannot just copy the files; you must also set strict permissions on the `.ssh` directory and its contents.

```bash
# Create the .ssh directory
mkdir /home/<your_username>/.ssh

# Copy the file
cp /root/.ssh/authorized_keys /home/<your_username>/.ssh/authorized_keys

# Set strict permissions
chmod 700 /home/<your_username>/.ssh
chmod 600 /home/<your_username>/.ssh/authorized_keys

# Give the new user ownership of this directory
chown -R <your_username>:<your_username> /home/<your_username>/.ssh
```

Now, exit and try to log in as your new user again.

```bash
ssh -i ~/.ssh/<private_key_name> <your_username>@<your_droplet_ip>
```

It should work now. You will see a prompt like this:

```text
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

<your_username>@<your_hostname>:~$
```

From now on, you will stop using `root` and use this account instead.

### What is next?

You have successfully configured a clean Ubuntu server and secured it with SSH keys. However, your server is still exposed to the open internet.

In the next chapter, **The firewall strategy**, you will lock down the network. You will learn how to configure [UFW](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands) to block unwanted traffic, set up [Fail2Ban](https://github.com/fail2ban/fail2ban) to stop brute-force attacks, and use the Recovery Console if you ever get locked out.
