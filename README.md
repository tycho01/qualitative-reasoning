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
