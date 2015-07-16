#!/usr/bin/env python3
# encoding: utf-8

from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image, ImageDraw, ImageQt

from filter_gui import Ui_MainWindow
from pascal import PascalClass


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, list_file, dir, clazz, type, cache=False, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.clazz = clazz
        self.type = type
        self.list_file = list_file
        self._outputDir = Path(clazz) / type
        if not self._outputDir.exists():
            self._outputDir.mkdir(parents=True)
        self.pascalClass = PascalClass(dir, clazz, type, cache)

        self.list.itemClicked.connect(self.onItemClicked)
        self.deleteButton.clicked.connect(self.onDelete)
        self.saveButton.clicked.connect(self.onSave)
        self._current_item = None

        self.open()

#    @pyqtSlot()
    def onItemClicked(self, item):
        self._current_item = item
        self.image.setPixmap(item.data(Qt.UserRole))

    def onDelete(self):
        checked_items = self.list.checkedItems()
        for item in checked_items:
            self.list.takeItem(self.list.row(item))
            if item == self._current_item:
                self.image.setPixmap(QPixmap())

    def onSave(self):
        new_file = Path(self.list_file.name)
        new_file = new_file.parent / '{0.stem}.filtered{0.suffix}'.format(new_file)
        with new_file.open('w') as fp:
            for i in range(self.list.count()):
                item = self.list.item(i)
                fp.write('{} {}\n'.format(item.data(Qt.UserRole+1).stem, item.data(Qt.UserRole+2)))

    def open(self):
        self.list_file.seek(0)
        for line in self.list_file:
            image, bbid = line.strip().split(' ')
            bbid = int(bbid)
            image = self.pascalClass[image]
            bb = self.pascalClass.bounding_boxes[image.stem][bbid]

            self.list.addImage(self.load_pixmap(image, bb), image, bbid)

    def load_pixmap(self, path, bb=None):
        im = Image.open(str(path)).convert('RGBA')

        if bb is not None:
            overlay = Image.new('L', im.size, color=255/2)
            overlaydraw = ImageDraw.Draw(overlay)
            overlaydraw.rectangle(bb, fill=0)
            black = Image.new('RGBA', im.size, color=0xFF000000)
            black.putalpha(overlay)
            im = Image.alpha_composite(im, black)
        return ImageQt.toqpixmap(im)

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--class', default='bicycle', dest='cls', help='The pascal category/class')
    parser.add_argument('--cache', action="store_true", help='Cache the pascal data')
#    parser.add_argument('--load', action="store_true", help='Load last session')
    parser.add_argument('-t', '--type', choices=('val', 'train', 'trainval'), default='val', help='The list type')
    parser.add_argument('-d', '--pascal-dir', default="../server/thesis/DBs/Pascal/VOC2011", dest='dir', help='Folder containing a pascal dataset')
    parser.add_argument('FILE', help='File list from grouper.py', type=argparse.FileType('r'))
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    main = MainWindow(args.FILE, args.dir, args.cls, args.type, args.cache)
    main.show()
    exit(app.exec_())
