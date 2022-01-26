"""
Copyright (c) Facebook, Inc. and its affiliates.

This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""

from torchmetrics import Metric
import torch


class DistributedArraySum(Metric):
    def __init__(self, dist_sync_on_step=True):
        super().__init__(dist_sync_on_step=dist_sync_on_step)

        self.add_state("quantity", default=torch.zeros(1), dist_reduce_fx="sum")

    def update(self, batch: torch.Tensor):  # type: ignore
        if self.quantity.shape == torch.Size([1]):  # type: ignore
            self.quantity = self.quantity.expand(batch.shape[0]).clone()  # type: ignore
        self.quantity += batch.to(self.quantity.device)

    def compute(self):
        return self.quantity
