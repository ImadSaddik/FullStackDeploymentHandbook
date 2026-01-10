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

Give your project a name and a description. Write something expressive so you can remember the purpose of the project later. I named mine “imad-saddik”. Click on **Create Project** when you are done.

![image](./images/1_1_2_information_about_project_step_1.png)
Give the project a name and a description._

DigitalOcean will ask if you want to move resources to this project. Click **Skip for now** because you are starting from scratch.

![image](./images/1_1_3_information_about_project_step_2.png)
_Skip this step because you don’t have any resources yet._
