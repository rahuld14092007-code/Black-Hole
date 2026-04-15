# Black Hole Gravitational Lensing Simulator

An advanced, pure-Python physics simulation that renders the gravitational lensing of a black hole and its accretion disk, similar to the visual effects seen in the movie *Interstellar*. 

Unlike standard 3D rendering, this project relies on **Raymarching** and **General Relativity**. It traces the paths of light rays backward from the camera to the accretion disk, accounting for the intense gravitational curvature of spacetime.

## 🚀 Features
* **Vectorized Raymarching**: Utilizes `numpy` to simultaneously calculate thousands of photon trajectories for high performance.
* **Relativistic Physics**: Uses a 4th-Order Runge-Kutta (RK4) numerical integrator to solve the equations of motion with General Relativity corrections.
* **Accretion Disk Rendering**: Simulates a glowing, temperature-mapped accretion disk with Doppler shifting approximations.
* **Procedural Output**: Generates a high-fidelity image of the warped disk using `matplotlib`.

## 🧠 The Physics (Geodesic Equations)

In Newtonian gravity, light travels in straight lines. In General Relativity, mass warps spacetime, forcing light to travel along curved paths called null geodesics. 

This simulation simplifies the full Einstein field equations for a non-rotating (Schwarzschild) black hole by applying a relativistic correction term to the standard Newtonian acceleration:

$$\vec{a} = -\frac{GM}{r^2}\hat{r} - \frac{3GM h^2}{c^2 r^4}\hat{r}$$

Where:
* $G$ is the gravitational constant.
* $M$ is the mass of the black hole.
* $c$ is the speed of light.
* $r$ is the distance from the singularity.
* $h = |\vec{r} \times \vec{v}|$ is the specific angular momentum of the photon.

The second term ($\frac{3GM h^2}{c^2 r^4}$) is the relativistic correction that allows photons to orbit the black hole (the photon sphere) or fall past the event horizon.

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/interstellar-blackhole-sim.git](https://github.com/yourusername/interstellar-blackhole-sim.git)
   cd interstellar-blackhole-sim
