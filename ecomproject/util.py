import random
import string

def genrate_random_string(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id_genrate(instance):
    new_order_id = genrate_random_string().upper()
    klass = instance.__class__
    order_id_exe = klass.objects.filter(order_id=new_order_id).exists()
    if order_id_exe:
        unique_order_id_genrate(instance)
    return new_order_id