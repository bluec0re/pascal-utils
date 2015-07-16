from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ImageList(QListWidget):
    def __init__(self, *args, **kwargs):
        super(ImageList, self).__init__(*args, **kwargs)

        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(100, 100))
        self.setSpacing(10)

    def addImage(self, pixmap, path, bbid=None):
        imageItem = QListWidgetItem(self)
        imageItem.setIcon(QIcon(pixmap))
        imageItem.setData(Qt.UserRole, pixmap)
        imageItem.setData(Qt.UserRole+1, path)
        imageItem.setData(Qt.UserRole+2, bbid)
        imageItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
        return imageItem


class CheckableImageList(ImageList):

    def addImage(self, pixmap, path, bbid):
        imageItem = super(CheckableImageList, self).addImage(pixmap, path, bbid)
        imageItem.setFlags(imageItem.flags() | Qt.ItemIsUserCheckable)
        imageItem.setCheckState(Qt.Unchecked)
        return imageItem

    def checkedItems(self):
        checked_items = []
        for index in range(self.count()):
            if self.item(index).checkState() == Qt.Checked:
                checked_items.append(self.item(index))
        return checked_items
