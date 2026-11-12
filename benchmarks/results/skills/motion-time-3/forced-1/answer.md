Use **TwistSpline** as your starting point. It targets camera or rig paths, combining a Bezier path with smoothly interpolated orientation (twist). It’s a header-only C++ library under the **MIT license**, suitable for commercial products with the license notice retained. Its reference plugin is for Maya 2022 and later, so check compatibility with your stack before adopting it.

The underlying technique is to interpolate orientation as its own channel along the path. For stable “up” direction, use a rotation-minimizing frame along the curve, then apply a separately controlled twist. This avoids the flips a Frenet frame can produce at inflection points.

Skill reference reports the project’s last push as January 2025.