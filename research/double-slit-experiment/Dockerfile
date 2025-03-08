FROM nvcr.io/nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --upgrade pip

# Install compatible CuPy version for CUDA 11.8 and matplotlib
RUN pip3 install "cupy-cuda11x>=12.0.0" matplotlib

# Set working directory
WORKDIR /workspace

CMD ["/bin/bash"]