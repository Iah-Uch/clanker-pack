For teaching and quick visual prototypes, start with p5.js: it’s approachable, browser-based, and has a large community and many examples. Its library is LGPL-2.1, so review the license obligations before bundling or modifying it in a commercial product.

For node-based visual creation, consider Blockly (Apache-2.0) or Google's visual programming tools; they suit teaching, though you may need to build your own examples and product experience.

For interactive graphics and 3D, look at Three.js (MIT) and PixiJS (MIT). Both are commercially usable, with attribution and license-notice requirements.

For a broad ecosystem of ready-made visual examples, also evaluate Processing (LGPL-2.1) and openFrameworks (MIT), though they’re more oriented toward coding and desktop installations than browser-first products.

My default: prototype with p5.js, use Three.js or PixiJS for production graphics, and choose Blockly if the product teaches programming through visual blocks. Check each project’s current license and the licenses of plugins, assets, fonts, and example code before shipping; this is general information, not legal advice.