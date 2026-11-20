FROM mambaorg/micromamba:2.4.0-debian12
ARG MAMBA_DOCKERFILE_ACTIVATE=1
COPY --chown=mambauser:mambauser environment.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml && micromamba clean --all --yes
WORKDIR /workspace
COPY --chown=mambauser:mambauser . /workspace
RUN python -m pip install --no-deps -e .
ENV MPLBACKEND=Agg
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "neutrontoolkit", "doctor"]
