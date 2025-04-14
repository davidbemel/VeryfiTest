from pathlib import Path
from processor import VeryfiProcessor
import logging

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    processor = VeryfiProcessor()
    results = processor.process_batch(
        input_dir=Path("documentos"),
        output_dir=Path("resultados")
    )
    
    logging.info("\nResumen Final:")
    logging.info(f" Documentos procesados: {results['processed']}")
    logging.info(f" Documentos fallidos: {results['failed']}")

if __name__ == "__main__":
    main()
