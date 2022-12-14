import os
import sys

import carla

from src.common.session import Session
from src.common.spawn import spawn_vehicles, spawn_ego
from src.sensors.camera import Camera
from src.util.timer import Timer


output_dir = sys.argv[1]


with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(autopilot=True)

    camera = Camera(parent=ego, transform=carla.Transform(carla.Location(z=2.7)))
    camera_queue = camera.add_queue()

    camera.start()

    timer_iter = Timer()

    iteration = 0

    os.makedirs(output_dir, exist_ok=True)

    while iteration < 1000:
        timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')
        session.world.tick()
        image = camera_queue.get()
        if iteration % 100 == 0:
            print('save')
            image.save_to_disk(f'{output_dir}/image_{image.frame:06d}.png')
        iteration += 1
