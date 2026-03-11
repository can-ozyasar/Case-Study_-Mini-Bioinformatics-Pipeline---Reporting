
rule extract_metrics:
    input:
        fastq = config["input_fastq"]
    output:
        csv = config["out_metrics_csv"]
    log:
        "results/logs/extract_metrics.log"
    shell:
        """
        python scripts/extract_metrics.py \
               --input {input.fastq} \
               --output {output.csv} \
               > {log} 2>&1
        """