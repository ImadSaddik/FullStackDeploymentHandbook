# The full-stack deployment book

From bare-metal cloud infrastructure to automated production-ready pipelines

## Introduction

Building a modern web application is only half the battle. Bringing that code to production, making it survive the open internet, and maintaining it over time is an entirely different discipline.

Many developers deploy their applications to managed platforms without knowing how they work. While convenient, these black boxes hide the mechanics of software delivery. So when a server crashes or infrastructure fails, guessing will not save you. To truly master your craft, you must understand what happens behind the scenes.

This book was born out of a simple philosophy: **before you automate anything, you must understand how to execute it manually.**

The book in your hands is the distilled result of eight months of active architectural refinements on a live production server. Every concept, script, and configuration block was tested, broken, and optimized using a real full-stack application: a **Vue.js** frontend, a **FastAPI** backend, and a self-hosted **Meilisearch** engine.

Regardless of your specific software stack, the mechanics detailed here are universal. They apply whether you are spinning up a virtual machine on DigitalOcean, configuring an AWS EC2 container, setting up a bare-metal server, or running a Raspberry Pi on your desk.

You will learn how to design cloud environments from the ground up, secure your entry gateways, configure raw reverse proxies, build modular continuous integration (CI) environments with deep security testing, and deploy code with atomic rollbacks. By the time you finish the final page, your application will not just be live. It will be secure, globally optimized, observable, and built to last.

## The roadmap

This book is structured systematically to guide you from absolute zero to an advanced automation posture.

* **Module 1: The foundation** — Cloud infrastructure provisioning, setting up locked rootless user models, and establishing strict SSH cryptographic authentication.
* **Module 2: The application runtime** — Manual stack deployment, memory swap optimization for resource-constrained systems, Gunicorn process engineering, and Supervisor monitoring.
* **Module 3: Data & search** — Self-hosting and isolating internal database and indexing layers securely behind standard server firewalls.
* **Module 4: Global delivery & app security** — DNS configuration, edge proxy routing, end-to-end SSL/TLS encryption, and robust Nginx web-layer hardening against soft 404 vulnerabilities and automated scanners.
* **Module 5: The automation pipeline** — Shifting security left by constructing a multi-stage GitHub Actions CI/CD framework featuring dependency auditing (SCA), source code scanning (SAST), integration testing, and atomic zero-downtime deployments.
* **Module 6: Optimization & maintenance** — Native log-based traffic analytics with GoAccess, real-time terminal resource observation, dynamic frontend vulnerability scanning (DAST), and automated rolling maintenance.

> [!IMPORTANT]
> Throughout this guide, you will see configuration parameters and text enclosed in angle brackets, such as `<your_domain>.com`, `<your_username>`, or `<your_key_name>`. These are **placeholders**. You must substitute them with your actual values and **remove the brackets** entirely when running commands or saving configuration profiles.

> [!TIP]
> **Slow is smooth, and smooth is lasting.** Do not rush the configuration blocks. Treat each module as an explicit link in your production chain. Understand what each line of code executes before moving to the next.
