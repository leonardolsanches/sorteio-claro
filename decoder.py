    import base64
    import zipfile
    import io

    # String Base64 (substitua pelo seu valor)
    base64_string = "SGVsbG8sIHdvcmxkIQ=="

    # Decodificar a string Base64
    decoded_data = base64.b64decode(base64_string)

    # Criar um arquivo ZIP em memória
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        # Adicionar o arquivo decodificado ao ZIP
        zip_file.writestr("my_file.txt", decoded_data)

    # Guardar o arquivo ZIP em um arquivo
    with open("output.zip", "wb") as zip_file:
        zip_file.write(zip_buffer.getvalue())
