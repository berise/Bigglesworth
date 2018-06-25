from bisect import bisect_left

from Qt import QtCore, QtGui, QtWidgets


class DeltaSpin(QtWidgets.QSpinBox):
    delta = 0

    def textFromValue(self, value):
        return str(value + self.delta)

    def valueFromText(self, text):
        try:
            value = int(text) - self.delta
        except:
            value = self.value()
        self.setValue(value)


class DeviceIdSpin(QtWidgets.QSpinBox):
    def textFromValue(self, value):
        if value == 127:
            return 'Broadcast'
        return str(value)


class DevicePopupSpin(QtWidgets.QDoubleSpinBox):
    values = [0, .1, .2, .3, .4, .6, .7, .8, .9, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 1.8, 1.9, 2, 2.2, 2.3, 2.4, 2.5, 2.6, 2.8, 2.9,
        3, 3.1, 3.3, 3.4, 3.5, 3.6, 3.8, 3.9, 4, 4.1, 4.2, 4.4, 4.5, 4.6, 4.7, 4.9, 5, 5.1, 5.2, 5.3, 5.5, 5.6, 5.7, 5.8, 
        6, 6.1, 6.2, 6.3, 6.5, 6.6, 6.7, 6.8, 6.9, 7.1, 7.2, 7.3, 7.4, 7.6, 7.7, 7.8, 7.9, 8, 8.2, 8.3, 8.4, 8.5, 8.7, 8.8, 8.9, 
        9, 9.1, 9.3, 9.4, 9.5, 9.6, 9.8, 9.9, 10, 10.1, 10.3, 10.4, 10.5, 10.6, 10.7, 10.9, 11, 11.1, 11.2, 11.4, 11.5, 11.6, 11.7, 11.8, 
        12, 12.1, 12.2, 12.3, 12.5, 12.6, 12.7, 12.8, 13, 13.1, 13.2, 13.3, 13.4, 13.6, 13.7, 13.8, 13.9, 
        14.1, 14.2, 14.3, 14.4, 14.5, 14.7, 14.8, 14.9, 15, 15.2, 15.3, 15.4, 15.5]
    locale = QtCore.QLocale.system()
    decimalPoint = locale.decimalPoint()
    textValues = []
    for v in values:
        text = locale.toString(v)
        if not decimalPoint in text:
            text += decimalPoint + '0'
        textValues.append(text)

    def textFromValue(self, value):
        return self.textValues[int(value)]

    def valueFromText(self, text):
        if text.endswith('s'):
            text = text[:-1]
        value, valid = self.locale.toFloat(text)
        if not valid:
            return self.value()
        pos = bisect_left(self.values, value)
        if pos <= 1:
            return 1
        if pos == len(self.values):
            return 127
        before = self.values[pos - 1]
        after = self.values[pos]
        if after - value < value - before:
            return pos
        return pos - 1


class LedWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.active = False
        self.setFixedSize(24, 10)
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.deactivate)

    def activate(self):
        self.brush = self.activeBrush
        self.update()
        self.timer.start()

    def deactivate(self):
        self.brush = self.inactiveBrush
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setRenderHints(qp.Antialiasing)
        qp.translate(.5, .5)
        qp.setPen(self.pen)
        qp.setBrush(self.brush)
        qp.drawEllipse(0, 0, 8, 8)
        qp.translate(self.width() - 12, 0)
        qp.setPen(self.window().palette().color(QtGui.QPalette.Active, QtGui.QPalette.WindowText))
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawPath(self.connPath)


class LedInWidget(LedWidget):
    pen = QtGui.QColor(QtCore.Qt.darkRed)
    inactiveBrush = QtGui.QRadialGradient(.5, .5, .6, .3, .3)
    inactiveBrush.setCoordinateMode(inactiveBrush.ObjectBoundingMode)
    inactiveBrush.setColorAt(0, QtGui.QColor(140, 80, 80))
    inactiveBrush.setColorAt(1, QtGui.QColor(80, 0, 0))
    activeBrush = QtGui.QRadialGradient(.5, .5, .5, .3, .3)
    activeBrush.setCoordinateMode(activeBrush.ObjectBoundingMode)
    activeBrush.setColorAt(0, QtGui.QColor(255, 160, 160))
    activeBrush.setColorAt(1, QtGui.QColor(255, 0, 0))
    brush = inactiveBrush

    connPath = QtGui.QPainterPath()
    connPath.moveTo(0, 4)
    connPath.lineTo(4, 4)
    connPath.moveTo(2, 4)
    connPath.arcMoveTo(2, 1, 6, 6, 135)
    connPath.arcTo(2, 1, 6, 6, 135, -270)


class LedOutWidget(LedWidget):
    pen = QtGui.QColor(QtCore.Qt.darkGreen)
    inactiveBrush = QtGui.QRadialGradient(.5, .5, .6, .3, .3)
    inactiveBrush.setCoordinateMode(inactiveBrush.ObjectBoundingMode)
    inactiveBrush.setColorAt(0, QtGui.QColor(80, 140, 80))
    inactiveBrush.setColorAt(1, QtGui.QColor(0, 80, 0))
    activeBrush = QtGui.QRadialGradient(.5, .5, .5, .3, .3)
    activeBrush.setCoordinateMode(activeBrush.ObjectBoundingMode)
    activeBrush.setColorAt(0, QtGui.QColor(160, 255, 160))
    activeBrush.setColorAt(1, QtGui.QColor(0, 255, 0))
    brush = inactiveBrush

    connPath = QtGui.QPainterPath()
    connPath.moveTo(9, 4)
    connPath.arcMoveTo(1, 1, 6, 6, 45)
    connPath.arcTo(1, 1, 6, 6, 45, 270)
    connPath.moveTo(5, 4)
    connPath.lineTo(9, 4)


class MidiToolBox(QtWidgets.QWidget):
    offState = 180, 180, 180
    onState = 60, 255, 60
    pens = offState, onState

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum))
        self.compute()
        self.progState = False
        self.ctrlState = False

    def compute(self):
        self.smallFont = self.font()
        self.smallFont.setBold(True)
        self.smallFont.setPointSize(self.smallFont.pointSize() * .5 + 1)
        self.smallFontMetrics = QtGui.QFontMetrics(self.smallFont)
        self.boundingRect = QtCore.QRect(0, 0, self.smallFontMetrics.width('CTRL'), self.smallFontMetrics.height() * 2)

    def setProgState(self, state):
        self.progState = state
        self.update()

    def setCtrlState(self, state):
        self.ctrlState = state
        self.update()

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.FontChange:
            self.compute()
        elif event.type() == QtCore.QEvent.PaletteChange:
            self.offState.setRgb(self.palette().color(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText))
            self.onState.setRgb(self.palette().color(QtGui.QPalette.Active, QtGui.QPalette.WindowText))
        return QtWidgets.QWidget.changeEvent(self, event)

    def sizeHint(self):
        return self.boundingRect.size()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setFont(self.smallFont)
        progPen = QtGui.QColor(*self.pens[self.progState])
        ctrlPen = QtGui.QColor(*self.pens[self.ctrlState])
        if not self.isEnabled():
            progPen.setAlphaF(.5)
            ctrlPen.setAlphaF(.5)
        qp.setPen(progPen)
        qp.drawText(self.rect(), QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop, 'PGM')
        qp.translate(0, 1)
        qp.setPen(ctrlPen)
        qp.drawText(self.rect(), QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom, 'CTRL')

    def resizeEvent(self, event):
        self.compute()


class MidiWidget(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal()
    baseStyleSheet = '''
        MidiWidget {
            border: 1px solid transparent;
        }
        MidiWidget:hover {
            border-radius: 2px;
            border-left: 1px solid palette(midlight);
            border-right: 1px solid palette(mid);
            border-top: 1px solid palette(midlight);
            border-bottom: 1px solid palette(mid);
        }'''
    pressedStyleSheet = '''
        MidiWidget {
            border-radius: 2px;
            border-left: 1px solid palette(mid);
            border-right: 1px solid palette(midlight);
            border-top: 1px solid palette(mid);
            border-bottom: 1px solid palette(midlight);
        }'''

    def __init__(self, direction):
        QtWidgets.QFrame.__init__(self)
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(2)
        layout.setContentsMargins(2, 1, 2, 1)

        self.direction = direction
        if direction:
            self.ledWidget = LedOutWidget()
            text = 'OUT'
        else:
            self.ledWidget = LedInWidget()
            text = 'IN'
        layout.addWidget(self.ledWidget)
        self.label = QtWidgets.QLabel(text + ' (0)')
        self.label.setEnabled(False)
        layout.addWidget(self.label)

        self.toolBox = MidiToolBox()
        layout.addWidget(self.toolBox)

        self.setStyleSheet(self.baseStyleSheet)
        self.count = 0
        self.setProgState = self.toolBox.setProgState
        self.setCtrlState = self.toolBox.setCtrlState

    def setConnections(self, count):
        self.label.setText('{} ({})'.format('OUT' if self.direction else 'IN', int(count)))
        self.label.setEnabled(False if count else True)
        self.toolBox.setEnabled(True if count else False)

    def mousePressEvent(self, event):
        self.setStyleSheet(self.pressedStyleSheet)

    def mouseMoveEvent(self, event):
        self.setStyleSheet(self.pressedStyleSheet if event.pos() in self.rect() else self.baseStyleSheet)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet(self.baseStyleSheet)
        if event.pos() in self.rect():
            self.clicked.emit()

    def leaveEvent(self, event):
        QtWidgets.QFrame.leaveEvent(self, event)
        self.setStyleSheet(self.baseStyleSheet)

    def activate(self):
        if self.count:
            self.ledWidget.activate()


class MidiInWidget(MidiWidget):
    def __init__(self, *args, **kwargs):
        MidiWidget.__init__(self, False)


class MidiOutWidget(MidiWidget):
    def __init__(self, *args, **kwargs):
        MidiWidget.__init__(self, True)


class VerticalLabel(QtWidgets.QLabel):
    def sizeHint(self):
        size = QtWidgets.QLabel.sizeHint(self)
        return QtCore.QSize(size.height(), size.width())

    def minimumSizeHint(self):
        size = QtWidgets.QLabel.minimumSizeHint(self)
        return QtCore.QSize(size.height(), size.width())

    def paintEvent(self, event):
        rect = QtCore.QRect(0, 0, self.height(), self.width())
#        print(self.rect(), rect)
#        textRect = self.fontMetrics().boundingRect(rect, QtCore.Qt.TextExpandTabs, self.text())
        qp = QtGui.QPainter(self)
        qp.rotate(-90)
        qp.translate(-self.rect().height(), 0)
        qp.drawText(rect, self.alignment(), self.text())



class Waiter(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.timerRect = QtCore.QRect(0, 0, 31, 31)
        self.color = self.palette().color(QtGui.QPalette.WindowText)
        self.pen = QtGui.QPen(self.color, 2, cap=QtCore.Qt.FlatCap)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.update)
        self.elapsedTimer = QtCore.QElapsedTimer()
        self.elapsedTimer.start()
        self.setMinimumSize(48, 48)
        self._active = True

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active
        if active and self.isVisible():
            self.timer.start()
        else:
            self.timer.stop()

    def showEvent(self, event):
        if self.active:
            self.timer.start()

    def hideEvent(self, event):
        self.timer.stop()

    def sizeHint(self):
        return QtCore.QSize(48, 48)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.translate(.5, .5)
        qp.setRenderHints(qp.Antialiasing)
        qp.setBrush(self.palette().color(QtGui.QPalette.WindowText))
#        qp.drawEllipse(self.timerRect)
#        qp.setPen(self.pen)
#        adjustSize = self.timerRect.width() * .05
        secs, rest = divmod(self.elapsedTimer.elapsed() * .001, 1)
        if int(secs) & 1:
            qp.drawPie(self.timerRect, 1440, -rest * 5760)
        else:
            qp.drawPie(self.timerRect, 1440, 5760 - rest * 5760)
#        if not rest:
#            qp.drawEllipse(self.timerRect.adjusted(adjustSize, adjustSize, -adjustSize, -adjustSize))
#        else:
#            qp.drawArc(self.timerRect.adjusted(adjustSize, adjustSize, -adjustSize, -adjustSize), 1440, -rest * 5760)

    def resizeEvent(self, event):
        size = min(self.width(), self.height()) - 1
        self.timerRect = QtCore.QRect((self.width() - size) * .5, (self.height() - size) * .5, size, size)
        self.pen.setWidth(size * .1)

