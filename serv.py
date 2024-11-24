import aiohttp
from aiohttp import web

import asyncio

import numpy as np
import sys
import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from env.deepmimic_env import DeepMimicEnv
from learning.rl_world import RLWorld
from util.arg_parser import ArgParser
from util.logger import Logger
import util.mpi_util as MPIUtil
import util.util as Util

# Dimensions of the window we are drawing into.
win_width = 800
win_height = int(win_width * 9.0 / 16.0)
reshaping = False

# anim
fps = 60
update_timestep = 1.0 / fps
display_anim_time = int(1000 * update_timestep)
animating = True

playback_speed = 1
playback_delta = 0.05

# FPS counter
prev_time = 0
updates_per_sec = 0

args = []
world = None

def build_arg_parser(args):
	arg_parser = ArgParser()
	arg_parser.load_args(args)

	arg_file = arg_parser.parse_string('arg_file', '')
	if (arg_file != ''):
		succ = arg_parser.load_file(arg_file)
		assert succ, Logger.print('Failed to load args from: ' + arg_file)

	rand_seed_key = 'rand_seed'
	if (arg_parser.has_key(rand_seed_key)):
		rand_seed = arg_parser.parse_int(rand_seed_key)
		rand_seed += 1000 * MPIUtil.get_proc_rank()
		Util.set_global_seeds(rand_seed)

	return arg_parser

def update_world(world, time_elapsed):
	num_substeps = world.env.get_num_update_substeps()  # 10
	timestep = time_elapsed / num_substeps  # 0.00166 (= 1 / 60 / 10)
	num_substeps = 1 if (time_elapsed == 0) else num_substeps

	for i in range(num_substeps):
		world.update(timestep)
		debug(world, timestep)

		valid_episode = world.env.check_valid_episode()
		if valid_episode:
			end_episode = world.env.is_episode_end()
			if (end_episode):
				world.end_episode()
				world.reset()
				break
		else:
			world.reset()
			break
	return

debug_frame = 0

def debug(world, timestep):
	global debug_frame
	for agent in world.agents:
		s = world.env.record_state(agent.id)
		# s には以下のフォーマットで姿勢データが格納されている
		# s[0] root ボーンの y 座標
		# s[1+(i+0)*9:1+(i+1)*9] ボーン 1 つあたりの座標/回転
		#   s[1:4 ] [x, y, z]
		#   s[4:7 ] [0, 1, 0] をクォータにオン q で回転させた後の値
		#   s[7:10] [1, 0, 0] をクォータにオン q で回転させた後の値
		# 詳細は DeepMimicCore/sim/CtController.cpp の RecordState 関数を参照
		s = s[1:136].reshape(15, 9)
		for p in s:
			#print(", ".join([str(x) for x in p]))
			pass
	debug_frame += 1
	return

def reload():
	global world
	global args

	world = build_world(args, enable_draw=False)
	return

def reset():
	world.reset()
	return

def shutdown():
	global world

	Logger.print('Shutting down...')
	world.shutdown()
	sys.exit(0)
	return

def animate(callback_val):
	global world

	if (animating):
		world.env.set_updates_per_sec(60);
		update_world(world, 1/60)

	if (world.env.is_done()):
		shutdown()

	return

def build_world(args, enable_draw, playback_speed=1):
	arg_parser = build_arg_parser(args)
	env = DeepMimicEnv(args, enable_draw)
	world = RLWorld(env, arg_parser)
	world.env.set_playback_speed(playback_speed)
	return world

async def handle(request):
	with open("index.html", "r") as f:
		return web.Response(text=f.read(), content_type="text/html")

def get_pose():
	poses = []
	for agent in world.agents:
		s = world.env.record_state(agent.id)
		s = s[1:136].reshape(15, 9)
		pose = "[" + ",".join(["[" + ",".join([str(x) for x in p]) + "]" for p in s]) + "]"
		poses.append(pose)
	return "[" + ",".join(poses) + "]"

async def websocket_handler(request):
	ws = web.WebSocketResponse()
	await ws.prepare(request)
	while True:
		animate(0)
		await ws.send_str(get_pose())
		await asyncio.sleep(1/60)
	print('websocket connection closed')
	return ws

app = web.Application()
app.add_routes([web.get('/', handle),
				web.get('/ws', websocket_handler)])

def main():
	global args
	args = sys.argv[1:]
	reload()
	web.run_app(app)

if __name__ == '__main__':
	main()
