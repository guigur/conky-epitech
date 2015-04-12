#By guigur 2015

import requests
import math
import sys
import cairo
import pycha.pie
import pycha.ring

global lines
global log
global token
token = ""

#your login 
user = "epitec_h"
#you unix password
password = "passwd"
#it can be your login or another one
log_user = "epitec_h"

def calcul_time_off():
        if log['nsstat']['active'] > log['nsstat']['nslog_norm']:
                norm = 72
        else:
                norm = log['nsstat']['nslog_norm']
        time_off = (norm - log['nsstat']['active'] - log['nsstat']['idle'])
        return time_off

def is_ok():
        if log['nsstat']['active'] > log['nsstat']['nslog_norm']:
                return(0)
        else:
                return(1)

def getToken():
        global token

        #if (token == ""):
        #        print("il est pas null")
        
	login_url = 'http://epitech-api.herokuapp.com/login'
	login_values = {'login': 'arthau_g', 'password': 'sjs&9<yb'}
        token_req = requests.get(login_url, params=login_values)
        eltoken = token_req.json()
        token = eltoken['token']

def getLog():
	global log
        global lines
        infos_url = 'http://epitech-api.herokuapp.com/user'
	log_param = {'token': token, 'user': log_user}
	log_req = requests.get(infos_url, params=log_param)
        log = log_req.json()
	lines = (
	    ('active', log['nsstat']['active']),
	    ('idle', log['nsstat']['idle']),
	    ('out_active', log['nsstat']['out_active']),
	    ('out_idle', log['nsstat']['out_idle']),
            ('time_off', calcul_time_off())
        )
	print(log['nsstat']['active'])
        if (is_ok() == 0):
                print("fais plus de log")

        
#getToken()
#getLog()
#print(token)

def ringChart(output):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 256, 256)

    dataSet = [(line[0], [[0, line[1]]]) for line in lines]

    options = {
            'axis':{
		'labelColor': '#ffffff',
		  'x': {
                          'hide': 'True',
                     
        		},
		},
        'legend': {
            'hide': True,
	},
        'background': {
            'hide': True,
	},
	'colorScheme': {
        'name': 'fixed',
        'args': {
                'colors': ['#40ff40', '#dcffdc', '#ff8080', '#ffdcdc', '#c3c3c3'],
            },
        },
    }
    chart = pycha.ring.RingChart(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(output)

def pieChart(output):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 256, 256)

    dataSet = [(line[0], [[0, line[1]]]) for line in lines]

    options = {
	'axis':{
		'labelColor': '#ffffff',
		  'x': {
                          'hide': 'True',
                          'ticks': [dict(v=1, label=1)],
        		},
		},
	'legend': {
            'hide': True,
        },
        'background': {
            'hide': True,
        },
	'colorScheme': {
        	'name': 'fixed',
        	'args': {
         		'colors': ['#40ff40', '#dcffdc', '#ff8080', '#ffdcdc', '#c3c3c3'],
            		},
        },
    }
    chart = pycha.pie.PieChart(surface, options)

    chart.addDataset(dataSet)
    chart.render()

    surface.write_to_png(output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        output = sys.argv[1]
    else:
        output = '.conky/conky-epitech/log.png'

#pieChart(output)
ringChart(output)



