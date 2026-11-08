# Neotics kit for Genesis

This folder is Neotics' own work, added to our copy of [Genesis](https://github.com/Genesis-Embodied-AI/genesis-world). It replays a recorded Neotics run in a second physics engine and reports how far the two disagree.

It is one part of the Neotics stack. Every fork in [neotics-io](https://github.com/neotics-io) reads the same two files:

- a **Neotics Scene** (`samples/depot.scene.json`): the room, the obstacles, the arm and the named places;
- a **Neotics Episode** (`samples/depot.episode.json`): a run recorded in MuJoCo, with time, joint positions and commands.

The depot is a sample made for these tools. It is not an entry or an answer for any [Neotics challenge](https://lab.neotics.io).

## Use it

Run from this folder:

```bash
python run_in_genesis.py samples/depot.scene.json samples/depot.episode.json
```

## How it's checked

Installs this repository's Genesis, replays the MuJoCo-recorded sample and requires both engines to agree on the arm. This runs on GitHub in `.github/workflows/neotics.yml`, on every change to this folder.

## Licence

See [`LICENSE`](LICENSE). It covers this folder only.
