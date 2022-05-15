import json
import typing as tp


PRINT_PADDING = 30


class Node:
    def __init__(self, ip: str, adj_nodes: tp.List[str]):
        self.ip = ip
        self.adjlist = adj_nodes
        self.dist_vector: tp.Dict[str, int] = {adj: 1 for adj in self.adjlist}
        self.next_vector: tp.Dict[str, str] = {adj: adj for adj in self.adjlist}

    def update(self, node_name: str, value: int, next_node: str) -> bool:
        if next_node == '':
            return False

        if node_name not in self.dist_vector or self.dist_vector[node_name] > value:
            self.dist_vector[node_name] = value
            self.next_vector[node_name] = next_node

            return True

        return False

    def dist(self, node_name: str) -> int:
        return self.dist_vector.get(node_name, -1)

    def next_node(self, node_name: str) -> str:
        return self.next_vector.get(node_name, '')

    def _print_header(self) -> None:
        print(
            f'{"[Source IP]":{PRINT_PADDING}} {"[Destination IP]":{PRINT_PADDING}} '
            f'{"[Next Hop]":{PRINT_PADDING}} {"[Metric]":{PRINT_PADDING}}'
        )

    def _print_record(self, dest_ip: str) -> None:
        print(
            f'{self.ip:{PRINT_PADDING}} '
            f'{dest_ip:{PRINT_PADDING}} '
            f'{self.next_vector[dest_ip]:{PRINT_PADDING}} '
            f'{str(self.dist_vector[dest_ip]):{PRINT_PADDING}}'
        )

    def print_status(self) -> None:
        self._print_header()

        for node_name in self.dist_vector:
            self._print_record(node_name)


class RIP:
    def __init__(self, net: tp.Dict[str, Node]):
        self.step = 0
        self.net = net

    def one_step(self) -> bool:
        updated = False

        for _, from_node in net.items():
            for _, to_node in net.items():
                if from_node.ip == to_node.ip:
                    continue

                for adj_node_name in to_node.adjlist:
                    adj_node = self.net[adj_node_name]

                    updated |= from_node.update(
                        to_node.ip,
                        from_node.dist(adj_node.ip) + 1,
                        from_node.next_node(adj_node.ip)
                    )

        if updated:
            self.step += 1

            for _, node in self.net.items():
                print(f'Simulation step {self.step} of router {node.ip}')

                node.print_status()

                print('\n')

        return updated

    def simulate(self):
        while self.one_step():
            pass

        for _, node in self.net.items():
            print(f'Final state of router {node.ip} table:')

            node.print_status()

            print('\n')


if __name__ == '__main__':
    net_draft = json.load(open('rip/config.json', 'r'))

    net = {ip: Node(ip, adj_nodes) for ip, adj_nodes in net_draft.items()}

    rip = RIP(net)
    rip.simulate()
