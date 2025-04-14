import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from veryfi import Client
from pydantic import BaseModel

# Configuracion basica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
 # Modelo para items de linea en facturas
class LineItem(BaseModel):
    sku: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    total: Optional[float] = None
    tax_rate: Optional[float] = None

# Modelo principal para datos de factura
class InvoiceData(BaseModel):
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    line_items: List[LineItem] = []

# Clase principal que encapsula el procesamiento.
class VeryfiProcessor:
    def __init__(self):
        """Inicializa con credenciales directas sin seguridad de entorno (version API actual)"""
        self.client = Client(
            client_id="vrf4KgU5JZXnSsMCm3nyKneiTPV3v61Vfx4G3sF",
            client_secret="HRmzRHjcPlRmjir62e1zg0aCSo4wPy3E57TFJvoiI68R9UVg0WFLEmKWVf23Dc8iLA2jS87XmH1BOTgVton8SH2Z0E48Pjls5bVHazYK7xHfzC0i1VVS1ob70mntur0m",
            username="david.3pl",
            api_key="8a1147415158b3b4bd039857e1fdcb11"
        )
    # Procesa un documento de factura individual utilizando la API de Veryfi y devuelve los datos estructurados.
    def process_document(self, file_path: Path) -> Tuple[Optional[InvoiceData], Optional[Dict]]:
        """Version actualizada compatible con la API v7+ de Veryfi"""
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

            # Metodo actualizado para la ultima version de Veryfi
            with open(file_path, 'rb') as f:
                response = self.client.process_document(
                    file_path=str(file_path.absolute()),  
                    categories=["Invoice"],
                    delete_after_processing=False
                )

            # Procesamiento de la respuesta
            # Mapeo de la respuesta de modelos Pydantic

            invoice_data = InvoiceData(
                vendor_name=response.get('vendor', {}).get('name'),
                vendor_address=response.get('vendor', {}).get('address'),
                invoice_number=response.get('invoice_number'),
                date=response.get('date'),
                line_items=[
                    LineItem(
                        sku=item.get('sku'),
                        description=item.get('description'),
                        quantity=item.get('quantity'),
                        price=item.get('price'),
                        total=item.get('total'),
                        tax_rate=item.get('tax_rate')
                    ) for item in response.get('line_items', [])
                ]
            )
            return invoice_data, response

        except Exception as e:
            logging.error(f"Error procesando {file_path.name}: {str(e)}")
            return None, None

    def process_batch(self, input_dir: Path, output_dir: Path) -> Dict[str, int]:
        """Procesamiento por lotes simplificado"""
        results = {'processed': 0, 'failed': 0}
        output_dir.mkdir(exist_ok=True)

        for pdf_file in input_dir.glob("*.pdf"):
            data, _ = self.process_document(pdf_file)
            if data:
                output_file = output_dir / f"{pdf_file.stem}.json"
                with open(output_file, 'w') as f:
                    json.dump(data.dict(), f, indent=2)
                results['processed'] += 1
                logging.info(f"Procesado: {pdf_file.name}")
            else:
                results['failed'] += 1
                logging.error(f"Falló: {pdf_file.name}")

        return results
