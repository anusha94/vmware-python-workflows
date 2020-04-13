import argparse



parser = argparse.ArgumentParser()
parser.add_argument("--server",
                    help="VC server to connect to")
parser.add_argument("--username",
                    help="username used for VC connection")
parser.add_argument("--password",
                    help="password used for VC connection")
parser.add_argument("--skipverification",
                    action='store_true',
                    help="don't verify certs during connection")