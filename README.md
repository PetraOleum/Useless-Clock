# Useless-Clock

Mastodon bot for random times, DST changes, and other timekeeping ephemera.

Add a mastodon secrets file to `usercred.secret` and you're basically good to go.

Running in cron at a random time each hour probably needs something like:

```
0 * * * * bash -c "sleep $[RANDOM\%60]m" ; python3 /path/to/clock.py --usercred /path/to/usercred.secret >> /path/to/clock-log.txt 2>&1
```
