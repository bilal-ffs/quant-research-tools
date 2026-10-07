# Drawdown and recovery

All drawdown metrics compound periodic **simple returns**, beginning with equity
`E_0 = 1.0`. The high-water mark at each observation is
`max(1.0, E_1, ..., E_t)` and drawdown is `E_t / peak - 1`, a negative decimal.
Starting capital participates in the peak calculation without adding a row to the
returned series. For `[-0.10, 0.05]`, drawdown is `[-0.10, -0.055]`.

```python
import pandas as pd
from quanttools.statistics import (
    drawdown_series, max_drawdown, drawdown_duration,
    drawdown_episodes, recovery_time,
)

returns = pd.Series([-0.2, 0.25, -0.1],
                    index=pd.date_range("2024-01-01", periods=3))
print(drawdown_series(returns))
print(drawdown_episodes(returns))
print(recovery_time(returns))  # 1: deepest episode recovered at an equal peak
```

## Episodes table

`drawdown_episodes(returns)` returns one row per excursion below a peak, in input
observation order. Recovery means **reaching or exceeding** the previous peak;
an equal peak ends an episode. Equal peaks reset the peak label to the latest
observation, while tied troughs select the first minimum.

| Column | Meaning |
| --- | --- |
| `peak` | Input label of the preceding peak; missing for initial equity |
| `trough` | Input label of the episode's first lowest equity |
| `recovery` | Input label reaching/exceeding the prior peak; missing if open |
| `peak_position` | Zero-based position in the cleaned input; `-1` for initial equity |
| `trough_position` | Zero-based trough position |
| `recovery_position` | Nullable zero-based recovery position |
| `depth` | Negative trough-to-peak fractional decline |
| `underwater_duration` | Count of strictly underwater observations, excluding recovery |
| `trough_to_recovery_duration` | Recovery position minus trough position; nullable if open |
| `recovered` | Whether a recovery was actually observed |

Timestamp labels are preserved. Initial equity has no invented timestamp: its peak
label is `None` (pandas may render this as `NaT`/`NaN`) and position is `-1`.
The position columns distinguish initial equity from any missing input label.

An unrecovered episode has `recovered=False`, missing recovery label/position,
and missing trough-to-recovery duration. Its underwater duration is the observed
age, **not a completed recovery time**. Counts refer to observations, not calendar
or trading days. Missing returns are removed before counting; retained labels and
order remain intact. No-drawdown inputs return an empty table with the same columns.

`recovery_time(returns)` returns the trough-to-recovery observation count for the
**deepest episode**. It returns `None` if that episode is unrecovered and `0` if
there was no drawdown. Equal-depth episodes select the first. It does not select a
shallower completed episode in place of an unrecovered deepest episode.

`drawdown_duration(returns)` retains its convention: the longest consecutive count
of strictly underwater observations, including open episodes. `max_drawdown`
returns the minimum negative drawdown. Calmar uses `CAGR / abs(max_drawdown)`;
zero drawdown makes the ratio undefined and raises `ValueError`. Ulcer index is
the root mean square of observation drawdowns in decimal units; starting equity
sets the initial peak but adds no extra zero to the mean.

A `-1.0` return is bankruptcy, so compounded equity remains zero thereafter.
Drawdown remains `-1.0` and recovery is open. Returns below `-1.0` are rejected.
See [input conventions](conventions.md) for validation and undefined metrics.
