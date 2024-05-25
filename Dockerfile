# Layer with Python and some shared environment variables
FROM python:3.10-slim-bullseye as python

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Layer for installing Python dependencies
FROM python as dependencies

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV VIRTUAL_ENV=/opt/venv

# Add some libraries sometimes needed for building Python dependencies, e.g. gcc
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update --fix-missing && \
    apt-get install --no-install-recommends -y \
    build-essential

# Copy our Python requirements here
COPY ./pyproject.toml .

# Install uv and Python dependencies
# Note: Turn off pip progress bar because it seemed to cause some issues on deployment
# Note: Using a virtualenv seems unnecessary, but it reduces the size of the resulting Docker image
RUN --mount=type=cache,target=/root/.cache/pip --mount=type=cache,target=/root/.cache/uv \
    python -m pip config --user set global.progress_bar off && \
    python -m pip install --upgrade pip uv && \
    uv venv /opt/venv && \
    uv pip install --requirement pyproject.toml


# Layer with only the Python dependencies needed for serving the app in production
FROM python as production

# Copy over just the code
COPY /site /site

# Copy over the virtualenv and add it to the path
COPY --from=dependencies /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /site

EXPOSE 80

# Collect static assets
RUN python app.py collectstatic -v 2 --noinput

# Run gunicorn
CMD ["gunicorn", "app:wsgi", "--config=gunicorn.conf.py"]
