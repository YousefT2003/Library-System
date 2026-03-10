# controllers/barcode_controller.py
import barcode
from barcode.writer import ImageWriter

def generate_book_barcode(book_id):
    ean = barcode.get_barcode_class('ean13')
    my_barcode = ean(str(book_id), writer=ImageWriter())
    # احفظها في مجلد public مثلاً لتكون متاحة للعرض
    filename = f"public/barcodes/{book_id}"
    my_barcode.save(filename)
    return f"{filename}.png"