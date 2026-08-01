# Full stack deployment book

![The full-stack deployment repo cover](./images/repo_cover.jpg)

A practical guide to setting up, securing, and automating full-stack web applications on virtual machines or bare-metal servers.

I wrote this book after spending months running and refining a live production server. It walks you through building a complete web application stack, including a frontend, an API backend, databases, and search engines, on virtual machines or bare-metal servers.

## Development setup

### Prerequisites

`LibreOffice` is required for automatically generating `PDF` slides from `ODF` files. If you don't have it installed, you can find the instructions on the [official download page](https://www.libreoffice.org/download/download-libreoffice/).

### Git hooks

This repository uses git hooks to automatically build PDF files whenever presentation slides are updated. To set up the hooks, run:

```bash
./scripts/install-hooks.sh
```
