FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - && \
    mkdir -p /etc/poetry/bin && \
    ln -s /etc/poetry/bin/poetry /usr/local/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

#RUN bash -c "timedatectl set-timezone America/Lima"
#RUN bash -c "timedatectl set-ntp on" 

COPY ./app /app
ENV PYTHONPATH=/app
