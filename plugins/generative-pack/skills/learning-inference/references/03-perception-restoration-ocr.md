# Perception, segmentation, tracking, restoration and OCR

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published method, not this project's code. Code license and weights license are separate; read the model card.

## Cross-cutting ideas

- **Promptable segmentation.** One model, many prompts: a click, a box or a mask in, a mask out. A heavy image encoder runs once, a light decoder runs per prompt, so interaction is instant.
- **Memory for video.** Treat video as a stream: keep a bank of features from past frames and attend to it to propagate masks or points through time.
- **Salient-object matting.** Predict a soft alpha mask for the foreground; useful for background removal and compositing.
- **Tracking any point.** Find a point's position in every later frame, handling occlusion with a visibility flag.
- **Super-resolution and restoration** train on synthetic degradation: take clean images, apply blur, noise, downscaling and compression in random order, learn to invert it. Real photos then look like the training distribution.
- **OCR is a pipeline.** Detect text regions, optionally fix orientation, recognize each region, then stitch layout.
- **Landmark models run on-device.** Small, quantized models plus a tracker that reuses the previous frame's box achieve real-time hand and face tracking.

## Segmentation and tracking

### SAM 2 — facebookresearch/sam2
**Status:** Apache-2.0, about 20k stars, pushed May 2026. Checked: README.
**Principle:** promptable segmentation for images and video, with an image treated as a one-frame video.
**Mechanism:** a hierarchical image encoder, a prompt encoder for points, boxes and masks, a mask decoder, and a **streaming memory** of past frame embeddings and predictions that the current frame attends to, which gives real-time video object tracking; the README adds `torch.compile` for the whole model and a video predictor for multiple objects.
**Use it when:** rotoscoping, click-to-cut, object tracking.

### U2-Net — xuebinqin/U-2-Net
**Status:** Apache-2.0, about 9.9k stars, pushed Jun 2024. Checked: README.
**Principle:** salient object detection with a nested U-structure: each stage of a U-Net is itself a small U-Net (a residual U-block), giving multi-scale features without a pretrained backbone.
**Mechanism (literature):** six encoder and five decoder stages emit side outputs that are fused; the output is a probability map used as an alpha matte. Powers many background-removal tools.

### TAPNet — google-deepmind/tapnet
**Status:** Apache-2.0, about 2.2k stars, pushed Sep 2026. Checked: README.
**Principle:** Tracking Any Point: given a query point in one frame, output its position and visibility in all frames.
**Mechanism (literature, TAPIR):** a global matching stage compares the query feature to every frame to find candidates; a refinement stage uses local cost volumes and an iterative network to correct the track. The repo ships datasets (TAP-Vid, TAPVid-3D), evaluation metrics, and checkpoints for TAP-Net, TAPIR, BootsTAPIR and the newer TAPNext, plus a RoboTAP benchmark.
**Use it when:** motion transfer, video editing, point-based robot learning.

### MediaPipe Hand Landmarker — google-ai-edge/mediapipe
**Status:** Apache-2.0, about 37k stars, pushed Oct 2026. Checked: README.
**Principle:** real-time on-device hand tracking: a palm detector finds the hand, a landmark model regresses 21 3D keypoints, and later frames reuse the previous landmarks to place the crop so the detector runs only when tracking is lost.
**Use it when:** gesture interfaces, interactive installations (it runs in the browser and on phones).

### Ultralytics YOLO — ultralytics/ultralytics
**Status:** **AGPL-3.0** with a paid enterprise license for commercial use (the README says so), about 62k stars, pushed Oct 2026. Checked: README.
**Principle:** single-pass object detection: a grid of predictions each output box, class and confidence; non-maximum suppression (or a learned assignment) removes duplicates. The package also covers segmentation, pose, tracking and classification behind one API.
**Use it when:** fast detection; license check first, since AGPL reaches network services.

## Restoration

### Real-ESRGAN — xinntao/Real-ESRGAN
**Status:** BSD-3-Clause, about 37k stars, pushed Aug 2024. Checked: README.
**Principle:** practical blind super-resolution trained with a high-order synthetic degradation pipeline.
**Mechanism (literature):** apply blur, resize, noise and JPEG compression repeatedly in random order (the "high-order" part, plus a sinc filter for ringing), train an RRDB generator with a U-Net discriminator and perceptual plus adversarial loss; anime-specific small models exist.
**Use it when:** upscaling photos, video frames and illustrations.

### GFPGAN — TencentARC/GFPGAN
**Status:** Apache-2.0 except listed third-party components (the LICENSE says so), about 38k stars, pushed Jul 2024. Checked: LICENSE head, README.
**Principle:** blind face restoration using a pretrained face generator as a prior: the encoder predicts latent codes and spatial feature transforms that steer the frozen generator, balancing fidelity and realism.
**Use it when:** restoring old or low-quality portraits. Faces generated by a prior can drift from the true identity; check results.

## OCR

### Tesseract — tesseract-ocr/tesseract
**Status:** Apache-2.0, about 77k stars, pushed Oct 2026. Checked: README.
**Principle:** the classic open OCR engine: page layout analysis, line finding, then an LSTM line recognizer trained per language, with dictionaries and language models to correct output.
**Use it when:** offline, CPU-only OCR with many languages. Preprocess (deskew, binarize, scale to roughly 300 DPI) for good results.

### PaddleOCR — PaddlePaddle/PaddleOCR
**Status:** Apache-2.0, about 91k stars, pushed Sep 2026. Checked: README.
**Idea:** a full document-parsing stack: detection, orientation classification, recognition, table and layout analysis, turning PDFs and images into structured data for downstream models. Heavier but stronger than Tesseract on scenes and tables.
