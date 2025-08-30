# Hop Along Visualiser

![Example gif](img/example.gif)

Fun visualiser using Barry Martin Hop Along fractals (using [this document](https://www.jolinton.co.uk/Mathematics/Hopalong_Fractals/Text.pdf) as a reference).
Iterations calculated with `numba`, and rendered using `matplotlib`.

## Setup

Install requirements and run main script.

```sh
python -m pip install -r requirements.txt
python main.py
```

## Options

```sh
python main.py --help
```

### Control the number of iteration per frame

```sh
python main.py --niters 1000
```

### Control the number of frames before rendered iterations disappear

```sh
python main.py --nhist 10
```

If this value is set to 0, the frame is completely cleared with each update.

### Control the number of frames before hop along parameters are reset

```sh
python main.py --nreset 10
```

If this value is set to 0, the parameters are never reset.
Low values (e.g., 1) create very chaotic (but fun) visuals as multiple structures are layered.
Larger values create more stable strutures, but too large and the visual can feel less dynamic.

### Control target framerate

```sh
python main --fps 25
```

Defaults to 25 fps for cinematic experience although my PC can only handle about 11 fps.

## Example Images

![Example1](img/example1.png)
![Example2](img/example2.png)
![Example3](img/example3.png)
![Example4](img/example4.png)
![Example5](img/example5.png)
![Example6](img/example6.png)
![Example7](img/example7.png)
![Example8](img/example8.png)
![Example9](img/example9.png)
