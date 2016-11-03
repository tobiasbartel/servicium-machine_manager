from django.shortcuts import render
import graphgenerator
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from main.settings import TEMPLATE_NAME


def machine_graph(request, my_instance_name, ):
    my_graph = graphgenerator.machine(my_instance_name)

    response = HttpResponse(my_graph, content_type='image/svg+xml')
    response['Content-Length'] = len(my_graph)
    return response
