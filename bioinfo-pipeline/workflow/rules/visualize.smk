rule visualize_metrics:
    input:
        csv = config["out_metrics_csv"] # DAG bağlantısı: Bu dosya metrics.smk'dan gelecek
    output:
        length_plot = "results/plots/read_length_dist.png",
        gc_plot     = "results/plots/gc_content_dist.png",
        qscore_plot = "results/plots/qscore_dist.png",
        outdir      = directory("results/plots/")
    params:
        dpi = config["plots_dpi"]
    log:
        "results/logs/visualize.log"
    shell:
        """
        python scripts/visualize.py \
               --input {input.csv} \
               --outdir {output.outdir} \
               --dpi {params.dpi} \
               > {log} 2>&1
        """