import json
import random
from copy import deepcopy
from datetime import datetime, timedelta

from django.http import HttpResponseForbidden
from django.shortcuts import render, HttpResponse

from django.utils.translation import gettext_lazy as _

from django_ratelimit.exceptions import Ratelimited

from inquiry.models import Inquiry

def rate_limiter_view(request, *args, **kwargs):
    return render(request, 'ratelimit.html', status=429)


def view_404(request, *args, **kwargs):
    return render(request, '404.html', status=404)


def handler_403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return HttpResponse('Sorry too many requests, please wait', status=429)
    return HttpResponseForbidden('Forbidden')


def home_view(request):
    return render(request, 'home.html', status=200)


# ---------- admin dashboard view -----------------

chart_options = {
                    "animation": True,
                    "barThickness": 10,
                    "barPercentage": 1,
                    "base": 0,
                    "grouped": False,
                    "maintainAspectRatio": False,
                    "responsive": True,
                    "scales": {
                        "x": {
                            "grid": {
                                "display": False
                            },
                            "ticks": {
                                "maxRotation": 90,
                                "precision": 0 # Set precision to 0 to display only integer values
                                # "minRotation": 40,
                            }
                        },
                        "y": {
                            "grid": {
                                "display": False
                            },
                            "ticks": {
                                    "precision": 0 # Set precision to 0 to display only integer values
                                }
                            },
                    },
                    "plugins": {
                            "legend": {
                                "align": "end",
                                "display": False,
                                "position": "top",
                                "labels": {
                                    "boxHeight": 5,
                                    "boxWidth": 5,
                                    "color": "#9ca3af",
                                    "pointStyle": "circle",
                                    "usePointStyle": True,
                                },
                                },
                            "tooltip": {
                                    "enabled": True,
                                },

                            "datalabels": {
                                    "anchor": 'end', #remove this line to get label in middle of the bar
                                    "align": 'end',
                                    "color": "#9333ea",
                                    "labels": {
                                        "title": {
                                            "font": {
                                                "weight": 'bold',
                                                "size": 16
                                            }
                                        },
                                    }
                                }
                    },
                    "layout": {
                        "padding": 40
                    }
                }

horizontal_options = deepcopy(chart_options)
horizontal_options['indexAxis'] = 'y'


def dashboard_callback(request, context):
    """
        Callback to prepare custom variables for index template which is used as dashboard
        template. It can be overridden in application by creating custom admin/index.html.
    """

    current_date = datetime.now().date()

    cities = ["New York, United States", "San francisco, United States", 
                "Los Angeles, United States", "Manchester, UK",
                "Newcastle, UK", "Melbourne, Australia", "Sydney Australia"
            ]

    # cityCountry = {}
    cityCountry = {x: random.randint(100, 4000) for x in cities}
    dateTime = {current_date - timedelta(days=x): random.randint(500, 6000) for x in range(1, 30)}


    dateTime = dict(sorted(dateTime.items()))
    dateTime = {x.strftime("%B, %d, %Y"): y for x, y in dateTime.items()}

    cityCountry = dict(sorted(cityCountry.items(), key=lambda x: x[1], reverse=True))

    new_users = [random.randint(500, 14000) for x in range(8)]
    active_users = [random.randint(500, 14000) for x in dateTime.values()]

    context.update(
        {
            "navigation": [
                {"title": _("Dashboard"), "link": "#dashboard", "active": True},
                {"title": _("Analytics"), "link": "#analytics"},
                {"title": _("Settings"), "link": "#settings"},
            ],
            "filters": [
                # {"title": _("All"), "link": "#", "active": True},
                {
                    "title": _("New"),
                    "link": "#",
                },
            ], 
            "bar_options": json.dumps(chart_options),
            "horizontal_chart": json.dumps(horizontal_options),
            "inquiries": Inquiry.objects.all()[:5],
            # "newUsers": sum(newUsers),
            # "activeUsers": sum(activeCount),
            "visitors": {
                "newUsers": sum(new_users),
                "activeUsers": sum(active_users),
                "dateTime": json.dumps(
                        {
                            "labels": list(dateTime.keys()),
                            "datasets": [
                                {
                                    "label": "Visitors",
                                    "data": list(dateTime.values()),
                                    "backgroundColor": "#9333ea",
                                    
                                },  
                            ],
                            
                        }
                ),
                "cityCountry": json.dumps(
                        {
                            "labels": list(cityCountry.keys())[:5],
                            "datasets": [
                                {
                                    "label": "Visitors",
                                    "data": [x for x in cityCountry.values()][:5],
                                    "backgroundColor": "#9333ea",
                                    
                                },  
                            ],
                            
                        }
                ),
                
            }
            
        }
    )
    return context