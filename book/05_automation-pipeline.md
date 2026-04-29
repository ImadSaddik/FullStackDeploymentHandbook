# Module 5: The automation pipeline

## Local hygiene

### Introduction

In the previous modules, you deployed your application manually. While this is a perfect way to understand how a Linux server works under the hood, doing it every time you write new code is tedious and risky. In this module, you will shift from manual server management to a continuous integration and continuous delivery (CI/CD) pipeline.

However, before you automate anything in the cloud, you must secure your local workflow. Catching a bug or a formatting error on your laptop takes seconds. Catching it after it has been deployed to a server takes minutes or even hours to fix.

In this subchapter, you will enforce code quality at the source. You will configure branch protection rules to stop accidental pushes to your main branch, and you will set up [pre-commit hooks](https://pre-commit.com/) to automatically format your code and catch errors before a commit is even created.
