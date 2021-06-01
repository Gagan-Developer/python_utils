import logging
from kazoo.client import KazooClient

def setup_logging():
    log_file = 'zksearch.log'
    FORMAT = '%(asctime)-15s %(funcName)s %(message)s'

    logging.basicConfig(filename=log_file,format=FORMAT)

    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    return log

def create_Kazoo_client(host, port):
    global log
    log = setup_logging()
    log.debug('creating Kazoo client')
    global zk
    zk = KazooClient(hosts=host + ':' + str(port), max_retries=5)
    log.debug('Starting ZK')
    zk.start()
    log.debug('Started ZK')

def search_keyword(word, search_data, path_list, index):
    if index == len(path_list):
        return search_data

    while index < len(path_list):
        parent_path = path_list[index]
        children = zk.get_children(parent_path)
        path_list.remove(parent_path)
        if children:
            child_list = list(map(lambda child: parent_path + '/' + child, children))
            path_list.extend(child_list)
            search_keyword(word, search_data, path_list, index + 1)
        else:
            data = str(zk.get(parent_path))
            if word in data:
                search_data.append(parent_path)
                break

    return search_data

def main():
    create_Kazoo_client('192.168.1.1', 2181)
    word = "0CAEEF4E38C9FB2DD1EA08539D628360"
    search_data = []
    path_list = ['']
    search_list = search_keyword(word, search_data, path_list, 0)
    print(search_list)


if __name__ == "__main__":
    main()
