FROM localhost/solar-protocol/base:beta AS builder
RUN apt-get --quiet update && apt-get --quiet upgrade --yes

RUN apt-get --quiet install build-essential \
  libffi-dev libjpeg-dev zlib1g-dev --yes

WORKDIR /protocol
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --quiet --no-cache-dir --requirement requirements.txt
RUN pip install --quiet --no-cache-dir /common

FROM localhost/solar-protocol/base:beta
RUN apt-get --quiet update && apt-get --quiet install libcairo2 zlib1g --yes
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /protocol
COPY . .

CMD python run.py
