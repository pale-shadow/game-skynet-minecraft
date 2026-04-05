# 🧠 Skynet Architect: Neural Core Models

This directory contains the inference assets for the **Skynet v7.1-RECLAMATION** ecosystem. It implements a **Dual-Inference** strategy, utilizing both the Raspberry Pi 5's Hailo-8L NPU and an external USB Edge TPU.

## 📡 Spatial Inference (Hailo-8L NPU)
*   **Model:** `yolov8s_h8l.hef`
*   **Role:** Drives the **Spatial Density Mapping** and cluster inference for optimal build site selection.
*   **Hardware:** Integrated via the Pi 5 PCIe bus.
*   **Deployment:** Linked from `/usr/share/hailo-models/yolov8s_h8l.hef`.

## 👁️ Visual Cortex (Edge TPU)
*   **Model:** `vision_v1.tflite`
*   **Role:** Performs real-time **Aesthetic Validation** on generated schematics.
*   **Classification:** Ensures "Black Ice" style compliance (Block-ratios of Tuff, Obsidian, and Froglights).
*   **Hardware:** USB Edge TPU Accelerator.

## 🛠️ Maintenance & Verification
To verify the status of the Neural Core, run the health check script:

```bash
python3 models/verify_models.py
```

## 🔄 Hybrid Workflow
While core logic is currently simulated in `src/vision_lite_overseer.py` and `src/npu_spatial_engine.py` for stability, these models serve as the production-ready inference targets for the 2026 **Void-Tech** era.
