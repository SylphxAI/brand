# Han v3 trial: stroke skeletons, our brush, compact storage

- `han24.pips`: the 24 trial characters as component placements plus stroke
  centre lines (format in [../source/hanstroke.py](../source/hanstroke.py),
  `encode` and `decode`). A component used by two or more characters in the
  same slot is stored once.
- `brush-pebble.woff2`, `brush-pop.woff2`, `brush-block.woff2`: the same
  characters drawn from the decoded `han24.pips` by three parametric brushes
  (`BRUSHES` in `hanstroke.py`). They prove the round trip.
- `report.json`: the measured sizes, timings and the components a 6,855-character
  Traditional set shares. Produced by [../source/run_v3.py](../source/run_v3.py).

## Data and licence

The stroke centre lines, stroke order and component trees come from
[Make Me a Hanzi](https://github.com/skishore/makemeahanzi): `graphics.txt`
(derived from Arphic PL UKai and KaitiM) is under the Arphic Public License,
and `dictionary.txt` is under the GNU LGPL 3. The files in this directory
derive from that stroke data, so they are distributed under the Arphic Public
License ([LICENSE-APL.txt](LICENSE-APL.txt)), not the OFL that covers Pip Trial and
Pip Trial TC. The APL is copyleft: any font built from this data stays under
the APL. A product release would either accept that, or rebuild the centre
lines from an OFL source.

Noto Sans TC (SIL OFL) is used only as the comparison reference in the specimens.
