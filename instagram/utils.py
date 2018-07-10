import uuid
import hashlib
import json


def safe_string(text):
    try:
        return str(text)
    except UnicodeEncodeError:
        return text.encode('ascii', 'ignore').decode('ascii')
    except BaseException:
        return ""


def generate_uuid(force=False):
    generated_uuid = str(uuid.uuid4())
    if force:
        return generated_uuid
    else:
        return generated_uuid.replace('-', '')


def generate_device_id(seed):
    volatile_seed = "12345"
    m = hashlib.md5()
    m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
    return 'android-' + m.hexdigest()[:16]


def md5_sum(text):
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()


def resp_to_json(response):
    return json.loads(response.text)


def list_to_dict(dict, list, selector):
    for item in list:
        dict[item[selector]] = item
