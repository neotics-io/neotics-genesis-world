"""Replay a Neotics Episode in Genesis and report how far it lands from the run it was recorded in.

    python run_in_genesis.py samples/depot.scene.json samples/depot.episode.json

Episodes are recorded in MuJoCo, so this is a second opinion from a different physics engine on the same robot,
the same scene and the same commands.
"""
import json
import sys
import tempfile
from pathlib import Path

import genesis as gs
import numpy as np

from neotics_scene import Scene, load_episode
from scene_to_urdf import to_urdf


def build(scene: Scene, urdf_dir: str):
    gs.init(backend=gs.cpu, logging_level="warning")
    world = gs.Scene(sim_options=gs.options.SimOptions(dt=0.01), show_viewer=False)
    world.add_entity(gs.morphs.Plane())
    for box in scene.boxes:
        world.add_entity(gs.morphs.Box(pos=box.center, size=box.size, fixed=True))
    for item in scene.items:
        density = item.mass / (item.size[0] * item.size[1] * item.size[2])
        world.add_entity(gs.morphs.Box(pos=item.center, size=item.size), material=gs.materials.Rigid(rho=density))
    urdf = Path(urdf_dir) / f"{scene.robot_name}.urdf"
    urdf.write_text(to_urdf(scene), encoding="utf-8")
    # The arm is bolted down, and only its joints are being compared here
    arm = world.add_entity(gs.morphs.URDF(file=str(urdf), fixed=True, collision=False))
    world.build()
    return world, arm


def replay(scene: Scene, episode: dict) -> dict:
    with tempfile.TemporaryDirectory() as folder:
        world, arm = build(scene, folder)
        dofs = [arm.get_joint(name).dofs_idx_local[0] for name in episode["joints"]]
        arm.set_dofs_kp(np.full(len(dofs), 400.0), dofs)
        arm.set_dofs_kv(np.full(len(dofs), 40.0), dofs)
        steps = round(1 / (episode["rate_hz"] * 0.01))
        measured = []
        for ctrl in episode["ctrl"]:
            measured.append(arm.get_dofs_position(dofs).cpu().numpy().copy())
            arm.control_dofs_position(np.array(ctrl), dofs)
            for _ in range(steps):
                world.step()
    gap = np.abs(np.array(measured) - np.array(episode["qpos"]))
    return {"frames": len(measured), "mean_gap_rad": float(gap.mean()), "worst_gap_rad": float(gap.max()), "peak_shoulder_rad": float(np.array(measured)[:, 1].max())}


if __name__ == "__main__":
    print(json.dumps(replay(Scene.load(sys.argv[1]), load_episode(sys.argv[2])), indent=2))
