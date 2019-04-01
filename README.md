# UvA Knowledge Representation assignment: Qualitative Reasoning

### Usage
```bash
# local
pip install -r requirements.txt
python container.py

# docker
docker build -t qr .
docker run -v $PWD:/app qr

# or enter interactively
docker run -it -v $PWD:/app --entrypoint /bin/sh qr
```

### Design

assumptions:
- continuous: will go through intermediate ordinal states

- How will the exogenously defined inflow behave? Choose assumptions at your discretion.

state-graph with https://en.wikipedia.org/wiki/DOT_(graph_description_language)

trace:
- intra-state
- inter-state

we list the assumptions on e.g. user inputs / starting states,
which in turn decide what will happen in the simulation.
