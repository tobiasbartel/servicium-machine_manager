from models import *
from pprint import pprint
from servicecatalog.models import READ, WRITE, BOTH
from instance_manager.models import Instance
import pydotplus
import re

def machine(my_instance_name, my_payment_methods_list=None):

    my_instance = Instance.objects.get(slug=my_instance_name)
    list_of_machines = Machine.objects.all().filter(instance=my_instance).order_by('zone').order_by('type').order_by('name')


    ARROW_SIZE = 0.7
    FONT_SIZE = 8

    graph = pydotplus.Dot(graph_type='digraph', graph_name='%s Hardware' % my_instance.__unicode__(), strict=True)
    # graph.set_prog('fdp')
    graph.set('splines', 'ortho')
    # graph.set('rankdir', 'LR')
    graph.set('overlap', 'false')
    graph.set('splines',  True)
    graph.set('nodesep', 0.5)
    graph.set('stylesheet', '/static/PaymentFont/css/paymentfont.css')
    # graph.set('newrank', True)
    graph.set('concentrate', True)

    machine_type = ''
    machine_type_graph = None

    for my_machine in list_of_machines:
        if machine_type != my_machine.type:
            #pprint('Change %s to %s' % (machine_type, my_machine.type, ))
            if machine_type_graph is not None:
                # pprint('Adding Graph %s' % (machine_type,))
                graph.add_subgraph(machine_type_graph)
            machine_type_graph = pydotplus.Subgraph(graph_name=my_machine.type.name)
            machine_type = my_machine.type

        node = pydotplus.Node()
        node.set_name(my_machine.name)
        if my_machine.type.name == 'loadbalancer':
            node.set('shape', 'hexagon')
        else:
            node.set('shape', 'box')
        node.set('fontsize', FONT_SIZE)
        node.set('fontname', 'PaymentFont,sans-serif')
        machine_type_graph.add_node(node)

        list_of_dependencies = MachineConnectMachine.objects.all().filter(from_machine=my_machine)
        for dependency in list_of_dependencies:
            edge = pydotplus.Edge(dependency.from_machine.name, dependency.to_machine.name)
            edge.set('arrowsize', ARROW_SIZE)
            edge.set('fontsize', FONT_SIZE)
            edge.set('fontname', 'PaymentFont,sans-serif')
            if dependency.comment is not None:
                edge.set('xlabel', 'Port: %s' % dependency.port)
            if dependency.access_direction == READ:
                edge.set('dir', 'back')
            elif dependency.access_direction == BOTH:
                edge.set('dir', 'both')
            graph.add_edge(edge)

        if my_machine.customer_accesable:
            node = pydotplus.Node()
            node.set_name('Merchant')
            node.set('fontsize', FONT_SIZE)
            node.set('fontname', 'PaymentFont,sans-serif')
            node.set('fillcolor', 'cornflowerblue')
            node.set('style', 'filled')
            node.set('shape', 'invhouse')
            graph.add_node(node)
            edge = pydotplus.Edge('Merchant', my_machine.name)
            edge.set('arrowsize', ARROW_SIZE)
            graph.add_edge(edge)
    graph.add_subgraph(machine_type_graph)

    my_graph = graph.create(format='svg', )
    my_graph = re.sub(r"( width=)", " min-width=", my_graph)
    my_graph = re.sub(r"( height=)", " min-height=", my_graph)

    return my_graph
