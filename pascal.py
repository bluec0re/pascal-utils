#!/usr/bin/env python3
# encoding: utf-8

import argparse
from pathlib import Path
import tempfile
from xml.etree import ElementTree as ET
from collections import namedtuple, defaultdict
import pickle


Point = namedtuple('Point', 'x, y')
BoundingBox = namedtuple('BoundingBox', 'min, max')


class PascalClass:
    def __init__(self, root, clazz, type, cache=False):
        if isinstance(root, str):
            root = Path(root)
        self.root = root.absolute()
        self.image_path = self.root / 'JPEGImages'
        self.images = []
        self.clazz = clazz
        self.type = type
        self.bounding_boxes = defaultdict(list)
        self.cache = cache

        self.load_image_list()
        self.load_bounding_boxes()

    def load_image_list(self):
        image_list = self.root / "ImageSets" / "Main" / "{}_{}.txt".format(self.clazz, self.type)
        with image_list.open() as f:
            for line in f:
                image, flag = line.split()
                if int(flag) == 1:
                    path = self.image_path / "{}.jpg".format(image)
                    self.images.append(path)

    def load_bounding_boxes(self):
        if self.cache:
            try:
                with open('bb.cache', 'rb') as fp:
                    self.bounding_boxes = pickle.load(fp)
                return
            except:
                pass

        annotation_path = self.root / "Annotations"
        for image in self.images:
            xmlPath = "{}.xml".format(annotation_path / image.stem)
            xml = ET.parse(xmlPath)
            objs = xml.findall("//object[name='{}']".format(self.clazz))

            for obj in objs:
                xmin = int(obj.find('bndbox/xmin').text)
                ymin = int(obj.find('bndbox/ymin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymax = int(obj.find('bndbox/ymax').text)
                bb = BoundingBox(Point(xmin, ymin), Point(xmax, ymax))
                self.bounding_boxes[image.stem].append(bb)

        if self.cache:
            with open('bb.cache', 'wb') as fp:
                pickle.dump(self.bounding_boxes, fp)

    def __getitem__(self, name):
        return self.image_path / "{}.jpg".format(name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('CLASS')
    parser.add_argument('-t', '--type', default='train')
    parser.add_argument('-d', '--db', default='local/DBs/Pascal/VOC2011', type=Path)

    args = parser.parse_args()

    pc = PascalClass(args.db, args.CLASS, args.type)

    dirname = Path(tempfile.mkdtemp('-thesis'))

    for image in pc.images:
        target = dirname / image.name
        target.symlink_to(image)
