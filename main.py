import re
import shutil
import subprocess as sp
import sys

from dateutil.parser import parse


def domain_expiration(domain: str) -> None:
    if whois_cmd_exists():
        run_whois_cmd(domain)


def whois_cmd_exists() -> bool:
    whois_path = shutil.which('whois')
    if not whois_path:
        msg = ["\nError: whois command not found.",
               "Please make sure a whois client is installed and in your path."]
        if sys.platform.startswith('linux'):
            msg.extend([
                'The whois command can be installed via apt with:',
                'sudo apt install whois\n'
            ])
        elif sys.platform == 'win32':
            msg.extend([
              'You can download whois from the Windows Sysinternals suite at:',
              'https://docs.microsoft.com/en-us/sysinternals/downloads/whois\n'
            ])
        print(*msg, sep='\n\n')
        return False
    return True


def run_whois_cmd(domain: str, timeout=5) -> None:
    cmd = ['whois', domain]
    proc: sp.CompletedProcess
    proc = sp.run(cmd, capture_output=True, timeout=timeout)
    try:
        proc.check_returncode()
        parse_output(domain, proc.stdout)
    except sp.TimeoutExpired:
        print(f'WHOIS request for {domain} timed out after {timeout} seconds.')
    except sp.CalledProcessError as e:
        # Sometimes CalledProcessError: Connection reset by peer is thrown,
        # even when the request succeeds.
        if 'Connection reset by peer' in str(e.stderr, 'utf-8'):
            parse_output(domain, proc.stdout)
        else:
            print('Error:', e)


def parse_output(domain: str, data: bytes) -> None:
    lines = str(data, 'utf-8').splitlines()
    pattern = r"^.*expir.*:"
    for line in lines:
        if re.match(pattern, line, re.IGNORECASE):
            datetime = parse(line.split(':')[1].strip())
            date = datetime.date()
            time = datetime.time()
            print(f'Registration for {domain} expires on {date } at {time}.')
            return
        elif any(s in line.lower() for s in ('no match', 'not found')):
            print(f'Domain name {domain} appears to not be registered.')
            return
    print(f'Sorry, could not parse an expiration date for {domain}.')


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        domain_expiration(arg)
