FROM python:3.7

RUN pip install numpy
RUN pip3 install torch==1.9.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install transformers
RUN pip install scikit-learn

RUN pip install -U "celery[redis]"
RUN pip install Flask

COPY models/bert-tokenizer.bin bert-tokenizer.bin
COPY models/bert-model.bin bert-model.bin
COPY models/LDA.bin LDA.bin
COPY models/LDA_vec.bin LDA_vec.bin

COPY server.py server.py
COPY models.py models.py

COPY start.sh start.sh

ENTRYPOINT ["/bin/bash","start.sh"]
