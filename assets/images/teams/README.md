# Team crests

Drop a crest in here named after the team's slug and it appears on that team's
fixture cards. Nothing else to update, and **no need to convert or resize it
first**: the *Optimise Images* workflow turns whatever you drop in into a
120px webp with a lowercase filename and commits it back.

- `cardiff-city.webp` covers Cardiff City 1, 2 and 3
- squad numbers are stripped, so one file serves all of a club's sides
- name the file after the club: `Cardiff City.png` becomes `cardiff-city.webp`
- `webp`, `png`, `svg`, `jpg` and `jpeg` are all accepted

Newport's own badge comes from `crest:` in `_data/club.yml`, not from here.

Without a file, the team shows its initials in the category colour, so a
missing crest looks deliberate rather than broken.

They render at 30px as a rounded square. Backgrounds are left alone: some of
these clubs use a white badge and some a dark one, and that is how their crest
actually looks.

To do it by hand instead of waiting for CI:

```
python3 -m venv /tmp/imgenv && /tmp/imgenv/bin/pip install pillow
/tmp/imgenv/bin/python .github/scripts/optimise-images.py
```
