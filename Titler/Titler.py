def titler(title, length=40):
    end = ""
    dashes = length - len(title)
    dashes = int(dashes / 2)
    if len(title) % 2 == 1:
        end = "="
    dashes2 = "=" * dashes
    return f"{dashes2}< {title} >{dashes2}{end}"
