from __future__ import absolute_import, division, print_function

import os

from qtpy import QtWidgets

from glue.external.echo.qt import autoconnect_callbacks_to_qt
from glue.utils.qt import load_ui


class DendrogramLayerStyleEditor(QtWidgets.QWidget):

    def __init__(self, layer, parent=None):

        super(DendrogramLayerStyleEditor, self).__init__(parent=parent)

        self.ui = load_ui('layer_style_editor.ui', self,
                          directory=os.path.dirname(__file__))

        connect_kwargs = {'alpha': dict(value_range=(0, 1))}

        self._connections = autoconnect_callbacks_to_qt(layer.state, self.ui, connect_kwargs)
