def convert_bytes(size, unit):
    if unit == 'KB':
        return round(size / 1024)
    elif unit == 'MB':
        return round(size / (1024 ** 2))
    elif unit == 'GB':
        return round((size / (1024 ** 3)))
    else:
        return size
