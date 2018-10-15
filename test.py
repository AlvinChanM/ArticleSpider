# coding=utf-8
__author__ = "alvin"
__date__ = "2018/4/28 13:51"
import redis
redis_cli = redis.StrictRedis()
redis_cli.incr("jobbole_count")