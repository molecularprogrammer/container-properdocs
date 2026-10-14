FROM ubuntu:24.04

RUN apt-get update && apt-get -y install --no-install-recommends \
    python3-full \
    python3-pip \
    python3.12-venv \
    default-jre \
    graphviz \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create directory intended to be mapped to doc source volume
WORKDIR /workspace

# Allow locally serving the site
EXPOSE 8000

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
RUN pip install --no-cache-dir \
    markdown \
    properdocs \
    mkdocs-materialx \
    mkdocs-awesome-pages-plugin \
    plantuml-markdown \
    mkdocs-minify-plugin

# Get PlantUML
RUN mkdir -p /opt/plantuml \
    && wget https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar \
       -O /opt/plantuml/plantuml.jar

ENV JAVA_TOOL_OPTIONS="-Djava.awt.headless=true"

# Install custom Markdown/MkDocs extensions
COPY extensions/ /opt/extensions/

# Make custom extensions importable by Python
ENV PYTHONPATH="/opt"

CMD ["/bin/sh"]
