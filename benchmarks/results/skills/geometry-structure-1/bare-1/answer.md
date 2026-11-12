For a commercial product, use adaptive subdivision: split the Bézier with de Casteljau until each segment is flat enough for your error tolerance, then connect the endpoints. It’s simple, handles curves well, and lets you trade speed for accuracy. For stroking or collision, choose tolerance based on the scale and consequences of error; also handle joins and endpoints separately.

For established implementations, inspect:

- **Anti-Grain Geometry (AGG)**: adaptive Bézier flattening; **AGG license**, a permissive MIT-style license suitable for commercial use.
- **Skia**: production-grade path and curve processing; **BSD-style license**, suitable for commercial use, with notices and third-party license terms to preserve.
- **Cairo**: path flattening and stroking; **LGPL/MPL dual license**. Commercial use is possible, but the applicable license’s obligations may affect how you distribute or modify it.

Check the exact license text and notices for the version you adopt, including dependencies. If you only need flattening, a small in-house de Casteljau implementation may be easier to integrate than taking on a graphics library.