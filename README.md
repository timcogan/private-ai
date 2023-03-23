# Private AI

This repository contains simple helper scripts for running a private
AI that you can communicate with over an encrypted Signal channel.

These scripts were put together with a Raspberry Pi 4 in mind, but
any Linux machine should work, theoretically.

## Setup

```bash
$ make init
```

## Run

```bash
$ make
```

## Reset repo

```bash
$ make clean
```

## Troubleshooting

Each piece (Signal messaging and AI chat) can be run in isolation with the following commands.

```bash
$ make run-msg
$ make run-ai
```

The most involved part of this setup is enabling the Signal CLI. You will need to setup a dedicated phone number for the AI's signal account. Google Voice is a simple option for creating a new, dedicated number.
