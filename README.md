# Python 3D Renderer

A simple 3D rendering engine built with Python, ModernGL, and GLFW. This project demonstrates loading a 3D model (`.obj` format) and rendering it with a dynamic Blinn-Phong lighting model. It features a first-person fly-through camera for scene navigation.



## Features

-   **ModernGL Rendering:** Utilizes ModernGL for efficient, modern OpenGL rendering.
-   **First-Person Camera:** Navigate the scene with classic WASD, space/shift, and mouse controls.
-   **Blinn-Phong Lighting:** Dynamic lighting that responds to camera and light source positions.
-   **OBJ Model Loading:** Loads vertex data from `.obj` files using `pywavefront`.


## Prerequisites

-   Python 3.7+
-   Pip (Python package installer)

## Installation

1.  Clone the repository:
    ```sh
    git clone https://github.com/ianmhoffman606/pyrender.git
    cd graphrender
    ```

2.  Install the required packages from `requirements.txt`:
    ```sh
    pip install -r requirements.txt
    ```

## How to Run

Once the dependencies are installed, run the main script from the root directory of the project:

```sh
python main.py
```

## Controls

-   **W, A, S, D:** Move the camera forward, left, backward, and right.
-   **Space:** Move up.
-   **Left Shift:** Move down.
-   **Mouse:** Look around.
-   **Escape:** Close the application.

## Project Structure

```
pyrender/
├── main.py             # Main application entry point and render loop
├── camera.py           # Implements the first-person camera
├── object.py           # Handles loading and processing of 3D models
├── mathlib.py          # Custom math classes (Vector3, Matrix44)
├── program.py          # Manages GLSL shader programs and uniforms
├── requirements.txt    # Project dependencies
├── models/
│   └── teapot.obj      # 3D model file
└── shaders/
    ├── default.vert    # Vertex shader for Blinn-Phong lighting
    └── default.frag    # Fragment shader for Blinn-Phong lighting
```

## Future Work

Here are some planned improvements:

-   [ ] Write a custom `.obj` parser to remove the `pywavefront` dependency.
-   [ ] Implement post-processing effects using framebuffers.

## Built With

-   ModernGL - Modern OpenGL bindings for Python
-   glfw - Windowing and event handling
-   NumPy - Vector and matrix operations
-   PyWavefront - `.obj` file loading