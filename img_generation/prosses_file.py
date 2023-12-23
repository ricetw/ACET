import json


class ProssesFile():
    
    @staticmethod
    def save_to_cpp_file(image):
        data_list = []
        for px_val in image:
            val = hex(px_val).split("0x")[1].upper()
            if len(val) < 2:
                val = f"0{val}"
            data_list.append(f"0X{val}")
        with open("./img_generation/Corvette_F1/image.h", "w") as fp:
            fp.write(f"extern const unsigned char MY_IMAGE[];\n")
        with open("./img_generation/Corvette_F1/image.cpp", "w") as fp:
            fp.write('#include "image.h"\n\n')
            fp.write("#include <avr/pgmspace.h>\n\n")
            fp.write("const unsigned char MY_IMAGE[61440] PROGMEM = {\n")
            fp.write(",\n".join([",".join(data_list[i : i + 16]) for i in range(0, len(data_list), 16)]))
            fp.write("};\n")
    
    @staticmethod
    def save_to_json_file(image):
        data_list = []
        for px_val in image:
            val = hex(px_val).split("0x")[1].upper()
            if len(val) < 2:
                val = f"0{val}"
            data_list.append(f"0X{val}")
        with open("./img_generation/json/image.json", "w") as fp:
            fp.write('{"image_data":"')
            fp.write(",".join([",".join(data_list[i : i + 16]) for i in range(0, len(data_list), 16)]))
            fp.write('"')
            fp.write("}")
    
    # 二進制圖像資料存json
    @staticmethod
    def binary_image_to_json(byte_image):
        binary_image_data = {"byte_data": str(byte_image)}
        with open("./img_generation/json/byte_data.json", "w") as json_file:
            json.dump(binary_image_data, json_file)

    # 二進制壓縮圖像資料存json
    @staticmethod
    def compress_image_to_json(compress_data):
        compress_data = {"crypto_data": str(compress_data)}
        with open("./img_generation/json/compress_data.json", "w") as c_json_file:
            json.dump(compress_data, c_json_file)
