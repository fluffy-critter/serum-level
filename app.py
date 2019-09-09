import flask
import math
import itertools

app = flask.Flask(__name__)


@app.route('/')
def index():
    from flask import request
    start_level = float(request.args.get('start_level', 0))
    dose = float(request.args.get('dose', 0))
    frequency = float(request.args.get('frequency', 24))
    half_life = float(request.args.get('half_life', 24))

    threshold = float(request.args.get('threshold', 0.0001))

    def levels():
        level = start_level
        beta = 0.5**(frequency/half_life)

        time = 0

        while True:
            previous = level
            attenuated = previous*beta
            level = attenuated + dose

            if threshold is not None and abs(level - previous) < threshold:
                break
            yield int(time/24), int(time%24/frequency + 1), attenuated, level

            time += frequency

    rows = list(itertools.islice(levels(), 500))

    return flask.render_template(
        'index.html',
        args={
            'start_level': start_level,
            'dose': dose,
            'frequency': frequency,
            'half_life': half_life,
            'threshold': threshold},
        rows=rows
        )
