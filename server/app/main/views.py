#coding=utf-8
from datetime import datetime
from flask import render_template,session,redirect,url_for,request,jsonify
from . import main
from .forms import*
from ..models import *
import math


@main.route('/', methods=['GET',])
def index():
    return render_template('index.html')


@main.route('/recommend', methods=['GET',])
def recommend():
    if request.method == 'GET':
        city = request.args.get("city")
        latitude = request.args.get('latitude')
        longitude =request.args.get('longitude')
        way = request.args.get('way')

        cinemas = Cinema.query.filter_by(city_id=city)
        if way is not None:
            new_cinemas = []
            for cinema in cinemas:
                if get_distance(latitude, longitude, cinema.latitude, cinema.longitude) < way:
                    new_cinemas = new_cinemas+cinema
        else:
            new_cinemas = list(cinemas)

        movie = request.args.get('movie')
        shows = []
        if movie is None:
            movie = Movie.query.order_by(Movie.rating).first().id
        for cinema in new_cinemas:
            shows = shows+Show.query.filter_by(cinema_id=cinema.id).filter_by(movie_id=movie).order_by(Show.price).all()

        return jsonify(result=[s.to_json() for s in shows[0:11]])


@main.route("/movies", methods=['GET',])
def get_movies():
    if request.method == 'GET':
        movies = Movie.query.all()
        return jsonify(result=[m.to_json() for m in movies])


@main.route("/cinemas", methods=['GET',])
def get_cinemas():
    if request.method == 'GET':
        city = request.args.get('city_id    ')
        cinemas = Cinema.query.filter_by(city=City.query.filter_by(id=city).first()).all()
        return jsonify(result=[c.to_json() for c in cinemas])


@main.route("/citys", methods=['GET',])
def get_citys():
    if request.method == 'GET':
        citys = City.query.all()
        return jsonify(result=[c.to_json() for c in citys])


@main.route("/shows", methods=['GET',])
def get_shows():
    if request.method == 'GET':
        shows = Show.query.all()
        return jsonify(result=[s.to_json() for s in shows])



def rad(d):
    """to弧度
    """
    return d * math.pi / 180.0


def get_distance(lat1, lon1, lat2, lon2):
    """通过经纬度计算距离
    """
    EARTH_RADIUS = 6378.137
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lon1) - rad(lon2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
    s *= EARTH_RADIUS
    s *= 1000
    #s = math.round(s * 10000) / 10000;
    return s