rule run_nanoplot:
    input:
        fastq = config["input_fastq"]
    output:
        report = "results/qc/NanoPlot-report.html",
        outdir = directory("results/qc/")
    threads:
        config["threads"]
    log:
        "results/logs/nanoplot.log"
    shell:
        """
        NanoPlot --fastq {input.fastq} \
                 --outdir {output.outdir} \
                 --threads {threads} \
                 --plots dot \
                 > {log} 2>&1
        """