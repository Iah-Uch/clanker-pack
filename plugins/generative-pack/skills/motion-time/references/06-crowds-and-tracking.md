# Crowds and tracking

Verified against each repo on 2026-10-15.

## RVO2 / ORCA (snape/RVO2)

- License and status: Apache-2.0, 977 stars, last push Oct 2026.
- Technique: optimal reciprocal collision avoidance. Many independent agents avoid each other without communicating, because each takes half of the responsibility for avoiding every pairwise collision. Choosing an agent's action reduces to a low-dimensional linear program. The README reports collision-free actions for thousands of agents in a few milliseconds. The library is C++98 and two-dimensional.
- Reach for it when: crowds, swarms, or any many-agent navigation where agents must not overlap.
- Mechanism (literature, van den Berg et al.): for agent A and neighbor B with relative position p and combined radius r, the velocity obstacle is the set of relative velocities that lead to collision within a time horizon tau. Take the smallest change u that moves the current relative velocity out of the obstacle, and let each agent take half of it: the ORCA constraint is the half-plane {v : (v − (v_A + u/2))·n ≥ 0}, where n is the outward normal of the obstacle boundary at that point. Each agent then picks the velocity inside the intersection of all its half-planes (and its max speed) that is closest to its preferred velocity: a small linear program in 2D, solved incrementally; if infeasible, a fallback program minimizes the maximum violation.
- Idea: when two agents share a conflict, split the correction between them instead of making one yield; the symmetry removes oscillation.
- Watch out: 2D only.

## ByteTrack (FoundationVision/ByteTrack)

- License and status: MIT, 6.7k stars, last push Jun 2024.
- Technique: multi-object tracking by associating every detection box, including low-score ones, instead of discarding them. Low-score boxes are matched to existing tracks by similarity, which recovers occluded objects and filters background. Per its README, this improved IDF1 by 1 to 10 points when applied to nine trackers.
- Reach for it when: you need persistent identities for objects across video frames.
- Mechanism (literature, the paper's steps): predict each track's box with a Kalman filter; split detections into high-score and low-score by thresholds; match tracks to high-score detections by IoU (intersection over union) with the Hungarian algorithm; match the tracks left over to the low-score detections by IoU; start new tracks from unmatched high-score detections; keep unmatched tracks alive for a number of frames before deleting them.
- Idea: do not throw away uncertain evidence early; use it only where it agrees with an existing track.
- Watch out: the method associates detection boxes, so check which detector the repo expects before planning a pipeline.
