"""Flask Stack Simulator starter: complete TODOs during the live demo.
Before class, preview templates/index.html directly in the browser.
Running this file starts a status page, not the completed simulator.
"""
import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, session, flash
from stack_model import Stack

# url_for, session, and flash. Import secrets and the completed Stack class.
app = Flask(__name__)
# TODO P2: Set SECRET_KEY for the session and flash messages.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
# This lesson uses short fictional stack values on localhost.


@app.route('/')
def index():
    stack = Stack(session.get('items', []))
    return render_template('index.html', items=list(reversed(stack.items)), size = stack.size(), popped = session.get('popped', []), highlight = request.args.get('peek') == '1',)


@app.route('/stack', methods=['POST'])
def operate():
    action = request.form.get('action', '')
    value = request.form.get('value', '')
    stack = Stack(session.get('items', []))
    popped = list(session.get('popped', []))
    highlight = False
    if action == 'push':
        if not value or len(value) >24:
            flash('Enter 1 to 24 characters.', 'error')
        elif stack.size() >= 20:
            flash('limit: 20 items', 'error')
        else:
            stack.push(value)
            flash(f'Pushed: {value}', 'succpythoness')
    elif action == 'pop':
        removed = stack.pop()
        if removed is None:
            flash('Stack is empty', 'error')
        else:
            popped.insert(0, removed)
            popped = popped[:20]
            flash(f'Popped: {removed}', 'success')
    elif action == 'peek':
        top = stack.peek()
        flash('Stack is empty.' if top is None else f'Top: {top}', 'error' if top is None else 'success')
        highlight = top is not None
    elif action == 'clear':
        stack.clear()
        popped = []
        flash('Stack and deleted history cleared.', 'success')
    else:
        flash('Unknown operation.', 'error')
    session['items'] = stack.items
    session['popped'] = popped

    return redirect(url_for('index', peek='1') if highlight else url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()  # Local development only. Stop with Ctrl+C.
