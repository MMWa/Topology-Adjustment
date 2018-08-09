import json
import uuid

from helpers.enums import Mode, PacketType
from helpers.packet import Packet
from node import gateway, relay, endnode
from simulation.IPMaker import IPMaker
from simulation.PropagationModel import PropagationModel
from simulation.world import World


class Sandbox(IPMaker, World, PropagationModel):
    def __init__(self):
        IPMaker.__init__(self)
        World.__init__(self)
        PropagationModel.__init__(self)
        self.nodes = []
        self.nodes.append(gateway(2, 2, self.get_address()))
        self.transactionQue = []
        self.transaction_log = []

    def add_relay(self, x, y):
        newAddress = self.get_address()
        self.nodes.append(relay(x, y, newAddress))
        return newAddress

    def add_endnode(self, x, y):
        newAddress = self.get_address()
        self.nodes.append(endnode(x, y, newAddress))
        return newAddress

    def broadcast(self, node, packet):
        for receiver in self.nodes:
            if not node.address == receiver.address:

                sender = node.get_position()
                p2 = receiver.get_position()

                signal_level = self.get_receiver_power(sender, p2, node.tx_power)
                if receiver.rx_sensitivity < signal_level:
                    # if the SNR is enough to decode a message then show it to the receiver
                    receiver.receive(packet, signal_level)
                    self.transaction_log.append([packet.src, packet.dst])

    def tick(self):
        # iterate over all the Node and preform any internal logic
        for x in self.nodes:
            x.run()

        # if a Node has something to broadcast take it and store it in transactionQue
        for x in self.nodes:
            hold_buf = x.Out_packetBuffer

            if not hold_buf is None:
                # if there is nothing to send dont store it in transactionQue
                for message in hold_buf:
                    self.transactionQue.append((x, message))
                if x.spawn_flag:
                    address_hold = self.add_relay(3, 2.6)
                    x.new_address = address_hold
                    Packet(Mode.Standard, PacketType.ACK_iRecommend, False, ID=uuid.uuid4(), src=x.new_address,
                           dst=x.iRecommend_complainer)
                    x.spawn_flag = False

        for (x, y) in self.transactionQue:
            # try to broadcast a Packet to all nodes in simulation
            # this is an internal simulation step
            # The implemented behavior is anything within transmission range can receive a Packet

            self.broadcast(x, y)
        self.transactionQue = []

    def serialize(self):
        state_buffer = []
        for x in self.nodes:
            state_buffer.append([x.address, x.get_position(), str(x.nodeType)])
        state_buffer = state_buffer, self.transaction_log
        self.transaction_log = []
        return json.dumps(state_buffer)

    def shutdown(self):
        for x in self.nodes:
            x.shutdown()
