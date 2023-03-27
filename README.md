# Private AI

![PrivateAI](https://github.com/timcogan/private-ai/blob/assets/logo.png)

This repository enables communication over an encrypted Signal
channel with a private AI.

These scripts were put together with a Raspberry Pi 4 in mind, but
any Linux machine should work.

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

Each component can be run in isolation with the following commands.

```bash
$ make run-msg  # Test Signal messaging
$ make run-ai  # Test AI
```

The most involved part of this setup is enabling the Signal CLI. You will need to create a dedicated phone number for the AI's signal account. Google Voice is a simple option for creating a dedicated number.
