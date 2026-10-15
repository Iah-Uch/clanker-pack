# Learning foundations, embeddings, self-play, robotics and decision engines

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published method, not this project's code.

## Cross-cutting ideas

- **Gradient descent on a differentiable program.** Anything built from differentiable operations can be trained: language models, cellular automata, signal-processing chains.
- **Self-organization by learned local rules.** A tiny shared update rule applied everywhere can be trained so the global pattern grows, repairs and persists.
- **Dimensionality reduction for visualization.** Embed high-dimensional data in 2D so neighbors stay neighbors.
- **Self-play and search.** An agent improves by playing itself, with a search procedure that turns a network's guesses into stronger moves, and the improved moves become new training targets.
- **Policy learning in simulation, then transfer.** Train a policy with reinforcement learning in thousands of parallel simulated robots, check it in a second simulator (sim2sim), then deploy on hardware (sim2real).
- **Typed decisions instead of free text.** When an application needs a choice (which tool, which value), a classifier over fixed options is faster, cheaper and cannot invent text.

## Entries

### nanoGPT — karpathy/nanoGPT
**Status:** MIT, about 64k stars, pushed Nov 2025. Checked: metadata and license.
**Principle:** the smallest readable GPT training loop.
**Mechanism (literature):** token and position embeddings feed N blocks of pre-norm causal self-attention, softmax(Q·K^T / sqrt(d) + causal mask)·V, and an MLP, each with residual connections; the loss is next-token cross-entropy; AdamW with warmup and cosine decay.
**Use it when:** learning how language models work, small experiments, baselines.

### UMAP — lmcinnes/umap
**Status:** BSD-3-Clause, about 8.3k stars, pushed Oct 2026. Checked: README, license.
**Principle:** build a weighted k-nearest-neighbor graph of the data (a fuzzy simplicial set), then lay out a low-dimensional graph with the same structure.
**Mechanism (literature):** edge weight w_ij = exp(−(d_ij − rho_i) / sigma_i), with rho_i the distance to the nearest neighbor (guaranteeing local connectivity) and sigma_i chosen so the weights sum to log2(k); the layout minimizes a cross-entropy between high- and low-dimensional edge weights by stochastic gradient descent with attractive forces along edges and repulsion from negative samples.
**Use it when:** visualizing embeddings, clusters, and any feature set; also usable as preprocessing for clustering.
**Pitfalls:** global distances in the plot are not meaningful; neighbors are.

### Growing Neural Cellular Automata — google-research/self-organising-systems
**Status:** Apache-2.0, about 450 stars, pushed Jan 2026. Checked: README (it points to the Distill article, with notebooks in the repo).
**Principle:** train a cellular automaton's local update rule so a seed cell grows into a target image, regenerates when damaged, and stays stable.
**Mechanism (literature):** each cell holds a state vector (16 channels, RGBA plus hidden); every step it perceives its neighbors through fixed Sobel filters and the identity, concatenates them, passes them through a small per-cell MLP, and adds the result as an update applied with a random per-cell mask (stochastic, asynchronous); training backpropagates a pixel loss through 64 to 96 steps, keeps a pool of previous states to teach persistence, and samples damage to teach regeneration.
**Use it when:** self-repairing textures, morphogenesis, tiny neural models that run in a shader.

### TensorFlow Playground — tensorflow/playground
**Status:** Apache-2.0, about 13k stars, pushed Jun 2026. Checked: README.
**Idea:** an in-browser neural network teaching tool: change layers, activations, regularization and data, watch the decision boundary and loss update live. A model for interactive explanation: every hyperparameter is a visible control with instant feedback.

### KataGo — lightvector/KataGo
**Status:** a custom license file; its head lists third-party libraries with their own licenses (GitHub shows no classification), about 5.2k stars, pushed Sep 2026. Checked: LICENSE head. Read the whole file before reuse.
**Principle:** AlphaZero-style self-play for Go with extra targets and efficiency tricks.
**Mechanism (literature):** a residual convolutional network outputs a policy over moves and a value; Monte Carlo tree search selects moves by maximizing Q(s,a) + c·P(s,a)·sqrt(N(s)) / (1 + N(s,a)); search visit counts become the policy training target, game outcomes the value target; KataGo adds auxiliary targets (score, ownership) and playout-cap randomization to learn faster.
**Use it when:** game AI, learning how search and learning combine; the engine speaks the GTP protocol.

### LeRobot — huggingface/lerobot
**Status:** Apache-2.0, about 28k stars, pushed Oct 2026. Checked: README.
**Idea:** open robot learning end to end: a dataset format for robot episodes (video plus state and action), pretrained policies (imitation learning, diffusion policies, vision-language-action), hardware drivers for low-cost arms, and simulation environments.
**Mechanism (literature):** imitation learning regresses actions from observations on teleoperated demonstrations; a diffusion policy denoises a short action sequence conditioned on the observation, which handles multimodal behavior.
**Use it when:** teaching a robot arm tasks from demonstrations.

### Unitree RL Gym — unitreerobotics/unitree_rl_gym
**Status:** BSD-3-Clause, about 3.6k stars, pushed Jul 2025. Checked: README.
**Principle:** reinforcement learning for legged robots in massively parallel simulation.
**Mechanism:** the README gives the workflow: **train** (agents act in the simulator to maximize a designed reward), **play** (check the policy), **sim2sim** (run it in another simulator so it does not overfit one simulator's quirks), **sim2real** (deploy). Rewards combine terms such as velocity tracking, energy, joint limits and smooth actions.
**Use it when:** locomotion policies for Unitree robots; template for reward design.

### Laya — NandhaKishorM/laya
**Status:** Apache-2.0, about 33k stars, pushed Oct 2026. Checked: README.
**Principle (as described by the README):** a multilingual, non-autoregressive decision engine: typed decisions (a choice from supplied options) in a single forward pass of about 33 ms, trained with reinforcement learning against strictly proper scoring rules, with a router that selects a checkpoint per request. Integrations for LangChain, LlamaIndex and CrewAI, an MCP server and an HTTP server are optional extras.
**Use it when:** routing, classification and tool selection where a generated answer is unnecessary. I did not verify the benchmark claims.

### Jev Chat — w3cj/jev-chat
**Status:** MIT, 115 stars, pushed Sep 2026. Checked: README.
**Principle:** a chat interface that calls tools without a language model writing text.
**Mechanism (from the README):** each turn a classifier answers named questions (what was asked, which tool, which value for each argument, whether to confirm, what reply to give); code then calls the MCP servers and builds the reply from the tools' own data, so every shown value was typed by the user or returned by a tool; an inspector shows each question and probability.
**Use it when:** an assistant that must not invent facts; auditable decision logs.
