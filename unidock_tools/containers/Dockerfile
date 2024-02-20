ARG BASE_IMAGE

FROM ${BASE_IMAGE}

COPY ./unidock /opt/unidock

RUN cd /opt/unidock && \
    cmake -B build && \
    cmake --build build -j`nprocs` && \
    cmake --install build && \
    rm -r /opt/unidock