from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import *



db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sources')
def source_table():
    return render_template('source_table.html')

@app.route('/samples')
def sample_table():
    return render_template('sample_table.html')


@app.route('/api/data')
def data():
    query = Source.query

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            Source.name.like(f'%{search}%'),
            Source.upn.like(f'%{search}%'),
            Source.fab.like(f'%{search}%'),
            Source.karyotype.like(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in ['upn', 'name', 'age', 'sex', 'dx', 'karyotype', 'fab']:
                name = 'name'
            col = getattr(Source, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [source.to_dict() for source in query],
        'total': total,
    }


if __name__ == '__main__':
    app.run()
