from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import *
from flask import Flask, render_template, Response, request, redirect, url_for


db.create_all()

app.url_map.strict_slashes = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sources')
def source_table():
    return render_template('source_table.html')

@app.route('/samples')
def sample_table():
    return render_template('sample_table.html')


@app.route('/api/source_data')
def source_data():
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
        'source_data': [source.to_dict() for source in query],
        'total': total,
    }
    
    
    
@app.route('/api/sample_data')
def sample_data():
    query = Sample.query

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            Sample.usn.like(f'%{search}%'),
            Sample.upn.like(f'%{search}%'),
            Sample.name.like(f'%{search}%'),
            Sample.type.like(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in ['usn', 'upn', 'name', 'type', 'collectiondate', 'time_point_weeks']:
                name = 'name'
            col = getattr(Sample, name)
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
        'sample_data': [sample.to_dict() for sample in query],
        'total': total,
    }

@app.route('/samples/<int:upn_id>')
def sample_table_per_upn(upn_id):
    query = Sample.query.filter_by(upn=upn_id).all()
    return render_template('sample_table_per_upn.html', samples=query)

@app.route('/sample_details/<int:usn_id>')
def sample_details(usn_id):
    query = Sample.query.filter_by(usn=usn_id).first()
    return render_template('sample_details.html', sample=query)

@app.route('/source_details/<int:upn_id>')
def source_details(upn_id):
    query = Source.query.filter_by(upn=upn_id).first()
    upn_samples_number = len(Sample.query.filter_by(upn=upn_id).all())
    return render_template('source_details.html', source=query, upn_samples_number=upn_samples_number)

if __name__ == '__main__':
    app.run()
