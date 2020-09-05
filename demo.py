import pandas as pd

from main import domain_expiration

if __name__ == '__main__':
    df = pd.read_csv('domains.csv')
    for domain in df['domain']:
        domain_expiration(domain)
