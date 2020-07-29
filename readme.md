This repo contains the files necessary to replicate a credential stuffing attack. 
It has 3 different containers
* `server` with a login endpoint
* `legitimate_users` with a script to simulate legitimate logins to the server 
* `attacker` with the script to simulate a credential stuffing attack

This repo also contains a folder named `datadog-terraform`. This folder contains the code needed to configure Datadog to visualize this simulation.
