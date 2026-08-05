# D71 Taygeta local avatar-video model research

## Objective

Produce a compact research memo identifying the best local video-generation route for this exact task:

- Input: an artistic portrait still plus spoken audio.
- Output: portrait-faithful artistic talking-avatar video with convincing lips, restrained natural motion, stable identity and stable image style.
- Hardware: NVIDIA GeForce RTX 5060 Ti, 16 GB VRAM, 180 W, Linux.
- Throughput requirement: a 20-minute finished video within one week on one GPU. Practical target is roughly 5–10 seconds rendered per hour, allowing some retries.
- Current system: official Wan 2.2 S2V 14B in ComfyUI, FP8, 832x480, 20 steps, 16 fps, typically 8–10 seconds per 40–63 minutes. Quality is unacceptable: identity/style degradation, jumpy or over-expressive motion, seams/exposure drift in multi-window mode, and occasional late failures. Wan 2.2 is known to be capable of better quality in other configurations.

## Research questions

1. Separate likely model limitations from configuration or implementation mistakes in the current Wan 2.2 S2V graph.
2. Compare the strongest currently available open/local audio-driven portrait or avatar models that could plausibly fit or be offloaded on 16 GB VRAM. Include at least Wan 2.2 S2V, InfiniteTalk, HunyuanVideo-Avatar, FantasyTalking, EchoMimic V2, Hallo/Hallo2, SkyReels or other truly relevant current options.
3. Include speed-oriented runtimes and accelerators where relevant: native PyTorch/ComfyUI, Wan2GP, TeaCache, SageAttention, quantization, step-distilled or LoRA accelerators, and frame interpolation/upscaling. Distinguish quality-preserving optimization from quality-sacrificing optimization.
4. Recommend a ranked shortlist and a small controlled test matrix, not a full deployment.
5. Flag licensing, Blackwell/RTX 5060 Ti compatibility, VRAM, supported resolutions/durations, and whether portrait fidelity is actually a design goal.

## Output

Write `result.md` with:

- a concise diagnosis;
- a ranked comparison table;
- exact reasons for the top recommendation;
- a 3–6 test pilot that can decide the issue quickly;
- uncertainties and claims needing verification.

Do not include credentials or private participant data. Do not propose paid cloud APIs as the primary answer.
