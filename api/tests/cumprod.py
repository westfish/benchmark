#   Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
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

from common_import import *


@benchmark_registry.register("cumprod")
class CumprodConfig(APIConfig):
    def __init__(self):
        super(CumprodConfig, self).__init__('cumprod')
        self.feed_spec = {"range": [-1, 1]}


@benchmark_registry.register("cumprod")
class PaddleCumprod(PaddleOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        result = paddle.cumprod(x=x, dim=config.dim)

        self.feed_list = [x]
        self.fetch_list = [result]
        if config.backward:
            self.append_gradients(result, [x])


@benchmark_registry.register("cumprod")
class TorchCumprod(PytorchOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        result = torch.cumprod(x=x, dim=config.dim)

        self.feed_list = [x]
        self.fetch_list = [result]
        if config.backward:
            self.append_gradients(result, [x])
