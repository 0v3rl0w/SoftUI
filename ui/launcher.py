#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pygame

from utils.apps import *
from typing import Tuple

class Launcher:
    def __init__(self, screen_res: Tuple[int, int]):
        self.surface = pygame.Surface(screen_res)
        sys.path.insert(0, os.environ["APP"])

        self.apps  = scan_for_apps()
        self.icons = get_app_icons(self.apps)
        self.colliders = []

        self.screen_res = screen_res
        self.appObject = None
        self.appName = ""

    def draw(self):
        self.surface.fill((0, 0, 0))
        x = 20
        y = 20
        for icon in self.icons:
            self.colliders.append(self.surface.blit(icon.get_surface(), (x, y)))
            x += 60

            if x > self.screen_res[0]-60:
                x = 20
                y += 90

            #if y > self.screen_res[1] - 90:
            # TODO

    def get_surface(self) -> pygame.Surface:
        if self.appObject is not None:
            self.surface.blit(self.appObject.get_surface(), (0, 0))
        else:
            self.draw()

        return self.surface

    def closeApp(self):
        if self.appObject is not None:
            self.appObject = None


    def mainloop(self, event):
        if self.appObject is not None:
            self.appObject.mainloop(event)

    def handler(self, cursor: Tuple[int, int]):
        if self.appObject is None:
            for icon in self.colliders:
                if icon.collidepoint(cursor):
                    self.appName = self.icons[self.colliders.index(icon)].get_app_name()
                    exec("import apps.{0}.main as {0}".format(self.appName))
                    self.appObject = eval(f"{self.appName}.callObject({self.screen_res})")
