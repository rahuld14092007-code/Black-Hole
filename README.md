# 🌌 Gargantua Engine v6: Cinematic Relativity Simulator

A high-performance, real-time black hole flight simulator built with **Python**, **ModernGL**, and **GLSL**. This project uses raymarching and general relativity approximations to render a physically-inspired visualization of a supermassive black hole.

---

## 📖 Project Description

The **Gargantua Engine** allows users to pilot a virtual observer through the warped spacetime of a singularity. Unlike static visualizations, this engine renders gravitational lensing, the Doppler effect, and volumetric gas particles in real-time at 60+ FPS.

### Key Features:
* **Volumetric Gas Particles:** Real-time swirling plasma disk using Flow-Field Advection.
* **Gravitational Lensing:** Light rays bend around the event horizon, creating the iconic Einstein Ring.
* **First-Person Flight:** Full 6-Degrees-of-Freedom (6-DOF) movement.
* **Relativistic Beaming:** Accurate brightness shifts based on gas velocity relative to the camera.
* **Dynamic Background:** A high-contrast starfield that warps and stretches under intense gravity.

---

## 🕹️ Controls & Navigation

The simulator uses a standard FPS (First-Person) control scheme. **The mouse is automatically captured** for a full 360-degree immersive experience.

### 🚀 Movement
* **W / S** : Forward / Backward
* **A / D** : Strafe Left / Right
* **Q / E** : Descend / Ascend (Vertical Movement)

### 🔭 View & Zoom
* **Mouse Move** : Look around (Pitch and Yaw)
* **Scroll Wheel** : Zoom In / Out (Telescopic FOV adjustment)

### 🔬 Physics & System
* **[ 1 ]** : Gargantua Mode (Realistic Orange Disk)
* **[ 2 ]** : Blue Quasar Mode (High-Energy Blue/Violet)
* **[ 3 ]** : The Void (Singularity & Stars only)
* **[ R ]** : **Emergency Reset** (Teleports camera back to safe start position)
* **[ ESC ]** : Exit and release mouse

---

## 🛠️ Installation & Setup

1. **Install Python 3.8+**
2. **Install Dependencies:**
   ```bash
   pip install moderngl moderngl-window numpy
