# kv_exporter.py

def export_to_kv(widgets, filepath="kivy.kv"):
    """
    Exporta uma lista de widgets Kivy para um ficheiro .kv.

    Args:
        widgets (list): Lista de widgets para exportar.
        filepath (str): Caminho do ficheiro onde salvar o conteúdo .kv.

    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("<FloatLayout>:\n")

        for widget in widgets:
            cls_name = widget.__class__.__name__
            text = getattr(widget, 'text', '')
            custom_id = getattr(widget, 'id', '')
            color = getattr(widget, 'color', None)
            bgcolor = getattr(widget, 'background_color', None)
            pos = (int(widget.x), int(widget.y))
            size = (int(widget.width), int(widget.height))

            f.write(f"    {cls_name}:\n")

            # ID
            if custom_id:
                f.write(f"        id: {custom_id}\n")

            # Text (com aspas simples escapadas)
            if text:
                safe_text = text.replace("'", "\\'")
                f.write(f"        text: '{safe_text}'\n")

            # Tamanho e posição fixos
            f.write(f"        size_hint: None, None\n")
            f.write(f"        size: {size[0]}, {size[1]}\n")
            f.write(f"        pos: {pos[0]}, {pos[1]}\n")

            # Cor do texto (se aplicável)
            if color:
                rgba_str = ', '.join(f"{c:.3f}" for c in color)
                f.write(f"        color: {rgba_str}\n")

            # Cor de fundo (se aplicável)
            if bgcolor:
                rgba_str = ', '.join(f"{c:.3f}" for c in bgcolor)
                f.write(f"        background_color: {rgba_str}\n")

            f.write("\n")
