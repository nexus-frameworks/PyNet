import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--server', action='store_true', default=False)

    return parser.parse_args()

def main():
    args = parse_args()
    if args.server:
        import server.server as server
        server.main(args.host, args.port)
    else:
        import client.client as client
        client.main(args.host, args.port)