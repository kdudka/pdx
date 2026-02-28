# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 The PDX Project Authors

from pdx.model import Model
from pdx.qdrant import VDB

import os

from tqdm import tqdm


# TODO: make this configurable
BATCH_SIZE_CUDA = 250


class Indexer:
    model: Model

    def __init__(self):
        self.model = Model()

    def _index_results(self, vdb: VDB, results: list[str]) -> None:
        if not results:
            return

        # Single batch forward pass (saturates GPU/CPU better)
        tensors = [tensor for _, tensor in results]
        vectors = self.model.tensors_to_vectors(tensors)

        # Batch upsert to Qdrant
        paths = [path for path, _ in results]
        vdb.upsert_batch(vectors, paths)

    def index_photos(self, cname: str, photos: list[str]) -> None:
        vdb = VDB(cname=cname)
        vdb.init_collection()

        if self.model.device == "cuda":
            batch_size = BATCH_SIZE_CUDA
        else:
            batch_size = os.cpu_count() or 1

        total = len(photos)
        with tqdm(total=total, unit="img") as pbar:
            for pos in range(0, total, batch_size):
                batch = photos[pos : pos + batch_size]

                # Load and preprocess images in parallel (uses more CPU)
                results = self.model.preprocess_img_batch(batch, pbar)
                self._index_results(vdb, results)
