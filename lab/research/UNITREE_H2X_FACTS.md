# Unitree H2-X ("Kung Fu Legend Guardian"): facts file for Curve Short 4 (written 23 Oct 2026)

Tags: P = primary (Unitree's own video/code, papers), S = secondary, EST = our arithmetic, UNV = not verified.
The research agent for this file hit the weekly limit; everything below was checked by hand on 23 Oct.

## 1. What was released
| # | Fact | Tag | Src |
|---|---|---|---|
| 1 | Unitree Robotics posted "Unitree Introducing: H2-X Kung Fu Legend Guardian" on YouTube on 21 Oct 2026; 61 s; 1920x1080 at 50 fps | P | P1 |
| 2 | Its description: "Powerful performance to serve and guard you, with a maximum endurance of approximately 8 hours." | P | P1 |
| 3 | 705,865 views and 7,943 likes by 23 Oct 2026, 17:45 BST | P | P1 (yt-dlp) |
| 4 | On-screen label 0:00-0:01: "Real Footage Throughout No Speed-Up" | P | P1 |
| 5 | On-screen label 0:23-0:25: "Ultra Long Endurance / Standing for Approximately 8 Hours" (so the 8 h figure is for standing) | P | P1 |
| 6 | On-screen label 0:33-0:35 (the masked man with a knife): "Security Demonstration" | P | P1 |
| 7 | On-screen label 0:41-0:53 (the person under the car): "Real Footage of Props for Reference Only" | P | P1 |
| 8 | End card 0:54-0:57: "Extreme testing. No imitation!"; "maintain a safe distance of at least 2-3 meters or more"; "the humanoid robot field is in the early stages of exploration worldwide" | P | P1 |
| 9 | Unitree hasn't published H2-X height, weight, price or launch date; only the runtime | S | S1 |
| 10 | Base H2 for comparison: about 180 cm, about 70 kg, list price $29,900 (retailers vary) | S (UNV for H2-X) | S2, S3 |

## 2. How robots like this learn (the mechanism)
| # | Fact | Tag | Src |
|---|---|---|---|
| 11 | Unitree's own open-source training code (unitree_rl_gym) works in four steps: Train (in the Isaac Gym simulator) → Play → Sim2Sim (MuJoCo) → Sim2Real (the physical robot) | P | P2 |
| 12 | Its default config trains **4,096** simulated robots in parallel (`num_envs = 4096`) | P | P2 (legged_robot_config.py line 5) |
| 13 | Simulation step 0.005 s with `decimation = 4`, so the trained controller acts every 0.02 s = **50 times a second** | P / EST (arithmetic) | P2 |
| 14 | Published method for kung fu on Unitree hardware: KungfuBot (TeleAI / SJTU, NeurIPS 2025) extracts human motion from video, filters and retargets it to the robot, trains a policy in simulation and deploys it on a Unitree G1 for kung fu and dance | P | P3 |
| 15 | Caveat for the script: we don't know H2-X's exact training pipeline; the narration says "robots like this" and "Unitree's own public training code", never "H2-X was trained with 4,096 copies" | — | — |

## 3. Footage (all Unitree Robotics, YouTube, 21 Oct 2026; used in short credited windows under commentary)
| Window | What |
|---|---|
| 0:01.0-0:03.0 | **Frame 0 candidate**: leaps onto a car's boot and flips over it, junkyard at night |
| 0:05-0:09 | Kicks dent a white car's door |
| 0:10-0:14 | Hits a bonnet; dust cloud |
| 0:19-0:22 | Flying and spinning kicks in front of crushed-car stacks |
| 0:23-0:25 | Kick with the "Standing for Approximately 8 Hours" label (top right) |
| 0:27-0:29 | Orange sparks around the robot |
| 0:33-0:40 | Knife "Security Demonstration" (staged; masked actor) |
| 0:41-0:47 | Lifts a car off a prop dummy |

## 4. Sources
- P1 Unitree Robotics, "Unitree Introducing: H2-X Kung Fu Legend Guardian", YouTube, 21 Oct 2026: https://www.youtube.com/watch?v=Y3zb4o47yqA
- P2 unitreerobotics/unitree_rl_gym (GitHub): https://github.com/unitreerobotics/unitree_rl_gym (README; legged_gym/envs/base/legged_robot_config.py)
- P3 Xie et al., "KungfuBot: Physics-Based Humanoid Whole-Body Control for Learning Highly-Dynamic Skills", arXiv 2506.12851, NeurIPS 2025: https://arxiv.org/abs/2506.12851
- S1 BigGo Finance on the H2-X debut (specs undisclosed): https://finance.biggo.com/news/b25f76b1-9b05-4d74-9d7d-f3df2163154c
- S2 Startup Fortune, "Unitree unveils H2-X security robot...": https://startupfortune.com/unitree-unveils-h2-x-security-robot-that-fights-like-a-kung-fu-master/
- S3 robozaps, Unitree H2 price/specs: https://blog.robozaps.com/b/unitree-h2-review
- Coverage: TV Tokyo BIZ (car lift, 8 h), 22 Oct 2026, 451k views: https://www.youtube.com/watch?v=9jcHVAnM97U
