import itertools
import random
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_full_domains(valid_domains, times,prefixLen=3):
    domains = []
    domain_iterator = itertools.cycle(valid_domains)
    
    for _ in range(times):
        domain = next(domain_iterator)
        random_chars = generate_random_string(prefixLen)
        full_domain = f"{random_chars}.{domain}"
        domains.append(full_domain)
    
    return domains

def get_domains(valid_domains, times):
    domains = []
    domain_iterator = itertools.cycle(valid_domains)
    
    for _ in range(times):
        domain = next(domain_iterator)
        # random_chars = generate_random_string(prefixLen)
        # full_domain = f"{random_chars}.{domain}"
        domains.append(domain)
    
    return domains
    