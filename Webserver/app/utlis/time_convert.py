from datetime import datetime

def string_to_int(_time:str, format:str='%Y-%m-%d %H:%M', _add:str='')->str :
    res = datetime.strptime(_time, f'{format}').timestamp()
    return f'{int(res)}{_add}'

def epoch_to_datetime(epochTime, format='%Y-%m-%d %H:%M:%S')-> str:
    return datetime.fromtimestamp(epochTime).strftime(format)