# --------------------------------------------------------
# This code is modified from jayleicn's repository.
# https://github.com/jayleicn/TVQAplus
# --------------------------------------------------------

import torch
import math
import torch.nn as nn


class PositionEncoding(nn.Module):
    def __init__(self, n_filters=128, max_len=500):
        super(PositionEncoding, self).__init__()
        # Compute the positional encodings once in log space.
        pe = torch.zeros(max_len, n_filters)  # (L, D)
        position = torch.arange(0, max_len).float().unsqueeze(1)
        div_term = torch.exp(torch.arange(0, n_filters, 2).float() * - (math.log(10000.0) / n_filters))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)  # buffer is a tensor, not a variable, (L, D)

    def forward(self, x):
        """
        :Input: (*, L, D)
        :Output: (*, L, D) the same size as input
        """
        pe = self.pe.data[:x.size(-2), :]  # (#x.size(-2), n_filters)
        extra_dim = len(x.size()) - 2
        for _ in range(extra_dim):
            pe = pe.unsqueeze(0)

        return pe


def test_pos_enc():
    mdl = PositionEncoding()

    batch_size = 8
    n_channels = 128
    n_items = 60

    input = torch.ones(batch_size, n_items, n_channels)

    out = mdl(input)
    print(out)


if __name__ == '__main__':
    test_pos_enc()
