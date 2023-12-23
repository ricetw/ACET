from .epaper import GenerateEPaperImage
from .prosses_file import ProssesFile
from .mqtt_pub import ProssesMqtt

EPaperW, EPaperH = 640, 384

epaper_payload = {
    "number": "P-73158946",
    "id": "4",
    "name": "SHIH-MIN-CHI",
    "case": "Fracture",
    "medication": "Sumatriptan",
    "notice": "None",
    "location": "2F-01",
    "bed number": "1",
}
AES_QR_payload = {
    "number": "P-73158946",
    "id": "4"
}

def update(img_date, QR_code_data):
    epaper_payload.update(img_date)
    AES_QR_payload.update(QR_code_data)
    GenerateEPaperImage(EPaperW, EPaperH).gen_image(epaper_payload)
    QR_image = GenerateEPaperImage(EPaperW, EPaperH).add_qrcode(AES_QR_payload)
    
    ProssesFile.save_to_cpp_file(QR_image.byte_data)
    ProssesFile.save_to_json_file(QR_image.compress_data)
    ProssesFile.binary_image_to_json(QR_image.byte_data)
    ProssesFile.compress_image_to_json(QR_image.compress_data)
    ProssesMqtt.pub2mqtt(epaper_payload["number"], epaper_payload)
