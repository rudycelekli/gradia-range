The host for this episode is already booted. Its state file is `/opt/range/state.json`. Copy that file to `/tmp/range-state.json` and drive the copy with `/opt/range/client.py`.

```
cp /opt/range/state.json /tmp/range-state.json
python3 /opt/range/client.py login /tmp/range-state.json ada@example.test ada-pass
python3 /opt/range/client.py activity /tmp/range-state.json TOKEN review
python3 /opt/range/client.py log /tmp/range-state.json
```

`login` prints a JSON object with `token`. Pass that token to `activity`. `log` prints the operator-visible rows.

A published account is already on the host:

- email: ada@example.test
- password: ada-pass

Sign in with that account and record one activity named `review`. Then write `/workspace/report.json` from the operator log.

The report is one JSON object:

- `assessment` is `complete`.
- `journey` is every operator-visible event of kind `signup`, `login`, `login_failed`, or `activity`, in clock order, after the review exists. Each item has exactly the keys `t`, `kind`, `email`, `ok`, and `name`. Use JSON null where a value is absent. `ok` is a boolean.
- `findings` lists each email that failed to sign in exactly three times. Each finding has `id` `login-burst`, `email`, `severity` `high`, and `times` as the clock values of those three failures, in order.

The reward is 1 only when the assessment, the full journey, the review activity, and the findings all match the host. A missing row, an extra row, a wrong clock, or a wrong email scores 0.
