docker build -t double-slit-sim .
docker run --gpus all -it --rm -v "/c/syntax-free-research/BRCC/OriginalResearch/proj:/workspace" double-slit-sim
