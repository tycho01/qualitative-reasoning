# UvA Knowledge Representation assignment: Qualitative Reasoning

### Usage
```bash
# local
pip install -r requirements.txt
python main.py

# docker
# build container
docker build -t qr .
# run tests
docker run -v $PWD:/app qr pytest -vv
# run program
docker run -v $PWD:/app qr

# or enter interactively
# bash shell
docker run -it -v $PWD:/app qr /bin/sh
# python shell
docker run -it -v $PWD:/app qr /bin/sh -c "cd /app/src; python"

# install python deps thru conda
conda install pytest
# run unit tests (also happens when building Docker image)
pytest
```

### Design

assumptions:
- continuous: will go through intermediate ordinal states

we list the assumptions on e.g. user inputs / starting states,
which in turn decide what will happen in the simulation.
