The host for this episode is already booted. Its state file is `/opt/range/state.json`. Copy that file to `/tmp/range-state.json` and drive the copy with `/opt/range/client.py`.

```
cp /opt/range/state.json /tmp/range-state.json
python3 /opt/range/client.py login /tmp/range-state.json ada@example.test ada-pass
python3 /opt/range/client.py activity /tmp/range-state.json TOKEN review
python3 /opt/range/client.py log /tmp/range-state.json
```

`login` prints a JSON object with `token`. Pass that token to `activity`.

A published account is already on the host:

- email: ada@example.test
- password: ada-pass

Sign in and record one activity named `review`. Then write `/workspace/handoff.json`.

The file is a JSON list of four objects, in this order, for the sign-in burst on the operator log:

1. `frm` `watch`, `to` `sense`
2. `frm` `sense`, `to` `confirm`
3. `frm` `confirm`, `to` `close`
4. `frm` `close`, `to` `tell`

Every object has `kind` `handoff`, `seat` `operator`, and `gap` `login_burst`. `t` is the clock of the last operator-visible row after the review, and the same `t` on all four objects.

The reward is 1 only when the list matches that chain. A wrong clock, a missing handoff, or an extra object scores 0.
