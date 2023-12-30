from typing import Tuple
from abc import abstractmethod

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QPainterPath

from ...base import LineEditAnimationBase


class SimpleLineEditBase(LineEditAnimationBase):
    def __init__(self, parent=None):
        super(SimpleLineEditBase, self).__init__(parent)
        self.border_radius: int = 0

        self.setFocusPolicy(Qt.ClickFocus)
        self.setProperty("transparent", True)

    @abstractmethod
    def setParams(self, font_color: QColor, *args):
        self.setStyleSheet(f"LineEditBase{{color:'{font_color.name()}';border:none;padding-left:10px;}}")
        pass

    def paintEvent(self, event):
        super().paintEvent(event)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.border_radius, self.border_radius)

        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setClipPath(path)
        painter.setRenderHint(QPainter.Antialiasing)

        self.drawForeground(painter)

    def drawForeground(self, painter):
        pass


class SimpleLineEdit_1(SimpleLineEditBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_foucus = False
        self.line_width_anim = 0
        self.anim_start_color: QColor = QColor()
        self.anim_finish_color: QColor = QColor()

    def setParams(self,
                  font_color: QColor,
                  anim_start_color: QColor = QColor(),
                  anim_finish_color: QColor = QColor(),
                  border_radius: int = 10,
                  ):
        super().setParams(font_color)
        self.border_radius = 0
        self.anim_start_color = anim_start_color
        self.anim_finish_color = anim_finish_color

    def get_anim_range(self) -> Tuple:
        min_v = 0
        max_v = self.width()
        return min_v, max_v

    def drawForeground(self, painter: QPainter):
        painter.save()
        line_height = 2

        pen = QPen(QColor(self.anim_start_color), line_height, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(QPointF(0, self.height() - line_height),
                         QPointF(self.width(), self.height() - line_height))

        if self.is_foucus:
            pen = QPen(QColor(self.anim_finish_color), line_height, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(QPointF(0, self.height() - line_height),
                             QPointF(self.line_width_anim, self.height() - line_height))

        painter.restore()

    def onAnimParamChangeSignal(self, v) -> None:
        self.line_width_anim = v

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.is_foucus = True
        self.animForwardRun()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.is_foucus = False
        self.animBackwardRun()


class SimpleLineEdit_2(SimpleLineEditBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.border_radius = 0
        self.anim_start_color: QColor = QColor()
        self.anim_finish_color: QColor = QColor()

    def setParams(self,
                  font_color: QColor,
                  anim_start_color: QColor = QColor(),
                  anim_finish_color: QColor = QColor(),
                  border_radius: int = 10,
                  ):
        super().setParams(font_color)
        self.border_radius = 0
        self.anim_start_color = anim_start_color
        self.anim_finish_color = anim_finish_color

    def drawForeground(self, painter: QPainter):
        painter.save()
        if not self.hasFocus():
            line_color = self.anim_start_color
        else:
            line_color = self.anim_finish_color
        line_width = 2

        pen = QPen(QColor(line_color), line_width, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(QPointF(0, self.height() - line_width + 1),
                         QPointF(self.width(), self.height() - line_width + 1))
        painter.restore()

    def get_anim_range(self) -> Tuple:
        return 0, 0