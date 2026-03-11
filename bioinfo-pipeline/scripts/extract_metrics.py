import gzip
import csv
import logging
import argparse
import numpy as np
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

# Loglama Konfigürasyonu (Kural 5)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def extract_metrics(input_fastq, output_csv):
    """
    FASTQ dosyasını streaming yöntemiyle okur ve metrikleri CSV'ye yazar.
    Bellek karmaşıklığı: O(1) - Dosya boyutu ne olursa olsun RAM kullanımı sabittir.
    """
    logging.info(f"İşlem başlatıldı. Girdi dosyası: {input_fastq}")
    
    try:
        # Kural 2: Streaming okuma ve anında yazma (Memory Efficient)
        with gzip.open(input_fastq, "rt") as handle, open(output_csv, "w", newline='') as out_file:
            writer = csv.writer(out_file)
            # CSV Başlıkları
            writer.writerow(["Read_ID", "Length", "GC_Content_Pct", "Mean_QScore"])
            
            read_count = 0
            for record in SeqIO.parse(handle, "fastq"):
                # Metrik hesaplamaları (Kural 6: Vektörize/Optimizeli hesaplama)
                read_id = record.id
                length = len(record)
                gc_content = gc_fraction(record.seq) * 100
                mean_qscore = np.mean(record.letter_annotations["phred_quality"])
                
                # Anında dosyaya yazarak RAM'i boşalt
                writer.writerow([read_id, length, f"{gc_content:.2f}", f"{mean_qscore:.2f}"])
                read_count += 1
                
                if read_count % 10000 == 0:
                    logging.info(f"{read_count} okuma işlendi...")
                    
        logging.info(f"İşlem tamamlandı. Toplam {read_count} okuma işlendi. Çıktı: {output_csv}")
        
    except Exception as e:
        logging.error(f"Veri işleme sırasında kritik bir hata oluştu: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FASTQ kalite metriklerini çıkarır.")
    parser.add_argument("-i", "--input", required=True, help="Girdi .fastq.gz dosyası")
    parser.add_argument("-o", "--output", required=True, help="Çıktı .csv dosyası")
    args = parser.parse_args()
    
    extract_metrics(args.input, args.output)