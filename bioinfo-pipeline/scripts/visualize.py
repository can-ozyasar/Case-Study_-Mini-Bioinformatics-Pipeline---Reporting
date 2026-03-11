import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def generate_reports(input_csv, out_dir, dpi):
    """
    Metrikleri okur, istatistikleri hesaplar ve grafik oluşturur.
    """
    logging.info(f"Veri yükleniyor: {input_csv}")
    
    try:
        #Pandas ile vektörize okuma ve analiz
        df = pd.read_csv(input_csv)
        
        os.makedirs(out_dir, exist_ok=True)
        
        # İstatistiksel Log Çıktısı
        logging.info(" İSTATİSTİKSEL ÖZET ")
        metrics = ['Length', 'GC_Content_Pct', 'Mean_QScore']
        
        for metric in metrics:
            mean_val = df[metric].mean()
            median_val = df[metric].median()
            logging.info(f"{metric} -> Ortalama: {mean_val:.2f}, Medyan: {median_val:.2f}")
            
        logging.info("--------------------------")

        # Yayın Kalitesi Görselleştirme
        sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
        
        # G1 Read Length Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Length'], bins=50, kde=True, color='royalblue')
        plt.title('Read Length Distribution', weight='bold')
        plt.xlabel('Read Length (bp)')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, 'read_length_dist.png'), dpi=dpi)
        plt.close()
        logging.info("Grafik oluşturuldu: read_length_dist.png")

        # G2 GC Content Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(df['GC_Content_Pct'], bins=50, kde=True, color='forestgreen')
        plt.title('GC Content Distribution (%)', weight='bold')
        plt.xlabel('GC Content (%)')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, 'gc_content_dist.png'), dpi=dpi)
        plt.close()
        logging.info("Grafik oluşturuldu: gc_content_dist.png")

        # G3 Mean Q-Score Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Mean_QScore'], bins=50, kde=True, color='darkorange')
        plt.title('Mean Read Quality Score Distribution', weight='bold')
        plt.xlabel('Mean Q-Score (Phred)')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, 'qscore_dist.png'), dpi=dpi)
        plt.close()
        logging.info("Grafik oluşturuldu: qscore_dist.png")
        
        logging.info("Tüm görselleştirme işlemleri başarıyla tamamlandı.")

    except Exception as e:
        logging.error(f"Görselleştirme sırasında hata oluştu: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Metrik verilerinden grafikler üretir.")
    parser.add_argument("-i", "--input", required=True, help="Girdi read_metrics.csv dosyası")
    parser.add_argument("-o", "--outdir", required=True, help="Grafiklerin kaydedileceği klasör")
    parser.add_argument("--dpi", type=int, default=300, help="Grafik çözünürlüğü (DPI)")
    args = parser.parse_args()
    
    generate_reports(args.input, args.outdir, args.dpi)