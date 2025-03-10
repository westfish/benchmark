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


@benchmark_registry.register("argsort")
class ArgsortConfig(APIConfig):
    def __init__(self):
        super(ArgsortConfig, self).__init__("argsort")

    def to_tensorflow(self):
        tf_config = super(ArgsortConfig, self).to_tensorflow()
        if self.descending:
            tf_config.direction = "DESCENDING"
        else:
            tf_config.direction = "ASCENDING"
        return tf_config


@benchmark_registry.register("argsort")
class PaddleArgsort(PaddleOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        indices = paddle.argsort(
            x=x, axis=config.axis, descending=config.descending)

        self.feed_list = [x]
        self.fetch_list = [indices]


@benchmark_registry.register("argsort")
class TorchArgsort(PytorchOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        indices = torch.argsort(
            x=x, axis=config.axis, descending=config.descending)

        self.feed_list = [x]
        self.fetch_list = [indices]


@benchmark_registry.register("argsort")
class TFArgsort(TensorflowOpBenchmarkBase):
    def build_graph(self, config):
        x = self.variable(name='x', shape=config.x_shape, dtype=config.x_dtype)
        indices = tf.argsort(
            values=x,
            axis=config.axis,
            direction=config.direction,
            stable=False)

        self.feed_list = [x]
        self.fetch_list = [indices]
