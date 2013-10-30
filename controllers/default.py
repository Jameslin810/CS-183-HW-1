# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import random


@auth.requires_login()
def index():
    message_test = "test"
    session.welcome_msg = "Hello this is my page"
    rows = db(db.board).select()
    return dict(rows=rows)
	
@auth.requires_login()
def second():
	message = session.welcome_msg
        return dict(message = message)
	##c = session.counter or 0 
##	c += 1
	##session.counter = c

@auth.requires_login()
def add():
    form = SQLFORM(db.board, Upload = URL('download'))
    form.vars.urlLink = random.getrandbits(60)
    url= URL('default', 'view', args=[form.vars.urlLink])
    if form.process().accepted:
        redirect(URL('default', 'index'))
    return dict(form = form)

def view():
    my_record = db.board(request.args(0))
    record = 0
    check = request.args(0)
    rows = db(db.board).select()
    for r in rows:
        if(r.urlLink == int(check)):
          record = r.id
    my_record = db.board(record)
    if my_record is None:
        session.flash = "Invalid request"
        #redirect(URL('default', 'second'))
    form = SQLFORM(db.board, record=my_record, readonly=True, Upload = URL('download'))
    download_button = A('Download', _class='btn', _href=URL('default', 'download', args=[r.Upload]))
    #return dict(download_button = download_button)
    return dict(form=form, download_File = download_button)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
