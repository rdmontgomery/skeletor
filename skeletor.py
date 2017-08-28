# -*- coding: utf-8 -*-
"""
Bokeh skeleton to run Python code in a browser

Created on Mon Aug 28 10:18:59 2017

@author: rickmontgomery
"""

from bokeh.io import curdoc
from bokeh.layouts import layout, row, column, widgetbox
from bokeh.models.widgets import Button, Div, TextInput
from datetime import datetime


class App():
    def __init__(self):
        self.build_interface()

        self.console = Div()
        self.console_buffer = []
        self.BUFFER_SIZE = 30

        self.filename = ''

        self.index = 0
        self.start_time = datetime.utcnow()

    def update(self):
        now = datetime.utcnow()
        # This is where my 1 Hz operations for live feedback
        # would normally take place.
        if (now - self.start_time).total_seconds() >= self.index:
            self.index += 1

    def build_interface(self):
        self.widgets = {}

        self.widgets['filename_textinput'] = TextInput(
                title='Filename')
        self.widgets['filename_textinput'].on_change(
                'value', self.handle_filename)

        self.widgets['loadfile_button'] = Button(
                label='Load file', button_type='primary')
        self.widgets['loadfile_button'].on_click(self.handle_loadfile_button)

    def handle_filename(self, attr, old, new):
        self.print_to_console('Filename = {}'.format(new))

    def handle_loadfile_button(self):
        self.print_to_console('Running script.')
        # df = pd.read_csv(self.filename)
        # Perform your operations
        # df.to_csv('Exported results.csv')

    def print_to_console(self, new_str):
        new_str = f'{datetime.now().strftime("%H:%M:%S")} | ' + str(new_str)
        print(new_str)
        if len(self.console_buffer) < self.BUFFER_SIZE:
            self.console_buffer.append(new_str)
            self.console.text = ('{}<br>' * len(self.console_buffer))[:-4] \
                .format(*self.console_buffer)
        else:
            self.console_buffer.pop(0)
            self.console_buffer.append(new_str)
            self.console.text = ('{}<br>' * len(self.console_buffer))[:-4] \
                .format(*self.console_buffer)


app = App()

layout = layout([
        [Div(text='<h1>Skeletor</h1>')],
        [row(
            column(
                Div(text='<h2>Settings</h2>', width=200),
                widgetbox(
                    app.widgets['filename_textinput'],
                    width=200
                    )
                ),
            column(
                Div(text='<h2>Control</h2>', width=225),
                widgetbox(
                    app.widgets['loadfile_button'],
                    width=225
                    )
                ),
            column(
                Div(text='<h2>Console</h2>'),
                app.console
                    )
        )]
    ])

curdoc().add_periodic_callback(app.update, 50)
curdoc().add_root(layout)
curdoc().title = 'Masters of the Universe'
