# UvA Knowledge Representation assignment: Qualitative Reasoning

### Usage
```bash
# local
pip install -r requirements.txt
python main.py

# docker
docker build -t qr .
docker run -v $PWD:/app qr

# or enter interactively
docker run -it -v $PWD:/app --entrypoint /bin/sh qr
```

### Design

assumptions:
- continuous: will go through intermediate ordinal states

we list the assumptions on e.g. user inputs / starting states,
which in turn decide what will happen in the simulation.
