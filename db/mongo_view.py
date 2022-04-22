import db_connect as dbc
import sys


client = dbc.get_client()


def main():
    ret = dbc.all_docs(sys.argv[1])
    for doc in ret:
        print(doc)


if __name__ == "__main__":
    main()  # noqa:W292