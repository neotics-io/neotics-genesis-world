import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT))

from neotics_scene import Scene, load_episode  # noqa: E402
from run_in_genesis import replay  # noqa: E402


def test_both_physics_engines_agree_on_the_arm():
    scene = Scene.load(KIT / "samples" / "depot.scene.json")
    report = replay(scene, load_episode(KIT / "samples" / "depot.episode.json"))
    print(report)
    assert report["frames"] == 250
    assert abs(report["peak_shoulder_rad"] - scene.reach[1]) < 0.15
    assert report["mean_gap_rad"] < 0.08
