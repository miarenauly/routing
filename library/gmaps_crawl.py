import googlemaps
from datetime import datetime
import json
import requests

"""
list_key = ['AIzaSyCdUGw_1KlNLB1t2an4cUj0PqWhgTb4HJ8',
'AIzaSyC0miiEYoowgdI1pXE_fuIeoEr192lmkTM',
'AIzaSyC7uWaT_2X6zu9Zw5jA1AY18pDd-bEZZDU', 
'AIzaSyCqWDFUaK2cPCXHO--CHxfFuZOW3YweaeQ',
'AIzaSyD3bLoM4QHREMBfyfRv3jXINndbKRO3_Q0',
'AIzaSyCMXF5C2YffXrYbFruSeRHZoLFYIAipDjs',
'AIzaSyB5Dj_o3TIyL_VaMoU4JmGa070-uWefeqY',
'AIzaSyCx8dLXHuMDPn_Mpo0F75ijt2YmjVXeI18',
'AIzaSyA4kdvlEzDa1IuaEJcyDy0Ex3eiUOvZsUc',
'AIzaSyAyGxQETJh3OetZ_sWwoGescGUQC6VoZJc',
'AIzaSyBxeAGhSsUr3z_wWnAlPznuhqfTKSfTosw',
'AIzaSyBkl8B9ddb6wG1XH_-WQBJV3LOTMMgndTk',
'AIzaSyBOrEPwInzXSeafvOXSvYz9VCsknyxnnLw',
'AIzaSyCCMYErfCa3ohViicUy2BHTZ0EEZSC6T7Y',
'AIzaSyCKItBq59jI4h_DZOyFkfg1WtZK1czxoBo',
'AIzaSyBt1paU35MV_ml5PYXxy243O_qN-ML3Dc4',
'AIzaSyCqjXn3PxRmVRKMiAGVye8KUb37bT81Jc4',
'AIzaSyC9YDTparoq93mROrIyqdqrH-1DMsSwElE',
'AIzaSyBPQbephBnOdGkGX2UdX4Gl_0sr5BmH4s8',
'AIzaSyAsOojEa4HJ2IrFTbx_i9zvQApx0IeRjEA',
'AIzaSyCUqwNOFtuCvmau_TKSv9IquPY5DDuZ7Kw',
'AIzaSyB-LtD3Md3ocfIgeYaCIge8LXeEPYOWmYc',
'AIzaSyDumSjLXVlTvteb4MfLxcvanc5GV0oN1a8',
'AIzaSyDy0ZzCU9ORSRNncc1rReeg8alFNxGP9RQ',
'AIzaSyCMs6AskeorcU9IFi1L7nbjTXysTX0Q8vs',
'AIzaSyDtkw3REru_7rvmvJMF1_bilBodDVekFLg',
'AIzaSyB9FIqa_ckue1ENkbOjJtVosTCP0BVjdzA',
'AIzaSyADYy_vre7E5Kwm7VCeuPIbrOX6fVa7_tY',
'AIzaSyB-8zSwqvCmHVq3ZU9fkSREZzUeh17vWEI',
'AIzaSyCvqlTd_Z7uS-kOgzYP7UsjpUdOaZjkGTE',
'AIzaSyA-5l1HbK8ye1N4Hh7qusnrP7aKMh3eBZ8',
'AIzaSyDa301rIK71x0z5W4GPlQ05XAoI1yDxbCE',
'AIzaSyCIMEu23Gnmd8-LppRzG2n_WfrlcU-wyn4',
'AIzaSyCO_5jhTary1xV0MSyw5P6N9qwt6EGZm9U',
'AIzaSyA_cVsBvbplOkkPkK2t_tuoKhYcsCdCp7E']

"""

gmaps = googlemaps.Client(key='AIzaSyCdUGw_1KlNLB1t2an4cUj0PqWhgTb4HJ8')

def google_direction(origin, destination):
    now = datetime.now()
    print(origin, destination)
    directions_result = gmaps.directions(
        origin, destination, mode="driving", departure_time=now, avoid="tolls|highways|ferries")
    return directions_result