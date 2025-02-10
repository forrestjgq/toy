# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import audio
from usr.modules.logging import getLogger
import asyncio
from collections import deque
import time


logger = getLogger(__name__)



class Player(object):

    def __init__(self, device=0, pa_gpio=None):
        self.aud = audio.Audio(device)
        if pa_gpio is not None:  # 设置pa的gpio, 放大声音(如有需要则设置)
            self.aud.set_pa(pa_gpio, 2)
        self.aud.setCallback(self.audio_cb)
        self.audios = deque()
        self.stop()
        self.evt = asyncio.Event()

    def audio_cb(self, event):
        if event == 0:
            logger.info('audio play start.')
        elif event == 7:
            logger.info('audio play finish.')
            def notify_player():
                self.evt.set()
            asyncio.get_running_loop().call_soon_threadsafe(notify_player)


    async def play(self, q: asyncio.Queue):
        while True:
            try:
                buf = q.get_nowait()
                self.aud.playStream(2, buf)
                await self.evt.wait()
            except asyncio.QueueEmpty:
                await asyncio.sleep(0.01)

    def add_audio(self, buf):
        self.audios.append(buf)


    def stop(self):
        self.aud.stopAll()

    def setVolume(self, level):
        # level: 0~11音量大小，0表示静音
        self.aud.setVolume(level)

async def play(q, *args, **kwargs):
    player = Player(*args, **kwargs)
    await player.play(q)