# FRONT DOCKERFILE

FROM continuumio/miniconda3

WORKDIR /app



RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libfontconfig1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN conda install --yes --freeze-installed -c conda-forge \
    pandas \
    matplotlib \
    && conda clean --all -f -y \
    && pip install streamlit openpyxl

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501"]
