#!/usr/bin/env python3
# encoding: utf-8
import sys

if sys.version_info < (3, 4):
    print("Python 3.4 or higher required")
    exit(-1)

from pathlib import Path

try:
    from PIL import Image, ImageQt, ImageDraw
except ImportError:
    print("Pillow required")

try:
    from PyQt5 import QtGui
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    print("PyQt5 required")

from grouper_gui import Ui_MainWindow
from pascal import PascalClass


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, clazz, dir, type, cache=False, load=False, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.lists = (
            self.leftList,
            self.rightList,
            self.topList,
            self.bottomList
        )
        self.leftShortcut = QShortcut(QtGui.QKeySequence("Left"), self)
        self.leftShortcut.activated.connect(self.onleft)
        self.rightShortcut = QShortcut(QtGui.QKeySequence("Right"), self)
        self.rightShortcut.activated.connect(self.onright)
        self.upShortcut = QShortcut(QtGui.QKeySequence("Up"), self)
        self.upShortcut.activated.connect(self.onup)
        self.downShortcut = QShortcut(QtGui.QKeySequence("Down"), self)
        self.downShortcut.activated.connect(self.ondown)
        self.spaceShortcut = QShortcut(QtGui.QKeySequence("Space"), self)
        self.spaceShortcut.activated.connect(self.onspace)
        self.escShortcut = QShortcut(QtGui.QKeySequence("Escape"), self)
        self.escShortcut.activated.connect(self.onesc)
        self.backspaceShortcut = QShortcut(QtGui.QKeySequence("Backspace"), self)
        self.backspaceShortcut.activated.connect(self.onbackspace)

        self.clazz = clazz
        self.type = type
        self._outputDir = Path(clazz) / type
        if not self._outputDir.exists():
            self._outputDir.mkdir(parents=True)
        self.pascalClass = PascalClass(dir, clazz, type, cache)

        if load:
            self.load()
        else:
            self.start()

    def _outfile(self, idx):
        return self._outputDir / "group_{}.txt".format(idx)

    def _updateList(self, idx):
        list = self.lists[idx]
        self._history.append((idx, list, list.addImage(self.currentImage.pixmap(), self.current)))
        with self._outfile(idx).open('a') as fp:
            fp.write("{} {}\n".format(self.current.stem, self.current_obj))
        if not self.next():
            QMessageBox.warning(self, "All images are processed", "All images are processed", QMessageBox.Ok)

    @pyqtSlot()
    def onleft(self, *args, **kwargs):
        self._updateList(0)

    @pyqtSlot()
    def onright(self, *args, **kwargs):
        self._updateList(1)

    @pyqtSlot()
    def onup(self, *args, **kwargs):
        self._updateList(2)

    @pyqtSlot()
    def ondown(self, *args, **kwargs):
        self._updateList(3)

    @pyqtSlot()
    def onspace(self, *args, **kwargs):
        if not self.next():
            QMessageBox.warning(self, "All images are processed", "All images are processed", QMessageBox.Ok)

    @pyqtSlot()
    def onbackspace(self, *args, **kwargs):
        if not self._history:
            QMessageBox.warning(self, "Nothing to undo", "Nothing to undo", QMessageBox.Ok)
            return

        idx, list, item = self._history.pop()
        list.takeItem(list.row(item))
        filepath = self._outfile(idx)
        with filepath.open() as fp:
            data = fp.read()
        data = data.split('\n')[:-2]
        with filepath.open('w') as fp:
            fp.write('\n'.join(data) + '\n')

        self.prev()

    def prev(self, cnt=2):
        if cnt == 0:
            return self.next()
        self.obj_index -= 1
        if self.obj_index < 0:
            self.img_index -= 2
            if self.img_index < 0:
                self.img_index = 0
            image = self.pascalClass.images[self.img_index]
            self.obj_index = len(self.pascalClass.bounding_boxes[image.stem]) - 1
        return self.prev(cnt-1)

    @pyqtSlot()
    def onesc(self, *args, **kwargs):
        self.close()

    def load(self):
        self.leftList.clear()
        self.rightList.clear()
        self.topList.clear()
        self.bottomList.clear()
        self._history = []
        self.img_index = 0
        self.obj_index = 0

        image_lists = [[]] * 4
        for i in range(4):
            with self._outfile(i).open('r') as fp:
                image_lists[i] = [line.strip().rsplit(' ', 1) for line in fp.readlines()]

        for i, image in enumerate(self.pascalClass.images):
            for j, bb in enumerate(self.pascalClass.bounding_boxes[image.stem]):
                empty = True
                for k in range(4):
                    if len(image_lists[k]) > 0:
                        empty = False
                        if image_lists[k][0][0] == image.stem and image_lists[k][0][1] == str(j):
                            image_lists[k].pop(0)
                            im = Image.open(str(image)).convert('RGBA')
                            overlay = Image.new('L', im.size, color=255/2)
                            overlaydraw = ImageDraw.Draw(overlay)
                            overlaydraw.rectangle(bb, fill=0)
                            black = Image.new('RGBA', im.size, color=0xFF000000)
                            black.putalpha(overlay)
                            im = Image.alpha_composite(im, black)
                            pixmap = ImageQt.toqpixmap(im)

                            self._history.append((k, self.lists[k], self.lists[k].addImage(pixmap, image)))
                            break
                if empty:
                    break
            if empty:
                break
        self.img_index = i
        self.obj_index = j
        self.next()

    def start(self):
        self.leftList.clear()
        self.rightList.clear()
        self.topList.clear()
        self.bottomList.clear()
        self._history = []
        self.img_index = 0
        self.obj_index = 0
        for i in range(4):
            self._outfile(i).open('w').close()

        return self.next()

    def next(self):
        if self.img_index >= len(self.pascalClass.images):
            return False

        filepath = self.pascalClass.images[self.img_index]
        objects = self.pascalClass.bounding_boxes[filepath.stem]
        self.current = filepath
        self.current_obj = self.obj_index
        self.show_image(filepath.absolute(), objects[self.obj_index])
        self.imageName.setText("{}".format(filepath.name))

        self.obj_index += 1
        if self.obj_index >= len(objects):
            self.obj_index = 0
            self.img_index += 1

        self.lcdNumber.display(self.obj_index)
        self.progressBar.setValue(self.img_index / len(self.pascalClass.images) * 100)

        return True

    def show_image(self, path, bb=None):
        im = Image.open(str(path)).convert('RGBA')

        if bb is not None:
            overlay = Image.new('L', im.size, color=255/2)
            overlaydraw = ImageDraw.Draw(overlay)
            overlaydraw.rectangle(bb, fill=0)
            black = Image.new('RGBA', im.size, color=0xFF000000)
            black.putalpha(overlay)
            im = Image.alpha_composite(im, black)
        pixmap = ImageQt.toqpixmap(im)
        self.currentImage.setPixmap(pixmap)

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--class', default='bicycle', dest='cls', help='The pascal category/class')
    parser.add_argument('--cache', action="store_true", help='Cache the pascal data')
    parser.add_argument('--load', action="store_true", help='Load last session')
    parser.add_argument('-t', '--type', choices=('val', 'train', 'trainval'), default='val', help='The list type')
    parser.add_argument('-d', '--pascal-dir', default="../server/thesis/DBs/Pascal/VOC2011", dest='dir', help='Folder containing a pascal dataset')
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = MainWindow(args.cls, args.dir, args.type, args.cache, args.load)
    window.show()
    sys.exit(app.exec_())
