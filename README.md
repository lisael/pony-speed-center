# Pony Speed Center
The speedometer for [ponylang](https://github.com/ponylang/ponyc).

This project contains Ansible scrpits to install and configure [Codespeed](https://github.com/tobami/codespeed).
We also provide a test runner that can be run in a cron task or used to rebuild the history (this operation is quite long and works best on an empty database)
Finally, ``suite/`` is the benchmark suite run by default by the runner.

## Installation and configuration

A codespeed install consists in two part: a Django web application that saves, processes and show the benchmarks results, and 1 or more "environments" (in codespeed terms).

An environment is a physical host where tests are run. It has to be as stable as possible, as we don't want to benchmark my new CPU, but Pony.

Most of the install part is handled by Ansible, but there are still missing parts:

- web server configuration:
  - TODO:
    - install gunicorn and configure apache/nginx to listen to Django
    - configure the web server to limit who can push some data. (IP? htaccess? both?)
- Initial configuration of codespeed
  - It's not long to do by hand and hard to automate with Ansible. Clearly not a priority here.
- Complete runner install. TBD

### Prerequisites 

To run the ansible scripts, you need to prepare the servers:

- Web server: it's only tested on Debian GNU/Linux stretch (testing)
- Environment servers: tested on Debian stretch and sid (sid has llvm-3.9 and llvm-4.0 packages)

These sever need to have python installed and to be accessible through ssh by a passwordless sudoer.

A bare-metal host is always better, for the purpose of benchmarking, but we provide a bash script that provision a sid lxc container in ``bin/create-lxc-runner.sh``.

### Configuration

The global configuration is in ``ansible/group_vars/all.yml``. This file is NOT self documented at the moment.

Per-host configuration is done in the inventory of your particular environment. An example inventory is ``ansible/dev``.

### Deployment

#### Web server

The first component to install and configure is codespeed.

Once your server is ready, run

```
ansible-playbook -i <your inventory> prepare.yml --limit codespeed
```

Once it's done, there is still a bit of configuration to do. Log in the web server host

```
ssh codespeed.lxc
sudo su codespeed
./manage.py syncdb
# crate an admin when asked to.

# run django dev server
./manage.py runserver 0.0.0.0:8000
```

On the web UI go to http://codespeed.lxc:8000/admin/codespeed/environment/add/ and create an environment. It's the codespeed model for one benchmark runner host.

The only important  field here is `Name` (functionally speaking, the other fields are important to the reader of the bench results!). Remember what you entered here.

TODO: finish the doc here

## Benchmarks

The benchmarks are pony packages in ``runner/suite``. Depending on its configuration, the runner may run any pony package, anywhere on the system.

## Runner

TODO: document the benchmark runner
