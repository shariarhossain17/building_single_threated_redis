from redis_server import RedisServer


def main():
    server=RedisServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("server closed by user...")
        server.stop()


if __name__ =="__main__":
    main()