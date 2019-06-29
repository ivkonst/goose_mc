def pad_list(batch, pad=None, sort=True):
    """
    Adds padding for lists to same length.
    Used to pad sentences in batch
    :param batch: exmaple [ [1,2,3], [1,2] ]
    :param pad: value generating function to pad with
    :return:
    >>> pad_list([[1,2,3], [1,2] ], int)
    [[1, 2, 3], [1, 2, 0]]
    """

    if pad is None:
        pad = list
    batch_lengths = list(map(len, batch))
    max_len = max(batch_lengths)

    for seq, length in zip(batch, batch_lengths):
        diff = max_len - length
        for idx in range(diff):
            seq.append(pad())
            
    if sort:
        batch = [
            batch[i] for i, _ in sorted(
                {i:batch_length for i, batch_length in enumerate(batch_lengths)}.items(), key=lambda x: x[1], reverse=True
            )
        ]
        return batch
    else:
        return batch, batch_lengths
