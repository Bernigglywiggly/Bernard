# Microduck (Pollen Robotics): facts for Curve Short 7

Checked 24 Oct 2026 against primary sources. Row numbers are what the script's `facts=` fields point at.
Anything not in this file does not go on screen or in the voice.

## Sources

- **P1** Pollen Robotics, "We made a new robot." (YouTube RAtzEyGBGFU), uploaded 27 Aug 2026, 2,093,384 views on 24 Oct, 86 s, 4K.
  Captions in the video: "RAW FOOTAGE", "Balance recovery" (16-32 s), "Slow motion x0.25" (34-40 s), "Floor picking"
  (42-54 s), "Roller skating" (56-64 s), "Chatting" + "Every single Microduck has its own unique voice" (66-84 s).
- **P2** Pollen Robotics, "Microduck Sim 2 Real." (YouTube szW7N_7B3tU), 27 Aug 2026, 189,250 views, 24 s, 4K.
  Split screen: left = simulation, right = real robot. On-screen line: "Straight from simulation to the robot" (5-8 s).
- **R1** github.com/pollen-robotics/microduck_rl (Apache-2.0 code; 3D meshes CC BY-NC-SA 4.0, so we never show their
  meshes), README.md and AGENTS.md on branch `develop`, read 24 Oct 2026. 2,593 stars.
- **R2** github.com/pollen-robotics/microduck (the robot runtime), README + docs/robot/simulation.md, 10,665 stars.
- **N1** NVIDIA Technical Blog, "Using AI Agents to Teach Robots Like Microduck to Walk in Simulation", 23 Oct 2026.
- **N2** NVIDIA GTC Berlin keynote (YouTube v-NGxyPjcrE), 23 Oct 2026, 6,506,462 views: Microducks on stage.
- **H1** huggingface.co/blog/nvidia/microduck-isaac-lab-sim-to-real (tutorial).

## The robot

| # | Fact | Source |
|---|---|---|
| 1 | About 25 cm tall, about 800 g (P1: 25 cm, 780 g) | P1, R1 README |
| 2 | 14 Dynamixel XL330 servos in the joints (P1 counts 15 degrees of freedom: the mouth servo has no joint in the sim model) | R1 AGENTS.md, R2 |
| 3 | Front camera, 8x8 depth sensor, two IMUs | P1 |
| 4 | Pre-order $399 before taxes and shipping, deliveries targeted before Christmas 2026 | P1 description |
| 5 | Open source (robot code Apache-2.0) | R1, R2 |
| 6 | Pollen Robotics is part of Hugging Face | public record (Apr 2025 acquisition) |
| 7 | The head is about 38% of the body mass ("a 38%-of-body-mass head MUST oscillate while walking") | R1 AGENTS.md |

## How it learns (all from its own training repo)

| # | Fact | Source |
|---|---|---|
| 10 | Reinforcement learning (PPO) in a simulator (mjlab on MuJoCo Warp); policies run at 50 Hz, exported to ONNX and put on the real robot | R1 README |
| 11 | "train the walking policy (uses your GPU; ~1-2 h for a usable gait at 4096 envs)" | R1 README Quickstart |
| 12 | 4,096 simulated ducks train at once (`--env.scene.num-envs 4096`) | R1 README, AGENTS.md |
| 13 | Walking rewards include: staying upright (`upright`), following the commanded velocity (`track_linear_velocity`, `track_angular_velocity`: the joystick command), lifting the feet (`foot_clearance`, `foot_swing_height`, target 2 cm), air time, and penalties for foot slip and jerky actions | R1 microduck_velocity_env_cfg.py |
| 14 | No reference animation: for get-up and pose tasks the reward is the end pose only, "NOT keyframe/waypoint trajectories ... The path is what RL is supposed to discover." | R1 AGENTS.md |
| 15 | Fall recovery is its own trained skill (`VelStand`: "Walking + fall recovery in one policy"; `StandUp`: "Stand up from face-down/face-up/sitting") | R1 README task table |
| 16 | The policies exploit loopholes: "RL optimizes the letter of the reward. Every under-specified degree of freedom will be exploited (ballistic whip instead of a roll, shoulder-roll instead of sagittal, head-tripod instead of standing)." Also "butt-hopping, crash-sits" from a sign mistake | R1 AGENTS.md |
| 17 | Engineers expect "2–5 iterations of reward-hacking whack-a-mole" per new skill | R1 AGENTS.md |

## The deliberately wrong bodies (domain randomisation, walking task)

Re-sampled for every simulated duck at every reset ("per-env").

| # | What changes | Range | Source |
|---|---|---|---|
| 20 | Mass and inertia | ±5% | R1 vel cfg `MASS_INERTIA_RANDOMIZATION_RANGE` |
| 21 | Centre of mass (balance point) of trunk and head | ±3 mm, ramped to ±8 mm by curriculum | R1 vel cfg `COM_RANDOMIZATION_RANGE` |
| 22 | Foot grip (friction) | 0.7x to 1.3x | R1 vel cfg `foot_friction` |
| 23 | Battery voltage, voltage sag under load, command delay, servo friction | per-env | R1 README "Actuator model" |
| 24 | Pushes: a sudden velocity change of up to ±0.3 m/s | every 3 to 6 s | R1 vel cfg `VELOCITY_PUSH_*` |
| 25 | IMU mounting error | up to 6° | R1 vel cfg |
| 26 | Gear play ("backlash") variants | ±1° per servo | R1 README |
| 27 | Why: "actuator fidelity is most of the sim2real gap" for tiny servos | R1 README |

## Do not use

- "20,000 pre-orders": unverified.
- "Nvidia's robot": it is Pollen's (Hugging Face). Nvidia featured it (N1, N2).
- Any derived total such as "N million shoves" or "N days of practice": depends on which checkpoint shipped; not worth an estimate label.
- Their 3D meshes (CC BY-NC-SA, non-commercial). Our 3D duck is our own design, sized from the Apache-licensed MJCF.
