

```markdown
# Long-Read Sequencing QC Pipeline

This repository contains a reproducible Quality Control (QC) and metric extraction pipeline for long-read sequencing data. It takes raw `.fastq.gz` files, evaluates read quality, extracts key metrics (Length, GC Content, Mean Q-Score), and generates publication-ready distribution plots.

## Engineering & Architecture Decisions

This pipeline was built with production-grade standards rather than basic sequential scripting:

* **O(1) Memory Complexity:** The core extraction script (`scripts/extract_metrics.py`) uses streaming I/O. It reads and writes read-by-read, meaning it can process massive FASTQ files (100GB+) without causing RAM bottlenecks.
* **Config-Driven:** Zero hardcoded paths. All inputs, outputs, threads, and parameters are centrally managed via `config/config.yaml`.
* **Deterministic Environment:** The infrastructure relies on a strictly version-pinned `Dockerfile` and `requirements.txt`. This guarantees exact reproducibility across different machines and operating systems.
* **DAG Orchestration:** Snakemake is used to define the workflow as a Directed Acyclic Graph (DAG), ensuring proper dependency tracking, error handling, and parallel execution.

## Directory Structure

```text
.
├── config/             # Pipeline configuration (yaml)
├── data/raw/           # Input directory for fastq.gz files (ignored by git)
├── env/                # Dockerfile and exact requirements
├── results/            # Auto-generated outputs (logs, plots, metrics, qc)
├── scripts/            # Python scripts for extraction and visualization
├── workflow/           # Snakemake rules
├── EMAIL_DRAFT.md      # Executive summary draft for stakeholders
└── README.md

```

## Setup & Execution

**1. Clone the repository and add data:**

```bash
git clone [https://github.com/YOUR_USERNAME/bioinfo-pipeline.git](https://github.com/YOUR_USERNAME/bioinfo-pipeline.git)
cd bioinfo-pipeline

# Place your raw sequencing data here:
# cp path/to/barcode77.fastq.gz data/raw/

```

**2. Build the Docker image:**

```bash
docker build -t bioinfo-runner -f env/Dockerfile .

```

**3. Run the pipeline:**
*For Linux/Mac:*

```bash
docker run --rm -v "$(pwd):/app" bioinfo-runner snakemake --cores 4

```

*For Windows (PowerShell):*

```bash
docker run --rm -v "${PWD}:/app" bioinfo-runner snakemake --cores 4

```

## Outputs

Once the pipeline finishes (`100% done`), check the `results/` directory:

* `results/qc/`: NanoPlot HTML reports.
* `results/metrics/read_metrics.csv`: Raw data extracted per read.
* `results/plots/`: Standardized PNG plots for GC distribution, Read Lengths, and Q-Scores.
* `results/logs/`: Step-by-step execution logs for debugging.

## Stakeholder Communication

Refer to `EMAIL_DRAFT.md` for the non-technical summary and next-step recommendations regarding the sequencing run.

```

***

### CTO Son Kontrolü: .gitignore Unutulmasın!
Bu kodu GitHub'a gönderirken `data/raw/` klasöründeki o devasa `.fastq.gz` dosyasını yanlışlıkla pushlamamak hayati önem taşır. Proje ana dizininde `.gitignore` adında bir dosya oluştur ve içine sadece şunları yaz:

📁 Dosya Yolu: `.gitignore`
```text
data/raw/*
!data/raw/.gitkeep
results/*
!results/.gitkeep
__pycache__/
.snakemake/

```

